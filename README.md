<div align="center">

# 🧠 Awesome Low-Memory LLM

**Run bigger language models on smaller hardware.**

A curated, hardware-first guide to local LLM inference, RAM/VRAM optimization, SSD offloading, quantization, and CPU-first inference.

[Explore projects](#-project-directory) · [Find your hardware](#-start-with-your-hardware) · [Compare techniques](#-techniques) · [Contribute](CONTRIBUTING.md)

![Awesome](https://awesome.re/badge.svg) ![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg) ![Link checks](https://github.com/notsointresting/awesome-low-memory-llm/actions/workflows/links.yml/badge.svg)

</div>

> [!IMPORTANT]
> **Low RAM does not mean low total memory, low storage, or fast tokens/second.** Some tools stream or offload weights, so SSD capacity and I/O speed matter. Claims below describe approaches—not independent benchmark results. See the [benchmark policy](BENCHMARKS.md).

## 🌐 Interactive visual hardware explorer

**[Open the Low-Memory LLM Atlas](docs/index.html)** — a responsive, framework-free HTML app with search, hardware filters, source-labeled model tests, and technical caveats. [Setup GitHub Pages](docs/README.md) to publish at a public URL.

## ⚡ Start with your hardware

| What you have | Where to start | What to check |
| --- | --- | --- |
| **CPU-only laptop / desktop** | [llama.cpp](https://github.com/ggml-org/llama.cpp), [Ollama](https://github.com/ollama/ollama), [KoboldCpp](https://github.com/LostRuins/koboldcpp) | Quantized model size, RAM, CPU instruction support |
| **Mac with Apple silicon** | [MLX LM](https://github.com/ml-explore/mlx-lm), [llama.cpp](https://github.com/ggml-org/llama.cpp), [Mistral.rs](https://github.com/EricLBuehler/mistral.rs) | Unified memory, context length, Metal backend |
| **Limited GPU VRAM** | [llama.cpp](https://github.com/ggml-org/llama.cpp), [ExLlamaV2](https://github.com/turboderp/exllamav2), [vLLM](https://github.com/vllm-project/vllm) | Supported quantization, offload path, total system RAM |
| **Android / mobile** | [MLC LLM](https://github.com/mlc-ai/mlc-llm), [llama.cpp](https://github.com/ggml-org/llama.cpp) | Device support, thermals, battery use |
| **Investigating SSD-backed inference** | [Edge0](https://github.com/Edge0-AI/Edge0), [FlexGen](https://github.com/FMInference/FlexGen) | Storage footprint, SSD throughput, reproducibility |
| **Researching sparse/MoE methods** | [PowerInfer](https://github.com/Tiiny-AI/PowerInfer), [llama.cpp](https://github.com/ggml-org/llama.cpp) | Model architecture and platform compatibility |

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
| [PowerInfer](https://github.com/Tiiny-AI/PowerInfer) | Activation-aware CPU/GPU hybrid inference | Check supported models and reproducibility |
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

### New: embedded devices, consumer PCs and hardware guidance (Nov 2026)

| Project | Practical reason to explore it |
| --- | --- |
| [Strata](https://github.com/Niko1221/Strata) | SSD-assisted inference and localhost APIs on consumer PCs |
| [FreeToken](https://github.com/flashml-org/freetoken) | Adaptive MoE cache management across accelerator and host resources |
| [PicoLM](https://github.com/RightNow-AI/picolm) | C runtime with author-reported ~45 MB runtime memory for embedded testing |
| [oMLX](https://github.com/jundot/omlx) | Apple Silicon server with tiered SSD/KV caching |
| [BigMoeOnEdge](https://github.com/Helldez/BigMoeOnEdge) | Current upstream for mobile/desktop bounded-memory MoE expert streaming |
| [Low-Spec Coding LLM Setup](https://github.com/Yasvanth-S/local-coding-llm-low-spec-setup) | A measured llama.cpp/aider coding setup on a GTX 1650 4 GB VRAM laptop |

> [!NOTE]
> These are **author-published** results. They are not our own independent benchmark runs. `edgeMoE` references a different repository in its README; see [BigMoeOnEdge](https://github.com/Helldez/BigMoeOnEdge) for the more active upstream.

### Extreme-scale CPU streaming: Kimi K3 in C

[**kimi-k3-in-c**](https://github.com/FareedKhan-dev/kimi-k3-in-c) is a portable C99 Kimi K3 engine. The author reports **2.78T parameters**, **8.24 GB peak RSS**, and **~26.5 seconds per token** with an 8 GB memory preset on a high-end test machine. **It still requires ~1.7 TB free SSD space** (checkpoint and packed trunk). These are author-reported measurements, **not independent tests**. An 8.24 GB peak footprint is also *greater* than 8.00 GB, so the 8 GB label is not a hard minimum-RAM guarantee.

## 🧭 Research expansion — November 2026

The [interactive Atlas](docs/index.html), [side-by-side comparison](docs/compare.html), and [market landscape](research/2026-11-11-market-landscape.md) now cover **53 projects**. These are curated *techniques and tools*, not a claim that every project runs on an 8 GB computer.

| Newly researched project | What it adds | Important boundary |
| --- | --- | --- |
| [MoE-Infinity](https://github.com/EfficientMoE/MoE-Infinity) | Hierarchical MoE expert offloading | Single-GPU DeepSeek-V2-Lite docs suggest at least 16 GB VRAM plus fast SSD; not an 8 GB CPU-only tool |
| [KTransformers](https://github.com/kvcache-ai/ktransformers) | Hybrid CPU–GPU MoE kernels | Real configurations in official guides may require 24+ GB GPU VRAM and hundreds of GB host RAM; do not infer laptop compatibility from 'hybrid' |
| [BitNet (bitnet.cpp)](https://github.com/microsoft/BitNet) | 1.58-bit inference for compatible models | Not a drop-in way to run an arbitrary existing Llama/Qwen checkpoint at 1 |
| [MNN / MNN-LLM](https://github.com/alibaba/MNN) | Mobile-first inference and INT4 quantization | Claimed speeds for tiny models on latest iPhones do not generalize to large models or typical Android phones |
| [ExecuTorch](https://github.com/pytorch/executorch) | PyTorch on-device deployment | A deployment framework, not proof that a particular 7B+ LLM fits; device backend and model export are required |
| [LiteRT](https://github.com/google-ai-edge/LiteRT) | Google on-device ML/GenAI runtime | A general edge runtime; check generative model operators, delegate availability and model packaging |
| [WebLLM](https://github.com/mlc-ai/web-llm) | WebGPU in-browser local inference | Requires compatible WebGPU browser/GPU and downloaded model files; browser memory and device limits still apply |
| [ONNX Runtime GenAI](https://github.com/microsoft/onnxruntime-genai) | ONNX generative model runtime | Model conversion, tokenizer and execution provider support vary; not specifically an SSD-streaming system |
| [OpenVINO GenAI](https://github.com/openvinotoolkit/openvino.genai) | Intel CPU/iGPU optimized inference | Optimization depends on supported Intel hardware and converted model variants; no universal minimum RAM |
| [SqueezeLLM](https://github.com/SqueezeAILab/SqueezeLLM) | Dense-and-sparse weight quantization | Research-focused; latest recorded upstream push was in 2024 |
| [LLM Compressor](https://github.com/vllm-project/llm-compressor) | Model compression for serving | A compression pipeline, not a local inference app; produced formats depend on target runtime and accelerator |
| [MobileLLM](https://github.com/facebookresearch/MobileLLM) | Sub-billion on-device model design | Primarily model/training research rather than a general-purpose local inference engine |
| [Betelgeuse](https://github.com/Betelgeuse-AI/Betelgeuse) | Bounded VRAM MoE expert paging | Author benchmarks center on RTX 3060 12 GB VRAM + 16 GB RAM, warm/repeated workloads, and a narrow setup; not a general 748B solution |
| [llama-modchip](https://github.com/synchopate/llama-modchip) | CPU-first sparse MoE + quantized GGUF optimizations | Author's headline 284B test is on 64 GB RAM with special quantization; not equivalent to 8 or 16 GB systems |
| [Speedy](https://github.com/DevDock-AI/Speedy) | RTX 3080 tuned Strata fork | Published Q4 comparison uses 128 GB system RAM and third-party GPU-unlock kernel module; 10 GB VRAM is NOT the full hardware requirement |
| [Pithos](https://github.com/benmaster82/Pithos) | Small C engine with expert streaming | Specializes in LFM families; author speed comparisons are specific to particular devices/models and experimental GPU backends |
| [FlashAttention](https://github.com/Dao-AILab/flash-attention) | IO-aware exact attention kernels | Kernel library, not a complete low-RAM inference engine; hardware/dtype support differs by version |
| [FlashInfer](https://github.com/flashinfer-ai/flashinfer) | LLM serving kernel library | Primarily accelerator serving infrastructure; not a CPU-only low-RAM consumer application |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | NVIDIA optimized inference and serving | Serving framework for compatible NVIDIA hardware; not a 4 GB laptop solution |

**Important:** Project hardware claims remain upstream-reported unless explicitly independently reproduced. Model weight storage, host RAM, accelerator VRAM, and context/KV memory are different constraints. See [benchmark methodology](BENCHMARKS.md).

## 📏 Community benchmark lab

**[Open the Benchmark Lab](docs/benchmark-lab.html)** · [Benchmark methodology](BENCHMARKS.md) · [Contribute a result](https://github.com/notsointresting/awesome-low-memory-llm/issues/new?template=benchmark.yml)

We now provide a **reproducible llama.cpp `llama-bench` wrapper** that records build/version, model size, test configuration, prompt-processing and generation throughput, plus raw per-repeat throughput samples. The output is a **local candidate submission**, never an automatically verified benchmark. It deliberately leaves TTFT, peak RAM and VRAM unknown because `llama-bench` does not measure them.

```bash
python scripts/bench_local.py --binary /path/to/llama-bench \
  --model /path/to/model.gguf --threads 4 --gpu-layers 0 \
  --prompt 512 --generate 128 --repeats 5 --output my-benchmark.json
```

**New reproducibility directories:**
- [locallm-bench](https://github.com/chutapp/locallm-bench) — cpu-only 16 gb reproducible test suite; The machines are cloud VMs, not typical 8 GB laptops.
- [local-llm-benchmarks](https://github.com/matnum/local-llm-benchmarks) — strix halo benchmark matrix; 128 GB desktop results do not generalize to 8/16 GB laptop tests; exact hardware and pinned software versions matter.
- [benchmarking-local-llm-hosting](https://github.com/carpetbot/benchmarking-local-llm-hosting) — edge hardware benchmark and cost tracking; Mix of measured and estimated/historical data may appear; only source-identified raw runs should be used as numerical evidence.

> No independent hardware benchmarks have been run by this repository's maintainer. Published upstream performance examples remain clearly labeled author-reported; submitted local output requires source and manual review.

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
