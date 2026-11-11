# Hardware research additions — 2026-11-11

Sources are upstream GitHub READMEs and repository metadata checked on 2026-11-11. **We did not run these projects or reproduce benchmark claims.** Use [BENCHMARKS.md](../BENCHMARKS.md) to understand evidence levels.

| Project | Mechanism | Source-reported hardware / performance | Limitations |
| --- | --- | --- | --- |
| [Strata](https://github.com/Niko1221/Strata) | SSD-assisted local inference and model-hosting APIs | Authors list RTX 5070 12 GB GPU + 64 GB RAM at 4–6 tok/s on a selected DeepSeek Flash test | Model-dependent memory and large SSD needs |
| [FreeToken](https://github.com/flashml-org/freetoken) | Heterogeneous MoE expert caching and elastic VRAM allocation | Source describes Windows/Linux consumer GPU support, no universal minimum memory | Not necessarily usable on sub-8 GB RAM devices; benchmark comparability unverified |
| [PicoLM](https://github.com/RightNow-AI/picolm) | Minimal C inference with mmap layer-by-layer model access | Project reports ~45 MB runtime RAM, ~638 MB disk model, ~10 tok/s on Raspberry Pi 5 | Exact memory semantics and different board configurations require reproduction; last push Feb 2026 |
| [oMLX](https://github.com/jundot/omlx) | Apple Silicon server with SSD-backed KV caching | macOS 15+, Apple Silicon; documentation includes memory limits and caching modes | Disk KV cache ≠ streaming arbitrary model weights beyond RAM |
| [BigMoeOnEdge](https://github.com/Helldez/BigMoeOnEdge) | Bounded-memory streaming MoE experts from flash via llama.cpp | Author reports ~1 tok/s with a 284B/91 GB disk model on a 12 GB Android phone; ~5 tok/s for 35B/21 GB on a 16 GB Windows laptop | Model occupies full storage footprint; strong reliance on I/O performance |
| [Low-Spec Coding LLM Setup](https://github.com/Yasvanth-S/local-coding-llm-low-spec-setup) | Reproducible llama.cpp + aider deployment recipe | On Ryzen 5 5600H / GTX 1650 4 GB / 6.6 GiB RAM, source reports Qwen3.5-4B Q4_K_M at 37.7 tok/s | Text-only benchmark; adding vision or larger context can trigger OOM |

## Data provenance

`data/projects.json` contains `profile.reports` with separate fields for **tested system RAM**, **peak resident RAM**, **GPU VRAM**, **disk footprint**, and **decode speed** where supported by the original README. These are never combined into a fictional “minimum RAM” metric. All reported numeric examples retain a URL to the original documentation. Absence of a benchmark means **unknown**, not **incompatible**.

The `supastishn/edgeMoE` repository's own README points to `Helldez/BigMoeOnEdge` for releases and status badges. This catalog preserves the historical reference while highlighting the apparently current upstream.

This evidence is a dated snapshot, not continuous monitoring or a security endorsement.
