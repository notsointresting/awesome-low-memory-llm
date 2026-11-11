<div align="center">

# 🧠 Awesome Low-Memory LLM

**Run bigger language models on smaller hardware.**

A curated, hardware-first guide to local LLM inference, RAM/VRAM optimization, SSD offloading, quantization, and CPU-first inference.

[Explore projects](#-project-directory) · [Find your hardware](#-start-with-your-hardware) · [Compare techniques](#-techniques) · [Contribute](CONTRIBUTING.md)

![Awesome](https://awesome.re/badge.svg) ![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg) ![Link checks](https://github.com/notsointresting/awesome-low-memory-llm/actions/workflows/links.yml/badge.svg)

</div>

> [!IMPORTANT]
> **Low RAM does not mean low total memory, low storage, or fast tokens/second.** Some tools stream or offload weights, so SSD capacity and I/O speed matter. Claims below describe approaches—not independent benchmark results. See the [benchmark policy](BENCHMARKS.md).

## ⚡ Start with your hardware

| What you have | Where to start | What to check |
| --- | --- | --- |
| **CPU-only laptop / desktop** | [llama.cpp](https://github.com/ggml-org/llama.cpp), [Ollama](https://github.com/ollama/ollama), [KoboldCpp](https://github.com/LostRuins/koboldcpp) | Quantized model size, RAM, CPU instruction support |
| **Mac with Apple silicon** | [MLX LM](https://github.com/ml-explore/mlx-lm), [llama.cpp](https://github.com/ggml-org/llama.cpp), [Mistral.rs](https://github.com/EricLBuehler/mistral.rs) | Unified memory, context length, Metal backend |
| **Limited GPU VRAM** | [llama.cpp](https://github.com/ggml-org/llama.cpp), [ExLlamaV2](https://github.com/turboderp/exllamav2), [vLLM](https://github.com/vllm-project/vllm) | Supported quantization, offload path, total system RAM |
| **Android / mobile** | [MLC LLM](https://github.com/mlc-ai/mlc-llm), [llama.cpp](https://github.com/ggml-org/llama.cpp) | Device support, thermals, battery use |
| **Investigating SSD-backed inference** | [Edge0](https://github.com/Edge0-AI/Edge0), [FlexGen](https://github.com/FMInference/FlexGen) | Storage footprint, SSD throughput, reproducibility |
| **Researching sparse/MoE methods** | [PowerInfer](https://github.com/SJTU-IPADS/PowerInfer), [llama.cpp](https://github.com/ggml-org/llama.cpp) | Model architecture and platform compatibility |

These are **starting points, not guarantees of compatibility** with a specific memory budget or model. Choose a model, precision, and context length before comparing memory requirements.

## 🔬 Deep research: ten oversized-model and hardware-fit projects

**[Read the full technical comparison](research/2026-11-11-ten-projects.md)** — memory techniques, supported hardware, evidence, limitations, last activity, and primary-source links. All throughput figures are **author-reported**, not independently replicated.

| Project | Key idea | Important qualification |
| --- | --- | --- |
| [Edge0](https://github.com/Edge0-AI/Edge0) | SSD expert offload + trained next-step prerouter + quantized adapter recovery | Uses released matched checkpoints, adapters and prerouters; cross-platform memory figures are not di |
| [Colibri](https://github.com/JustVugg/colibri) | Hierarchical expert placement in GPU, host RAM, and NVMe | Not a universal all-architecture runtime; explicit per-model engines and large model downloads |
| [AirLLM](https://github.com/lyogavin/airllm) | Layer-by-layer transfer from disk to accelerator | Disk-intensive weight preparation and loading; macOS docs restrict support to Apple Silicon and Llam |
| [Slipstream](https://github.com/Schero94/slipstream) | llama.cpp/Metal fork with SSD MoE expert streaming and size-bounded cache | Mac app is ad-hoc signed, not Apple notarized; performance highly sensitive to SSD and cache; small  |
| [Swap-MoE](https://github.com/ek15072809/Swap-MoE) | llama.cpp patches for on-demand mmap paging of expert tensors | Fixating experts changes routing behavior, potentially affecting output quality; OS page cache and I |
| [InferSSD](https://github.com/wici-ai/inferssd) | llama.cpp-based SSD-streamed MoE experts using standard GGUF, Metal/CUDA backends | Supported architectures and GGUF conversions are limited/tested explicitly; vendor comparisons are a |
| [edgeMoE / BigMoeOnEdge](https://github.com/supastishn/edgeMoE) | CPU-only Android/desktop SSD or flash expert streaming on llama.cpp public API with b | README branding and badges point to Helldez/BigMoeOnEdge instead of this repository; confirm canonic |
| [HotPin](https://github.com/LozzKappa/hotpin-llm) | Routing-guided hot expert pinning (mlock / VirtualLock) and optional read-ahead for C | Benefits only when weights exceed available RAM |
| [DwarfStar (ds4)](https://github.com/antirez/ds4) | Narrow model-specialized engine, SSD streaming, Metal/CUDA/ROCm, multi-GPU and multi- | Not a generic GGUF runner; model list is intentionally narrow and may change; software described as  |
| [llmfit](https://github.com/AlexsJones/llmfit) | Hardware introspection, model compatibility scoring, estimated throughput and crowd-s | Predictions are estimates, not guarantees |

## 📚 Project directory

### Inference runtimes and local apps

| Project | Why it matters |
| --- | --- |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Portable GGUF inference with quantization and CPU/GPU offloading |
| [Ollama](https://github.com/ollama/ollama) | Straightforward way to run and serve local models |
| [MLX LM](https://github.com/ml-explore/mlx-lm) | LLM inference and fine-tuning on Apple silicon with MLX |
| [KoboldCpp](https://github.com/LostRuins/koboldcpp) | Local GGUF inference with a packaged interface |
| [MLC LLM](https://github.com/mlc-ai/mlc-llm) | Deployment-oriented LLM inference across device classes |
| [Mistral.rs](https://github.com/EricLBuehler/mistral.rs) | Rust-based LLM inference with quantization support |
| [vLLM](https://github.com/vllm-project/vllm) | High-throughput serving; **not necessarily suited to very low RAM** |
| [SGLang](https://github.com/sgl-project/sglang) | Efficient model serving; primarily an advanced-serving option |

### Techniques and research implementations

| Project | Focus | Caveat |
| --- | --- | --- |
| [Edge0](https://github.com/Edge0-AI/Edge0) | SSD-backed MoE weight streaming and predictive prefetch | Project performance claims are not independently verified here |
| [FlexGen](https://github.com/FMInference/FlexGen) | Offloading model execution across GPU, CPU, and disk | Research implementation; review model and setup compatibility |
| [PowerInfer](https://github.com/SJTU-IPADS/PowerInfer) | Activation-aware CPU/GPU hybrid inference | Check supported models and reproducibility |
| [ExLlamaV2](https://github.com/turboderp/exllamav2) | Quantized GPU inference | Hardware, format, and model-family constraints apply |
| [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8-bit and 4-bit quantization components | Library, not a complete inference application |
| [AutoGPTQ](https://github.com/AutoGPTQ/AutoGPTQ) | GPTQ quantization tooling | Check repository maintenance and supported stacks |
| [GPTQModel](https://github.com/ModelCloud/GPTQModel) | GPTQ model quantization and inference integration | Verify current backend compatibility |
| [AWQ](https://github.com/mit-han-lab/llm-awq) | Activation-aware weight quantization | Research/code availability does not imply turnkey deployment |
| [HQQ](https://github.com/mobiusml/hqq) | Half-quadratic quantization for LLMs | Quantization tooling; integration varies |
| [AQLM](https://github.com/Vahe1994/AQLM) | Additive quantization for LLM compression | Check supported model families and runtimes |

### Model formats and ecosystems

| Project | Focus |
| --- | --- |
| [GGUF](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) | Model file format used by llama.cpp and compatible tooling |
| [Hugging Face Transformers](https://github.com/huggingface/transformers) | Broad model ecosystem and inference APIs |
| [Optimum](https://github.com/huggingface/optimum) | Model hardware and inference optimization integrations |

### Hardware-fit discovery

| Project | Why it matters |
| --- | --- |
| [llmfit](https://github.com/AlexsJones/llmfit) | Detect CPU, RAM, GPU and VRAM to estimate what models fit and collect community benchmarks; not an inference engine |

## 🧩 Techniques

| Method | Idea | Trade-off |
| --- | --- | --- |
| **Quantization** | Store weights at lower precision | Accuracy and backend compatibility can vary |
| **CPU/GPU offloading** | Place some tensors or layers in host memory | PCIe or unified-memory limits and latency |
| **Disk / SSD offloading** | Fetch weights from storage rather than keeping all resident | Storage capacity, bandwidth, random I/O, latency |
| **Sparse activation / MoE routing** | Compute a subset of experts/weights per token | Depends on architecture and router behavior |
| **KV-cache optimization** | Reduce or manage attention-cache memory | Context length, precision, and quality trade-offs |
| **Memory-efficient attention** | Avoid unnecessary attention intermediates | Implementation-dependent constraints |

## 🧪 Benchmarks: evidence over hype

We do **not** rank tools by unverified "35B on 2 GB" headlines. For comparisons, record:

- Exact **model and variant**, dense vs. MoE, quantization format and bits/weight.
- **RAM peak, VRAM peak, and disk use** (measured separately), OS, CPU/GPU, and available memory.
- **Prompt processing and generation tokens/sec**, first-token latency, prompt/context lengths, and test settings.
- Source of result: **independently reproduced**, **author-reported**, or **community-reported**.

See [BENCHMARKS.md](BENCHMARKS.md), [the submission template](.github/ISSUE_TEMPLATE/benchmark.yml), and [machine-readable catalog](data/projects.json). The catalog intentionally contains **no invented minimum RAM or speed numbers**.

## 🛠️ Quick start: a local quantized model

1. Read [how to choose a model](guides/choosing-a-model.md).
2. Install a compatible runtime from its **official** documentation.
3. Select a license-compatible model small enough for available **RAM + VRAM**, including KV cache and runtime overhead.
4. Measure actual peak memory and generation speed on your hardware.
5. Share reproducible findings via a [benchmark issue](https://github.com/notsointresting/awesome-low-memory-llm/issues/new?template=benchmark.yml).

## 🤝 Contributing

Found a new runtime, a reproducible memory benchmark, or an outdated link? [Open a project submission](https://github.com/notsointresting/awesome-low-memory-llm/issues/new?template=project.yml) or a pull request. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. Inclusion is not an endorsement, and we avoid paid placement.

## 📜 License

[MIT](LICENSE). Individual linked projects have their own licenses and terms.
