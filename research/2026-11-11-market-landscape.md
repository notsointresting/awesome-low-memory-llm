# Low-memory LLM market landscape — November 11, 2026

> **Method**: qualitative desk research using official GitHub READMEs, public GitHub repository metadata, [Trendshift inference directory](https://trendshift.io/topics/llm-inference), and openly accessible fit tools. Snapshot only; **no hands-on inference benchmarks, benchmark replays, market-size estimates, or user interviews** were conducted. Individual project descriptions and requirements are upstream-published, not guarantees.

## Executive synthesis

The local inference market has three competing constraints: **weight residency**, **KV-cache/context memory**, and **I/O throughput**. A project that solves one may leave another untouched. A recent [2026 academic survey](https://link.springer.com/article/10.1007/s10462-026-11651-1) frames the problem as data movement across weights, KV cache and activations. Consequently, a useful low-memory directory must separate **total device RAM**, **peak process RAM**, **GPU VRAM**, **disk footprint**, **prefill**, **decode**, and **cold versus warm cache**.

**Positioning recommendation:** be the open, evidence-labeled atlas of *inference techniques* rather than an unverified list of models that "fit" in a particular RAM tier.

## Ecosystem segmentation

| Segment | What developers are solving | Representative projects | Main constraint |
| --- | --- | --- | --- |
| Out-of-core / SSD streamed MoE | Model exceeds host RAM or VRAM | [Edge0](https://github.com/Edge0-AI/Edge0), [Colibri](https://github.com/JustVugg/colibri), [MoE-Infinity](https://github.com/EfficientMoE/MoE-Infinity), [Betelgeuse](https://github.com/Betelgeuse-AI/Betelgeuse) | Storage capacity and **bytes read per token** |
| CPU/GPU hybrid | Partial model on accelerators plus host RAM | [KTransformers](https://github.com/kvcache-ai/ktransformers), [PowerInfer](https://github.com/Tiiny-AI/PowerInfer) | Host RAM, CPU ISA, PCIe bandwidth |
| Weight compression | Lower model weight footprint | [BitNet](https://github.com/microsoft/BitNet), [SqueezeLLM](https://github.com/SqueezeAILab/SqueezeLLM), [LLM Compressor](https://github.com/vllm-project/llm-compressor) | Format/model compatibility and quality trade-offs |
| Embedded / on-device | Small offline models on phones and tiny boards | [MNN](https://github.com/alibaba/MNN), [ExecuTorch](https://github.com/pytorch/executorch), [LiteRT](https://github.com/google-ai-edge/LiteRT), [PicoLM](https://github.com/RightNow-AI/picolm) | CPU/NPU acceleration, heat, battery, app footprint |
| Browser inference | Run model in user browser | [WebLLM](https://github.com/mlc-ai/web-llm) | WebGPU support, browser memory limits |
| Serving & context memory | High throughput, context windows, caching | [FlashAttention](https://github.com/Dao-AILab/flash-attention), [FlashInfer](https://github.com/flashinfer-ai/flashinfer), [vLLM](https://github.com/vllm-project/vllm) | GPU resource allocation and KV-cache utilization |
| Model-to-hardware discovery | Choose fit before downloading | [llmfit](https://github.com/AlexsJones/llmfit), [Local LLM Advisor](https://localllmadvisor.com/), [ModelFit](https://modelfit.io/) | Quality of estimators, model/quant version and measured evidence |

## Direct and adjacent competitors

- [awesome-local-llm](https://github.com/rafska/awesome-local-llm): broad local runtimes and resources. GitHub snapshot: **3,053 stars** on 2026-11-11.
- [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference): inference papers/code; **5,553 stars** on 2026-11-11. It centers research rather than constrained personal hardware.
- [awesome-mobile-llm](https://github.com/stevelaskaridis/awesome-mobile-llm): mobile and embedded research, with an October 2026 update; **417 stars** on 2026-11-11.
- [llmfit](https://github.com/AlexsJones/llmfit): automatically detects hardware, estimates model fit, and now supports contributor measurements. It already has a CLI, TUI and web dashboard. **Don't clone its model-recommender premise**.
- [Local LLM Advisor](https://localllmadvisor.com/), [ModelFit](https://modelfit.io/), [LocalLM Fit](https://locallmfit.com/): hardware/model fit calculators. Differentiate by **engine mechanism, source context, disk/flash use and evidence provenance**, not only a RAM slider.
- [Trendshift — LLM inference](https://trendshift.io/topics/llm-inference) and [GitHub topics](https://github.com/topics/llm-inference) provide discovery sources, not ground truth on performance.

## High-signal technical findings

1. **SSD streaming is feasibility, not an interaction-speed guarantee.** [kimi-k3-in-c](https://github.com/FareedKhan-dev/kimi-k3-in-c) reports 2.78T inference at ~8.24 GB RSS, but approximately **1.7 TB free storage** and **tens of seconds per token** on its documented low-memory configuration.
2. **Some tools need more RAM than their headline VRAM.** [Speedy](https://github.com/DevDock-AI/Speedy) advertises consumer 10 GB RTX cards yet its cited Q4-class setup uses **128 GB host RAM**; [MoE-Infinity](https://github.com/EfficientMoE/MoE-Infinity) suggests **16 GB VRAM** on a DeepSeek-Lite path.
3. **Bit-level compression is model-specific.** [BitNet](https://github.com/microsoft/BitNet) targets BitNet-trained models; it does not magically convert any arbitrary checkpoint into accurate 1.58-bit inference.
4. **KV-cache offload differs from weight offload.** [oMLX](https://github.com/jundot/omlx) caches prior context on SSD. This is not equivalent to fitting a model whose weight tensors exceed RAM.
5. **Mobile platforms are distinct.** [MNN](https://github.com/alibaba/MNN), [LiteRT](https://github.com/google-ai-edge/LiteRT), and [ExecuTorch](https://github.com/pytorch/executorch) operate in mobile deployment ecosystems; reports on flagship devices cannot be generalized to 4 GB entry phones.
6. **Cold/warm tests can invert perceived speed.** [Betelgeuse](https://github.com/Betelgeuse-AI/Betelgeuse) reports strong *warm-cache repeated-workload* throughput; those figures do not describe first-run cold SSD performance.

## Audience segments (hypotheses; not surveyed)

| Persona | Main question | Directory feature |
| --- | --- | --- |
| Developer with 8–16 GB laptop | "What can I run without freezing my PC?" | Source-labeled system RAM and true peak residency; measured decode/TTFT |
| Enthusiast with 8–24 GB VRAM | "Can I use my SSD and RAM for a larger model?" | Explicit VRAM **versus host RAM**, disk capacity and I/O warning |
| Phone developer | "Which runtime deploys efficiently on Android/iOS?" | Runtime/delegate compatibility, NPU/CPU, battery and thermal caveats |
| Local coding agent developer | "Will this remain responsive with long contexts?" | KV cache, 8K/32K/128K context tiers, TTFT and disk latency |
| Research engineer | "Can I reproduce the paper's result?" | Model hash, benchmark recipe, upstream data and independent replication level |

## Product gap & prioritized roadmap

- **P0: integrity and provenance.** Keep one source-of-truth JSON, validate external links, expose review dates, separate author-reported claims from reproduced results, and never infer min RAM from device RAM.
- **P1: side-by-side comparisons.** Display constraints, hardware configurations and caveats without implying that unlike-model tok/s are comparable. [Compare page](../docs/compare.html).
- **P2: reproducible benchmark intake.** Require model revision, quant, OS/device, system RAM, peak RSS, GPU VRAM, disk bytes, warm/cold, prompt/generation length and logs before publication.
- **P3: targeted hardware evidence.** Prioritize widely owned 4, 8, 16 and 32 GB host RAM systems; do not invent benchmark rows to fill gaps.
- **P4: community discovery.** Weekly review of new repos from Trendshift/GitHub, GitHub issue template for contribution, and a visible stale-data signal. No unverified automatic promotion.

## Ethical and practical constraints

There is no credible total-addressable-market estimate from this desk research, so **no revenue, growth, adoption or market-share projections** are presented. GitHub stars are discoverability proxies, not users or proof of reproducibility. Some upstream research code is experimental and could require caution with downloaded weights, scripts, or security boundaries. Individual projects retain their own licenses.

Last manual desk review: **2026-11-11**.
