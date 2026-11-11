#!/usr/bin/env python3
"""Offline parser tests using synthetic llama-bench-style rows; NOT performance data."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from bench_local import parse_llama_bench_output


def fixture():
    base = {"build_commit": "fixture-only", "model_type": "fake 1B", "backends": "CPU",
            "n_threads": 4, "n_gpu_layers": 0, "model_size": 1000, "cpu_info": "synthetic",
            "gpu_info": "", "model_n_params": 1000,
            "avg_ts": 12.5, "stddev_ts": 0.5, "samples_ts": [12.0, 13.0]}
    return [dict(base, n_prompt=512, n_gen=0),
            dict(base, n_prompt=0, n_gen=128, avg_ts=7.0, samples_ts=[6.5, 7.5])]


class ParserTests(unittest.TestCase):
    def test_valid(self):
        result, metadata = parse_llama_bench_output(json.dumps(fixture()), prompt=512, generate=128, repeats=2)
        self.assertEqual(result["prompt_processing"]["mean_tokens_per_second"], 12.5)
        self.assertEqual(result["text_generation"]["samples_tokens_per_second"], [6.5, 7.5])
        self.assertEqual(metadata["build_commit"], "fixture-only")

    def test_wrong_repetitions(self):
        with self.assertRaises(ValueError):
            parse_llama_bench_output(json.dumps(fixture()), prompt=512, generate=128, repeats=3)

    def test_wrong_config(self):
        rows = fixture()
        rows[0]["n_prompt"] = 1024
        with self.assertRaises(ValueError):
            parse_llama_bench_output(json.dumps(rows), prompt=512, generate=128, repeats=2)

    def test_corrupt_or_missing(self):
        with self.assertRaises(ValueError):
            parse_llama_bench_output("{}", prompt=512, generate=128, repeats=2)
        rows = fixture()
        rows[1]["avg_ts"] = float("nan")
        with self.assertRaises(ValueError):
            parse_llama_bench_output(json.dumps(rows), prompt=512, generate=128, repeats=2)

    def test_mismatched_metadata(self):
        rows = fixture()
        rows[1]["build_commit"] = "different"
        with self.assertRaises(ValueError):
            parse_llama_bench_output(json.dumps(rows), prompt=512, generate=128, repeats=2)


if __name__ == "__main__":
    unittest.main()
