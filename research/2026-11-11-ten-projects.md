# Deep research: 10 low-memory LLM projects

> Reviewed against upstream GitHub repository metadata and READMEs on **2026-11-11**. All performance figures below are **author-reported** and were **not reproduced independently** for this directory. Repository status is a snapshot, not an ongoing health guarantee.

## Reading this guide

**RAM** = host resident memory; **VRAM** = device memory; **SSD footprint** = model + temporary files on storage. They are different budgets. Project-specific memory peak metrics (RSS vs physical footprint vs working set) are not interchangeable. Author-reported benchmark rates may differ drastically with prompt length, context, quantization, I/O throughput, thermal state, CPU, and active expert distribution.

| Project | Technique | Hardware direction | Evidence | Status snapshot |
| --- | --- | --- | --- | --- |
| [Edge0](https://github.com/Edge0-AI/Edge0) | SSD expert offload + trained next-step prerouter + quantized adapter recovery | Project tests: Apple M5 16 GiB, iPhone 17 Pro Max, Android Snapdragon 8 Elite device with 16 GB, Windows CPU/R… | Author-reported | Active; 2026-11-11 |
| [Colibri](https://github.com/JustVugg/colibri) | Hierarchical expert placement in GPU, host RAM, and NVMe; CPU, Vulkan, CUDA backends; optimized model-family engines | README requires at least 8 GB host RAM (16+ preferable) and at least 22 GB free disk for smallest model. Large… | Author-reported | Active; 2026-11-11 |
| [AirLLM](https://github.com/lyogavin/airllm) | Layer-by-layer transfer from disk to accelerator; some MoE paths stream selected experts | GPU models vary: author reports 70B on 4 GB GPU VRAM; Kimi K3 on 3.72 GB GPU VRAM (RTX 6000 Ada). VRAM figures… | Author-reported | Active; 2026-11-11 |
| [Slipstream](https://github.com/Schero94/slipstream) | llama.cpp/Metal fork with SSD MoE expert streaming and size-bounded cache | Targets Apple Silicon Macs with 16–36 GB RAM and a sufficiently large, fast SSD; offers a macOS app and headle… | Author-reported | Unarchived; last push 2026-08-17 |
| [Swap-MoE](https://github.com/ek15072809/Swap-MoE) | llama.cpp patches for on-demand mmap paging of expert tensors; optional LRU retention, expert fixation and prefetch | Project targets Linux/Windows CPU-only PCs with 16 GB RAM and SSD with space for full quantized model; no GPU … | Author-reported | Unarchived; last push 2026-10-20 |
| [InferSSD](https://github.com/wici-ai/inferssd) | llama.cpp-based SSD-streamed MoE experts using standard GGUF, Metal/CUDA backends | macOS/Metal and Linux/CUDA documented. README says Windows in progress while also mentioning Windows release p… | Author-reported | Active; 2026-11-11 |
| [edgeMoE / BigMoeOnEdge](https://github.com/supastishn/edgeMoE) | CPU-only Android/desktop SSD or flash expert streaming on llama.cpp public API with bounded expert cache | Author describes tests on a 12 GB RAM Android phone; flash storage must hold complete quantized model (DeepSee… | Author-reported | Unarchived; last push 2026-08-03; provenance caution |
| [HotPin](https://github.com/LozzKappa/hotpin-llm) | Routing-guided hot expert pinning (mlock / VirtualLock) and optional read-ahead for CPU/NVMe MoE | Windows/Linux, AVX2+ CPU, NVMe recommended; measured Ryzen AI 9 HX 370 with 23.6 GB RAM.… | Author-reported | Unarchived; last push 2026-07-08 |
| [DwarfStar (ds4)](https://github.com/antirez/ds4) | Narrow model-specialized engine, SSD streaming, Metal/CUDA/ROCm, multi-GPU and multi-machine options | Primary target is high-memory personal hardware: Metal Macs with ~64–96+ GB for certain models; smaller Macs c… | Author-reported | Active; 2026-11-08; explicitly beta |
| [llmfit](https://github.com/AlexsJones/llmfit) | Hardware introspection, model compatibility scoring, estimated throughput and crowd-submitted empirical benchmarks | Runs on Linux, Windows, and macOS; scans CPU/RAM and GPU/VRAM where supported. Does not itself execute LLM inf… | Author-reported | Active; 2026-11-10 |

## Detailed project assessments

### 1. [Edge0](https://github.com/Edge0-AI/Edge0)

- **Status (2026-11-11):** Active; 2026-11-11.
- **Memory mechanism:** SSD expert offload + trained next-step prerouter + quantized adapter recovery.
- **Hardware / setup:** Project tests: Apple M5 16 GiB, iPhone 17 Pro Max, Android Snapdragon 8 Elite device with 16 GB, Windows CPU/RTX 4070 SUPER. Actual current unified engine supports edge0-35b; edge0-8b is planned..
- **Benchmark evidence (project author; NOT independently reproduced):** 35B model on M5 Metal: 24.8–24.9 tok/s, 3.43 GiB physical footprint; Android CPU: 11.4–11.8 tok/s, 2.82 GiB RSS (different metrics)..
- **Limitations / verification notes:** Uses released matched checkpoints, adapters and prerouters; cross-platform memory figures are not directly comparable..
- **Sources:** [Upstream repository](https://github.com/Edge0-AI/Edge0), [Supporting documentation 1](https://github.com/Edge0-AI/Edge0/blob/main/edge0-infer/docs/benchmarking.md), [Supporting documentation 2](https://github.com/Edge0-AI/Edge0/blob/main/edge0-infer/docs/limitations.md).

### 2. [Colibri](https://github.com/JustVugg/colibri)

- **Status (2026-11-11):** Active; 2026-11-11.
- **Memory mechanism:** Hierarchical expert placement in GPU, host RAM, and NVMe; CPU, Vulkan, CUDA backends; optimized model-family engines.
- **Hardware / setup:** README requires at least 8 GB host RAM (16+ preferable) and at least 22 GB free disk for smallest model. Large MoE models need far more storage..
- **Benchmark evidence (project author; NOT independently reproduced):** Project reports Qwen3.6-35B-A3B around 6 tok/s CPU and 30 tok/s CUDA on its specified test systems; results depend on model, quantization, hardware and cache..
- **Limitations / verification notes:** Not a universal all-architecture runtime; explicit per-model engines and large model downloads. Large MoEs can be much slower than smaller models..
- **Sources:** [Upstream repository](https://github.com/JustVugg/colibri), [Supporting documentation 1](https://github.com/JustVugg/colibri/blob/main/docs/quickstart.md).

### 3. [AirLLM](https://github.com/lyogavin/airllm)

- **Status (2026-11-11):** Active; 2026-11-11.
- **Memory mechanism:** Layer-by-layer transfer from disk to accelerator; some MoE paths stream selected experts.
- **Hardware / setup:** GPU models vary: author reports 70B on 4 GB GPU VRAM; Kimi K3 on 3.72 GB GPU VRAM (RTX 6000 Ada). VRAM figures do NOT represent complete host RAM or disk requirements..
- **Benchmark evidence (project author; NOT independently reproduced):** GPU memory is reported by author; generating the largest models may take many seconds or minutes per token. No independently repeated benchmark included here..
- **Limitations / verification notes:** Disk-intensive weight preparation and loading; macOS docs restrict support to Apple Silicon and Llama/Mistral-style architectures..
- **Sources:** [Upstream repository](https://github.com/lyogavin/airllm), [Supporting documentation 1](https://github.com/lyogavin/airllm#faq).

### 4. [Slipstream](https://github.com/Schero94/slipstream)

- **Status (2026-11-11):** Unarchived; last push 2026-08-17.
- **Memory mechanism:** llama.cpp/Metal fork with SSD MoE expert streaming and size-bounded cache.
- **Hardware / setup:** Targets Apple Silicon Macs with 16–36 GB RAM and a sufficiently large, fast SSD; offers a macOS app and headless functionality..
- **Benchmark evidence (project author; NOT independently reproduced):** Author's 36 GB Mac Qwen3.6-35B-A3B Q4: approximately 5.5 tok/s with 2 GiB cache vs ~19 tok/s with 14 GiB cache..
- **Limitations / verification notes:** Mac app is ad-hoc signed, not Apple notarized; performance highly sensitive to SSD and cache; small upstream community..
- **Sources:** [Upstream repository](https://github.com/Schero94/slipstream), [Supporting documentation 1](https://github.com/Schero94/slipstream/blob/main/BENCHMARKS.md), [Supporting documentation 2](https://github.com/Schero94/slipstream/blob/main/bench/RESULTS.md).

### 5. [Swap-MoE](https://github.com/ek15072809/Swap-MoE)

- **Status (2026-11-11):** Unarchived; last push 2026-10-20.
- **Memory mechanism:** llama.cpp patches for on-demand mmap paging of expert tensors; optional LRU retention, expert fixation and prefetch.
- **Hardware / setup:** Project targets Linux/Windows CPU-only PCs with 16 GB RAM and SSD with space for full quantized model; no GPU required..
- **Benchmark evidence (project author; NOT independently reproduced):** Author's 16 GB setup: Qwen3.5-35B-A3B Q4_K_M (19.7 GB disk) 7.28 tok/s; 122B Q2_K (42.6 GB) 2.00 tok/s..
- **Limitations / verification notes:** Fixating experts changes routing behavior, potentially affecting output quality; OS page cache and I/O strongly influence speed. Patch maintenance needed against llama.cpp..
- **Sources:** [Upstream repository](https://github.com/ek15072809/Swap-MoE), [Supporting documentation 1](https://github.com/ek15072809/Swap-MoE#benchmarks), [Supporting documentation 2](https://github.com/ek15072809/Swap-MoE#known-limitations).

### 6. [InferSSD](https://github.com/wici-ai/inferssd)

- **Status (2026-11-11):** Active; 2026-11-11.
- **Memory mechanism:** llama.cpp-based SSD-streamed MoE experts using standard GGUF, Metal/CUDA backends.
- **Hardware / setup:** macOS/Metal and Linux/CUDA documented. README says Windows in progress while also mentioning Windows release packages—verify actual feature parity before recommending Windows..
- **Benchmark evidence (project author; NOT independently reproduced):** Project provides 4K-prompt / 256-output benchmark protocol and comparison tables on M5 Max 48 GB and NVIDIA systems (e.g. 8 GB host RAM + 16 GB VRAM)..
- **Limitations / verification notes:** Supported architectures and GGUF conversions are limited/tested explicitly; vendor comparisons are author-run and may not be apples-to-apples across formats..
- **Sources:** [Upstream repository](https://github.com/wici-ai/inferssd), [Supporting documentation 1](https://github.com/wici-ai/inferssd/blob/main/docs/benchmark.md).

### 7. [edgeMoE / BigMoeOnEdge](https://github.com/supastishn/edgeMoE)

- **Status (2026-11-11):** Unarchived; last push 2026-08-03; provenance caution.
- **Memory mechanism:** CPU-only Android/desktop SSD or flash expert streaming on llama.cpp public API with bounded expert cache.
- **Hardware / setup:** Author describes tests on a 12 GB RAM Android phone; flash storage must hold complete quantized model (DeepSeek V4 Flash example ~91 GB)..
- **Benchmark evidence (project author; NOT independently reproduced):** Author reports ~0.94 tok/s for 284B model on 12 GB Android phone (256-token greedy decode test methodology)..
- **Limitations / verification notes:** README branding and badges point to Helldez/BigMoeOnEdge instead of this repository; confirm canonical origin and maintenance before elevating it. Optional expert dropping and reduced expert count are LOSSY, unlike baseline full-expert streaming..
- **Sources:** [Upstream repository](https://github.com/supastishn/edgeMoE), [Supporting documentation 1](https://github.com/supastishn/edgeMoE/blob/main/docs/benchmarks.md), [Supporting documentation 2](https://github.com/Helldez/BigMoeOnEdge).

### 8. [HotPin](https://github.com/LozzKappa/hotpin-llm)

- **Status (2026-11-11):** Unarchived; last push 2026-07-08.
- **Memory mechanism:** Routing-guided hot expert pinning (mlock / VirtualLock) and optional read-ahead for CPU/NVMe MoE.
- **Hardware / setup:** Windows/Linux, AVX2+ CPU, NVMe recommended; measured Ryzen AI 9 HX 370 with 23.6 GB RAM..
- **Benchmark evidence (project author; NOT independently reproduced):** Author reports GPT-OSS 120B Q4 (58.5 GB disk) at 2.6 tok/s in 19.1 GB RAM; Qwen3 30B-A3B 19.7 tok/s in 10.4 GB RAM..
- **Limitations / verification notes:** Benefits only when weights exceed available RAM. README contains a placeholder arXiv link; treat scholarly status as unverified. AGPL-3.0 license..
- **Sources:** [Upstream repository](https://github.com/LozzKappa/hotpin-llm), [Supporting documentation 1](https://github.com/LozzKappa/hotpin-llm#results).

### 9. [DwarfStar (ds4)](https://github.com/antirez/ds4)

- **Status (2026-11-11):** Active; 2026-11-08; explicitly beta.
- **Memory mechanism:** Narrow model-specialized engine, SSD streaming, Metal/CUDA/ROCm, multi-GPU and multi-machine options.
- **Hardware / setup:** Primary target is high-memory personal hardware: Metal Macs with ~64–96+ GB for certain models; smaller Macs can use SSD streaming. CUDA and Strix Halo ROCm supported..
- **Benchmark evidence (project author; NOT independently reproduced):** Author reports aggregate ~126 tok/s over 16 sessions on an eight-L40S setup; not a low-RAM single-PC benchmark..
- **Limitations / verification notes:** Not a generic GGUF runner; model list is intentionally narrow and may change; software described as beta..
- **Sources:** [Upstream repository](https://github.com/antirez/ds4), [Supporting documentation 1](https://github.com/antirez/ds4/blob/main/docs/SSD_STREAMING.md), [Supporting documentation 2](https://github.com/antirez/ds4/blob/main/docs/MODELS.md).

### 10. [llmfit](https://github.com/AlexsJones/llmfit)

- **Status (2026-11-11):** Active; 2026-11-10.
- **Memory mechanism:** Hardware introspection, model compatibility scoring, estimated throughput and crowd-submitted empirical benchmarks.
- **Hardware / setup:** Runs on Linux, Windows, and macOS; scans CPU/RAM and GPU/VRAM where supported. Does not itself execute LLM inference..
- **Benchmark evidence (project author; NOT independently reproduced):** Predicted tokens/sec estimates must be separated from user-contributed measured results; benchmark workflows are documented..
- **Limitations / verification notes:** Predictions are estimates, not guarantees. Ideal for selecting runtimes/models, not as a standalone inference engine..
- **Sources:** [Upstream repository](https://github.com/AlexsJones/llmfit), [Supporting documentation 1](https://github.com/AlexsJones/llmfit/blob/main/docs/benchmarking.md), [Supporting documentation 2](https://github.com/AlexsJones/llmfit/blob/main/docs/platform-support.md).


## Verification methodology and caveats

- **Verified here:** public repository exists, not archived at time of check, last activity as shown by GitHub, and descriptions or benchmarks appear in its own README/documentation.
- **Not verified:** executable builds, model downloads, independent benchmark replication, published numbers on other hardware, or safety of installing third-party binaries.
- **Source-of-claim:** every benchmark in this file is **project-author-reported**, not independently validated by the maintainers of this awesome list.
- **Canonical identity caution:** the `supastishn/edgeMoE` README uses branding and release links for `Helldez/BigMoeOnEdge`; investigate provenance before treating the former as official.
- **Maintenance caution:** GitHub unarchived status alone is not proof of active maintenance; review recent issues/releases when deciding on production use.
- **Security:** audit installation scripts and binary signatures before running them. Do not pipe remote shell scripts into a shell without reviewing them.

See [BENCHMARKS.md](../BENCHMARKS.md) before submitting independently reproducible measurements.
