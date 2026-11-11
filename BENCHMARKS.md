# Benchmark methodology

**No independently reproduced benchmark measurements are currently published by the maintainers.** Author-reported upstream figures appear separately in the Atlas. Candidate community submissions remain unverified until reviewed.

## Required fields

- Tool name, repository URL, commit/release, OS, runtime version, and complete command or configuration.
- Model repository and exact revision, parameter size (including active parameters for MoE where available), quantization type, and weight-file size.
- Hardware: CPU, GPU, VRAM, RAM total, storage medium and available capacity, and power mode if relevant.
- Prompt length, generation length, context window, batch size, and KV-cache settings.
- Measurement procedure, repeated runs, peak **host RAM**, peak **device VRAM**, **disk footprint**, prompt tokens/sec, generation tokens/sec, time to first token.
- Status: **independently reproduced**, **community-reported**, or **author-reported**, with a public source or log.

## Rules

Use consistent tokenization and report definitions. Different tokenizers, batch sizes, contexts, and quantization settings must not be compared as equivalent. Report uncertainty and device thermal throttling when relevant. Do not equate sparse MoE total parameters with dense-model compute requirements. Do not infer minimum RAM from a compressed model file size. We will clearly label unverifiable or not-yet-reproduced claims.

## Template

Use the [benchmark issue form](.github/ISSUE_TEMPLATE/benchmark.yml) to submit data. The maintainers review and annotate results before adding them to a comparison table.

## Reproduce a baseline on an 8 GB or 16 GB computer

Choose a model **with a documented license and an appropriate quantization**, and leave space for OS, runtime and KV cache. An 8 GB physical RAM computer does not offer 8 GB free to the model. Do not select a model from parameter count alone.

The [Benchmark Lab](docs/benchmark-lab.html) generates a local command for `scripts/bench_local.py`. It wraps [upstream llama-bench](https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md) in a subprocess without downloading or installing any model. It runs prompt processing (pp) and text generation (tg) with identical quantization, runtime revision and parameters, then writes a **candidate JSON** to disk.

```sh
python scripts/bench_local.py --binary ./build/bin/llama-bench \
  --model ./models/MODEL.gguf --threads 4 --gpu-layers 0 \
  --prompt 512 --generate 128 --repeats 5 \
  --model-source https://huggingface.co/OWNER/REPO \
  --model-revision REVISION --quantization Q4_K_M \
  --output my-benchmark.json
```

### Recorded automatically

- OS, CPU (as exposed by the system), build commit, `llama-bench` CPU/GPU names and backends;
- Model filename (not its complete local path), on-disk size where available, `model_type`, exact command flags and run timestamp;
- Prompt processing and generation mean token rates, standard deviation, per-repeat token rates, model parameter count when included;
- If `--system-ram-gib` is provided, the test machine's system RAM (not peak RAM); on Linux the wrapper can obtain MemTotal from `/proc/meminfo`.

### Explicitly NOT measured

- **Time to first token (TTFT):** `llama-bench` does not include tokenization/sampling or the whole serving/request path.
- **Peak process RAM (RSS), peak VRAM, SSD read bytes, cold-start load times, power and quality:** not provided by `llama-bench` itself. We leave these `null` instead of calculating them from file size or GPU capacity.
- **Usability or model quality:** a fast model may not answer a real question well.

For these metrics, collect extra logs from a separate monitoring tool and document sampling rate, units, and peak measurement boundary; do not attach unsupported metrics to the wrapper output.

### Cold versus warm runs

`llama-bench` performs warmups by default. Its throughput is **not a cold-start TTFT**. Mark separate cold-start experiments as such and describe dropped filesystem cache or process restarts. Do not flush page cache on shared computers without understanding the effects.

### Submission process

1. Run the wrapper on **your** hardware, inspect `my-benchmark.json` and redact identifying paths/hostnames or usernames.
2. Include model source and immutable revision, quantization, OS, GPU driver if used, real system RAM, storage type, model size, context/KV settings, and every command flag.
3. Submit via [benchmark issue](.github/ISSUE_TEMPLATE/benchmark.yml) with your candidate JSON or log and any caveats.
4. Maintainers distinguish `community-reported` from `independently-reproduced`. A GitHub issue alone never upgrades a claim to independent replication.

All submitted data is reviewed before inclusion in [the accepted community index](data/community-benchmarks.json). **That index starts empty** and never includes synthetic test fixtures.

### Reproducible benchmark collections to consult

- [locallm-bench](https://github.com/chutapp/locallm-bench): Published 150 author-run tests across model/quantization/context configurations on 16 GB AMD EPYC cloud VMs, including memory caps and stability scenarios. The machines are cloud VMs, not typical 8 GB laptops. Its measured tok/s and usability criteria are workload-specific; results are not independently replicated by this directory.
- [local-llm-benchmarks](https://github.com/matnum/local-llm-benchmarks): Reproducible llama.cpp benchmark matrix on AMD Ryzen AI Max+ 395 128 GB unified memory, including prefill, decode, TTFT, power and token-efficiency. 128 GB desktop results do not generalize to 8/16 GB laptop tests; exact hardware and pinned software versions matter.
- [benchmarking-local-llm-hosting](https://github.com/carpetbot/benchmarking-local-llm-hosting): Documents SBC, Mac Mini and local-hosting measurements, including measured throughput, power, and cost methodology. Mix of measured and estimated/historical data may appear; only source-identified raw runs should be used as numerical evidence.

The upstream [llama-bench README](https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md) documents `-m`, `-p`, `-n`, `-r`, `-t`, `-ngl` and `-o json`; its generated rows include `avg_ts`, `stddev_ts` and `samples_ts`.
