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
