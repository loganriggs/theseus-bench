"""Canonical, gauge-aware tensor-program serialization prototype."""

import hashlib
import json
import math
import zlib

import torch


FORMAT_VERSION = 1


def _quantized_list(tensor, step):
    if step <= 0:
        raise ValueError("quantization step must be positive")
    q = torch.round(tensor.detach().double().cpu() / step).to(torch.int64)
    return {"shape": list(q.shape), "q": q.reshape(-1).tolist()}


def _sign_fix_svd(u, vh):
    u = u.clone()
    vh = vh.clone()
    for column in range(u.shape[1]):
        pivot = int(u[:, column].abs().argmax())
        if u[pivot, column] < 0:
            u[:, column] *= -1
            vh[column, :] *= -1
    return u, vh


def canonical_linear(weight, step, rank=None):
    weight = weight.detach().double().cpu()
    u, singular, vh = torch.linalg.svd(weight, full_matrices=False)
    if rank is None:
        tolerance = (torch.finfo(weight.dtype).eps * max(weight.shape)
                     * float(singular.max()))
        rank = int((singular > tolerance).sum())
    rank = min(int(rank), singular.numel())
    u, vh = _sign_fix_svd(u[:, :rank], vh[:rank, :])
    return {"op": "linear_svd", "rank": rank,
            "u": _quantized_list(u, step),
            "s": _quantized_list(singular[:rank], step),
            "vh": _quantized_list(vh, step)}


def _factor_key(tensor, step):
    payload = json.dumps(_quantized_list(tensor, step), separators=(",", ":"),
                         sort_keys=True).encode("ascii")
    return hashlib.sha256(payload).digest()


def _normalize_sign(vector):
    vector = vector.detach().double().cpu()
    norm = float(vector.norm())
    if norm == 0:
        return vector, 0.0, 1.0
    unit = vector / norm
    pivot = int(unit.abs().argmax())
    sign = -1.0 if unit[pivot] < 0 else 1.0
    return unit * sign, norm, sign


def canonical_bilinear_cp(left, right, down, step):
    """Canonicalize D[:,r] outer L[r,:] outer R[r,:]."""
    left = left.detach().double().cpu()
    right = right.detach().double().cpu()
    down = down.detach().double().cpu()
    if left.shape != right.shape or down.shape[1] != left.shape[0]:
        raise ValueError("expected left/right [rank,din], down [dout,rank]")
    components = []
    for index in range(left.shape[0]):
        l, nl, sl = _normalize_sign(left[index])
        r, nr, sr = _normalize_sign(right[index])
        d, nd, sd = _normalize_sign(down[:, index])
        coefficient = nl * nr * nd * sl * sr * sd
        if _factor_key(r, step) < _factor_key(l, step):
            l, r = r, l
        component = {"coefficient": int(round(coefficient / step)),
                     "left": _quantized_list(l, step),
                     "right": _quantized_list(r, step),
                     "down": _quantized_list(d, step)}
        key = json.dumps(component, separators=(",", ":"), sort_keys=True)
        components.append((key, component))
    components.sort(key=lambda item: item[0])
    return {"op": "bilinear_cp", "rank": left.shape[0],
            "components": [component for _, component in components]}


def scalar_quadratic_bilinear_factors(matrix, tolerance=None):
    """Return a minimum-product real bilinear factorization of ``x.T @ S @ x``.

    A product gate computes ``(left @ x) * (right @ x)``.  If the symmetric
    part of ``S`` has inertia ``(positive, negative)``, the exact minimum gate
    count is ``max(positive, negative)``.  Opposite-sign eigendirections share
    one gate via a difference of squares; unpaired directions use a square.

    The skew-symmetric part is discarded because it contributes zero to the
    scalar quadratic.  Eigenvalues at or below ``tolerance`` are treated as
    zero.  The returned rows satisfy

        S_symmetric = sum_r sym(left[r] outer right[r])

    up to the selected numerical tolerance.
    """
    matrix = matrix.detach().cpu()
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("scalar quadratic matrix must be square")
    if matrix.is_complex():
        raise ValueError("scalar quadratic matrix must be real")
    source_dtype = matrix.dtype
    matrix = matrix.double()
    symmetric = (matrix + matrix.T) / 2
    eigenvalues, eigenvectors = torch.linalg.eigh(symmetric)
    scale = float(eigenvalues.abs().max()) if eigenvalues.numel() else 0.0
    if tolerance is None:
        precision_dtype = source_dtype if source_dtype.is_floating_point else matrix.dtype
        # Promotion improves the solve but cannot remove roundoff already baked
        # into a low-precision input matrix. Numerical inertia must therefore use
        # the source precision unless the caller supplies a semantic threshold.
        tolerance = torch.finfo(precision_dtype).eps * max(matrix.shape) * scale
    tolerance = float(tolerance)
    if tolerance < 0:
        raise ValueError("tolerance must be nonnegative")

    positive = [index for index in range(eigenvalues.numel())
                if float(eigenvalues[index]) > tolerance]
    negative = [index for index in range(eigenvalues.numel())
                if float(eigenvalues[index]) < -tolerance]
    positive.sort(key=lambda index: float(eigenvalues[index]), reverse=True)
    negative.sort(key=lambda index: abs(float(eigenvalues[index])), reverse=True)

    # Fix the otherwise arbitrary sign of every (simple) eigendirection.
    vectors = eigenvectors.clone()
    for index in positive + negative:
        vector = vectors[:, index]
        pivot = int(vector.abs().argmax())
        if vector[pivot] < 0:
            vectors[:, index] *= -1

    left_rows = []
    right_rows = []
    paired = min(len(positive), len(negative))
    for offset in range(paired):
        pos = positive[offset]
        neg = negative[offset]
        pos_vector = math.sqrt(float(eigenvalues[pos])) * vectors[:, pos]
        neg_vector = math.sqrt(-float(eigenvalues[neg])) * vectors[:, neg]
        left_rows.append(pos_vector + neg_vector)
        right_rows.append(pos_vector - neg_vector)
    for pos in positive[paired:]:
        vector = math.sqrt(float(eigenvalues[pos])) * vectors[:, pos]
        left_rows.append(vector)
        right_rows.append(vector)
    for neg in negative[paired:]:
        vector = math.sqrt(-float(eigenvalues[neg])) * vectors[:, neg]
        left_rows.append(vector)
        right_rows.append(-vector)

    dimension = matrix.shape[0]
    if left_rows:
        left = torch.stack(left_rows)
        right = torch.stack(right_rows)
    else:
        left = torch.empty((0, dimension), dtype=matrix.dtype)
        right = torch.empty((0, dimension), dtype=matrix.dtype)
    return {"left": left, "right": right,
            "inertia": (len(positive), len(negative)),
            "products": max(len(positive), len(negative)),
            "interface_dimension": len(positive) + len(negative),
            "tolerance": tolerance}


