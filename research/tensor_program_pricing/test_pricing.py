import importlib.util
from pathlib import Path
import unittest

import torch


PATH = Path(__file__).with_name("pricing.py")
SPEC = importlib.util.spec_from_file_location("tensor_program_pricing", PATH)
PRICING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRICING)


class PricingTests(unittest.TestCase):
    def setUp(self):
        self.gen = torch.Generator().manual_seed(7)

    def test_dense_and_gauge_equivalent_chain_have_identical_bytes(self):
        left = torch.randn(5, 3, generator=self.gen, dtype=torch.float64)
        right = torch.randn(3, 4, generator=self.gen, dtype=torch.float64)
        gauge = torch.randn(3, 3, generator=self.gen, dtype=torch.float64)
        gauge = gauge + 3 * torch.eye(3, dtype=torch.float64)
        dense = {"nodes": [{"name": "map", "op": "linear",
                            "weight": left @ right}]}
        chain = {"nodes": [{"name": "map", "op": "matrix_chain",
                            "left": left @ gauge,
                            "right": torch.linalg.solve(gauge, right)}]}
        self.assertEqual(PRICING.canonical_bytes(dense, 1e-8),
                         PRICING.canonical_bytes(chain, 1e-8))

    def test_cp_scale_sign_and_permutation_gauges_have_identical_bytes(self):
        left = torch.randn(4, 5, generator=self.gen, dtype=torch.float64)
        right = torch.randn(4, 5, generator=self.gen, dtype=torch.float64)
        down = torch.randn(6, 4, generator=self.gen, dtype=torch.float64)
        base = {"nodes": [{"name": "mlp", "op": "bilinear_cp",
                           "left": left, "right": right, "down": down}]}
        permutation = torch.tensor([2, 0, 3, 1])
        scales = torch.tensor([2.0, -0.5, 3.0, -4.0], dtype=torch.float64)
        transformed = {"nodes": [{"name": "mlp", "op": "bilinear_cp",
            "left": (left * scales[:, None])[permutation],
            "right": (right / scales[:, None])[permutation],
            "down": down[:, permutation]}]}
        self.assertEqual(PRICING.canonical_bytes(base, 1e-8),
                         PRICING.canonical_bytes(transformed, 1e-8))

    def test_shared_constant_is_serialized_once(self):
        table = torch.arange(32, dtype=torch.float64).reshape(8, 4)
        program = {"constants": {"tokens": table}, "nodes": [
            {"name": "a", "op": "generic", "kind": "lookup",
             "constant_refs": ["tokens"]},
            {"name": "b", "op": "generic", "kind": "lookup",
             "constant_refs": ["tokens"]}]}
        canonical = PRICING.canonical_program(program, 0.1)
        self.assertEqual(list(canonical["constants"]), ["tokens"])
        self.assertEqual(canonical["nodes"][0]["body"]["constant_refs"], ["tokens"])

    def test_generic_tensor_dof_removes_internal_gauge(self):
        self.assertEqual(PRICING.generic_tensor_dof([(4, 3), (3, 5)], [3]), 18)

    def test_indefinite_rank_two_quadratic_needs_one_product(self):
        matrix = torch.diag(torch.tensor([4.0, -9.0], dtype=torch.float64))
        result = PRICING.scalar_quadratic_bilinear_factors(matrix)
        reconstructed = sum(
            (torch.outer(left, right) + torch.outer(right, left)) / 2
            for left, right in zip(result["left"], result["right"])
        )
        self.assertEqual(result["inertia"], (1, 1))
        self.assertEqual(result["products"], 1)
        self.assertEqual(result["interface_dimension"], 2)
        torch.testing.assert_close(reconstructed, matrix)

    def test_quadratic_product_count_is_maximum_inertia(self):
        matrix = torch.diag(torch.tensor([16.0, 1.0, -9.0, 0.0],
                                         dtype=torch.float64))
        result = PRICING.scalar_quadratic_bilinear_factors(matrix)
        reconstructed = sum(
            (torch.outer(left, right) + torch.outer(right, left)) / 2
            for left, right in zip(result["left"], result["right"])
        )
        self.assertEqual(result["inertia"], (2, 1))
        self.assertEqual(result["products"], 2)
        self.assertEqual(result["interface_dimension"], 3)
        torch.testing.assert_close(reconstructed, matrix)

    def test_scalar_quadratic_program_uses_minimal_bilinear_rank(self):
        matrix = torch.diag(torch.tensor([144.9, -73.8], dtype=torch.float64))
        canonical = PRICING.canonical_program({"nodes": [{
            "name": "question_channel", "op": "scalar_quadratic",
            "matrix": matrix,
        }]}, step=1e-6)
        body = canonical["nodes"][0]["body"]
        self.assertEqual(body["op"], "scalar_quadratic_bilinear")
        self.assertEqual(body["rank"], 1)
        self.assertEqual(body["inertia"], [1, 1])
        self.assertEqual(body["interface_dimension"], 2)

    def test_rate_distortion_sweep_prices_quantized_artifact(self):
        table = torch.linspace(-1, 1, 257, dtype=torch.float64)
        program = {"constants": {"table": table}}

        def evaluator(canonical):
            encoded = canonical["constants"]["table"]
            restored = canonical["step"] * torch.tensor(encoded["q"])
            return (restored - table).square().mean()

        result = PRICING.rate_distortion_frontier(program, [1e-4, 1e-2, 0.1],
                                                  evaluator)
        points = sorted(result["points"], key=lambda point: point["step"])
        self.assertLessEqual(points[-1]["bits"], points[0]["bits"])
        self.assertGreaterEqual(points[-1]["distortion"], points[0]["distortion"])


if __name__ == "__main__":
    unittest.main()
