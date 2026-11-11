# Benchmark methodology

**No benchmark measurements are shipped at launch.** Entries are added only when supporting evidence and experimental settings are available.

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