def canonical_scalar_quadratic(matrix, step, tolerance=None):
    """Canonical payload for a scalar quadratic in the bilinear-product grammar."""
    factors = scalar_quadratic_bilinear_factors(matrix, tolerance)
    down = torch.ones((1, factors["products"]), dtype=torch.float64)
    body = canonical_bilinear_cp(factors["left"], factors["right"], down, step)
    body["op"] = "scalar_quadratic_bilinear"
    body["inertia"] = list(factors["inertia"])
    body["interface_dimension"] = factors["interface_dimension"]
    return body


def canonical_program(program, step):
    """Canonicalize a small typed program.

    Nodes are independent semantic outputs in this prototype. Shared tensor ids in
    `constants` are serialized once and referenced by name from generic nodes.
    """
    nodes = []
    for node in program.get("nodes", []):
        op = node["op"]
        if op == "linear":
            nodes.append({"name": node["name"],
                          "body": canonical_linear(node["weight"], step,
                                                   node.get("rank"))})
        elif op == "matrix_chain":
            weight = node["left"] @ node["right"]
            nodes.append({"name": node["name"],
                          "body": canonical_linear(weight, step, node.get("rank"))})
        elif op == "bilinear_cp":
            nodes.append({"name": node["name"],
                          "body": canonical_bilinear_cp(node["left"], node["right"],
                                                        node["down"], step)})
        elif op == "scalar_quadratic":
            nodes.append({"name": node["name"],
                          "body": canonical_scalar_quadratic(
                              node["matrix"], step, node.get("tolerance"))})
        elif op == "generic":
            nodes.append({"name": node["name"], "body": {
                "op": "generic", "kind": node["kind"],
                "inputs": sorted(node.get("inputs", [])),
                "constant_refs": sorted(set(node.get("constant_refs", [])))}})
        else:
            raise ValueError(f"unsupported op {op}")
    nodes.sort(key=lambda node: node["name"])
    constants = {name: _quantized_list(value, step)
                 for name, value in sorted(program.get("constants", {}).items())}
    return {"format": FORMAT_VERSION, "step": step, "nodes": nodes,
            "constants": constants}


def canonical_bytes(program, step):
    canonical = canonical_program(program, step)
    raw = json.dumps(canonical, separators=(",", ":"), sort_keys=True).encode("ascii")
    return zlib.compress(raw, level=9)


def price_bits(program, step):
    return 8 * len(canonical_bytes(program, step))


def rate_distortion_frontier(program, steps, evaluator):
    """Return nondominated (bits, distortion, step) points.

    evaluator receives the canonical program dict so the caller can use the real
    Theseus replacement verifier rather than a parameter-space proxy.
    """
    points = []
    for step in steps:
        canonical = canonical_program(program, step)
        points.append({"step": step, "bits": price_bits(program, step),
                       "distortion": float(evaluator(canonical))})
    frontier = []
    for point in sorted(points, key=lambda item: (item["bits"], item["distortion"])):
        if not frontier or point["distortion"] < min(x["distortion"] for x in frontier):
            frontier.append(point)
    return {"points": points, "frontier": frontier}


def generic_tensor_dof(node_sizes, internal_bond_dims, stabilizer_dim=0):
    """Generic quotient dimension diagnostic, separate from description bits."""
    return (sum(math.prod(shape) for shape in node_sizes)
            - sum(int(rank) ** 2 for rank in internal_bond_dims)
            + int(stabilizer_dim))
