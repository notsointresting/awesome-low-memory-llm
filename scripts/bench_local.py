#!/usr/bin/env python3
"""Capture an attributable llama-bench candidate without claiming memory measurements.

Runs a local, already installed llama-bench binary. Never downloads models.
Stdlib only. Candidate results require human review before publication.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def finite_nonnegative(value, description):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{description} must be numeric")
    if not (0 <= value < float("inf")):
        raise ValueError(f"{description} must be finite and nonnegative")
    return value


def parse_llama_bench_output(raw, *, prompt, generate, repeats):
    """Require exactly one pp and one tg measurement from upstream JSON."""
    rows = json.loads(raw)
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError("Expected exactly two llama-bench rows (pp and tg)")
    results = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Invalid llama-bench row")
        p, n = row.get("n_prompt"), row.get("n_gen")
        if (p, n) == (prompt, 0):
            label = "prompt_processing"
        elif (p, n) == (0, generate):
            label = "text_generation"
        else:
            raise ValueError("Unexpected test configuration; review llama-bench version/flags")
        if label in results:
            raise ValueError("Duplicate llama-bench test")
        samples = row.get("samples_ts")
        if not isinstance(samples, list) or len(samples) != repeats:
            raise ValueError("Missing or incomplete per-repeat samples_ts")
        samples = [finite_nonnegative(v, "samples_ts") for v in samples]
        mean = finite_nonnegative(row.get("avg_ts"), "avg_ts")
        sd = finite_nonnegative(row.get("stddev_ts"), "stddev_ts")
        if mean <= 0 or any(v <= 0 for v in samples):
            raise ValueError("Throughput must be positive")
        results[label] = {
            "tokens": prompt if label == "prompt_processing" else generate,
            "mean_tokens_per_second": mean,
            "stddev_tokens_per_second": sd,
            "samples_tokens_per_second": samples,
        }
    if set(results) != {"prompt_processing", "text_generation"}:
        raise ValueError("Both prompt processing and generation are required")
    a, b = rows
    for key in ("build_commit", "model_type", "backends", "n_threads", "n_gpu_layers", "model_size"):
        if a.get(key) != b.get(key):
            raise ValueError(f"Disagreement between tests for {key}")
    return results, a


def system_ram_gib():
    """Only Linux MemTotal; no inference about available/peak memory."""
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                return round(int(line.split()[1]) / (1024 * 1024), 3)
    except (OSError, ValueError, IndexError):
        pass
    return None


def build_candidate(rows, metadata, args, command):
    results, row = parse_llama_bench_output(rows, prompt=args.prompt, generate=args.generate, repeats=args.repeats)
    file = Path(args.model)
    return {
        "schema_version": 1,
        "status": "candidate-unverified",
        "evidence": "community-reported",
        "tool": "llama-bench",
        "source_documentation": "https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md",
        "captured_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "runtime": {"name": "llama.cpp", "build_commit": row.get("build_commit"), "build_number": row.get("build_number"), "backends": row.get("backends")},
        "model": {"filename": file.name, "source_url": args.model_source, "revision": args.model_revision,
                  "quantization": args.quantization, "file_size_bytes": file.stat().st_size if file.is_file() else row.get("model_size"),
                  "type": row.get("model_type"), "parameters": row.get("model_n_params")},
        "hardware": {"os": platform.system(), "os_release": platform.release(), "cpu": row.get("cpu_info"),
                     "gpu": row.get("gpu_info"), "system_ram_gib": args.system_ram_gib if args.system_ram_gib is not None else system_ram_gib(),
                     "storage_medium": args.storage_medium, "gpu_vram_capacity_gib": args.gpu_vram_capacity_gib},
        "configuration": {"command": [Path(command[0]).name, *command[1:]], "threads": args.threads,
                          "gpu_layers": args.gpu_layers, "prompt_tokens": args.prompt,
                          "generation_tokens": args.generate, "repetitions": args.repeats,
                          "context_depth_tokens": 0, "batch_tokens": args.batch, "microbatch_tokens": args.ubatch,
                          "kv_cache_k": args.cache_k, "kv_cache_v": args.cache_v, "cache_state": "llama-bench-default-warmup"},
        "measurements": {**results, "time_to_first_token_ms": None, "peak_ram_gib": None,
                         "peak_vram_gib": None, "disk_read_bytes": None, "power_watts": None},
        "limitations": ["Not independently reproduced", "llama-bench excludes tokenization and sampling",
                        "TTFT, peak RAM and VRAM are not measured by this runner",
                        "Model may be larger than the available memory and can cause system swapping or OOM"],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--binary", required=True, help="Existing local llama-bench executable")
    ap.add_argument("--model", required=True, help="Existing local GGUF model file")
    ap.add_argument("--output", required=True, help="Candidate JSON output file (no upload)")
    ap.add_argument("--model-source", default=None, help="Official immutable model URL")
    ap.add_argument("--model-revision", default=None, help="Model revision or commit hash")
    ap.add_argument("--quantization", default=None)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--gpu-layers", type=int, default=0)
    ap.add_argument("--prompt", type=int, default=512)
    ap.add_argument("--generate", type=int, default=128)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--batch", type=int, default=512)
    ap.add_argument("--ubatch", type=int, default=128)
    ap.add_argument("--cache-k", default="f16")
    ap.add_argument("--cache-v", default="f16")
    ap.add_argument("--storage-medium", choices=["nvme", "sata-ssd", "hdd", "other", "unknown"], default="unknown")
    ap.add_argument("--system-ram-gib", type=float, default=None)
    ap.add_argument("--gpu-vram-capacity-gib", type=float, default=None)
    ap.add_argument("--timeout", type=int, default=1800, help="Total process timeout in seconds")
    args = ap.parse_args(argv)
    if not Path(args.binary).is_file():
        ap.error("The llama-bench binary must already exist at --binary")
    if not Path(args.model).is_file():
        ap.error("The GGUF model must already exist at --model")
    for n in ("threads", "prompt", "generate", "repeats", "batch", "ubatch", "timeout"):
        if getattr(args, n) <= 0:
            ap.error(f"--{n.replace('_', '-')} must be positive")
    if args.gpu_layers < 0:
        ap.error("--gpu-layers must be nonnegative")
    for n in ("system_ram_gib", "gpu_vram_capacity_gib"):
        v = getattr(args, n)
        if v is not None and (not (0 < v < float("inf"))):
            ap.error(f"--{n.replace('_', '-')} must be finite and positive")
    if Path(args.output).resolve() == Path(args.model).resolve():
        ap.error("Output cannot overwrite the model file")
    if Path(args.output).resolve() == Path(args.binary).resolve():
        ap.error("Output cannot overwrite the executable")
    command = [
        args.binary, "-m", args.model, "-p", str(args.prompt), "-n", str(args.generate),
        "-t", str(args.threads), "-ngl", str(args.gpu_layers), "-r", str(args.repeats),
        "-b", str(args.batch), "-ub", str(args.ubatch), "-ctk", args.cache_k,
        "-ctv", args.cache_v, "-o", "json",
    ]
    print("Running local llama-bench. No models are downloaded.", file=sys.stderr)
    try:
        run = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        ap.exit(1, f"Unable to complete local benchmark: {type(exc).__name__}. Check paths/hardware.\n")
    if run.returncode != 0:
        ap.exit(1, f"llama-bench exited with code {run.returncode}. See local logs and retry.\n")
    try:
        candidate = build_candidate(run.stdout, None, args, command)
    except (ValueError, json.JSONDecodeError) as exc:
        ap.exit(1, f"Unexpected llama-bench output: {exc}\n")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Candidate saved: {path}\nThis is NOT an independently verified result; inspect before sharing.")


if __name__ == "__main__":
    main()
