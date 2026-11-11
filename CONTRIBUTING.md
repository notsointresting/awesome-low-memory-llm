# Contributing

Thanks for improving this hardware-first LLM resource. Contributions are welcome through issues and pull requests.

## What belongs here?

Include open-source inference runtimes, compression/offloading techniques, reference implementations, model formats, and reproducible learning resources with a direct connection to local or memory-efficient LLM execution.

We favor maintained projects with transparent source code, clear documentation, and a usable license. A research implementation may still be included when clearly labeled.

## Submitting a project

1. Search the README and existing issues for duplicates.
2. Link the project's **official repository** and describe its memory-saving mechanism in one factual sentence.
3. Identify supported hardware, model families, and limitations **only when documented**.
4. Add it in alphabetical or thematic order to README and to `data/projects.json` when appropriate.
5. Run `python scripts/validate.py` locally before submitting a PR.

Do not claim minimum RAM, benchmarks, rankings, or platform support without a clear source and experimental conditions. Prefer links to original documentation over marketing pages. Avoid referral and affiliate links, paid placement, and promotional language.

## Benchmark submissions

Follow `BENCHMARKS.md`. Provide logs/commands where possible; disclose whether results are independently reproduced, author-reported, or community-reported. Do not compare dense vs. MoE parameter totals as though they have identical compute costs.

## Community standards

Be respectful and constructive. See `CODE_OF_CONDUCT.md`. Maintainers may edit descriptions for consistency and reject unrelated or misleading submissions.

## Community benchmark submissions

Visit the [Benchmark Lab](docs/benchmark-lab.html) for a reproducible `llama-bench` command and [BENCHMARKS.md](BENCHMARKS.md) for methodology. Candidate JSON is not an accepted or independently reproduced benchmark: maintainers review model source/revision, quantization, hardware, repeat samples, logs, and source of measured RAM/VRAM before manually adding records to `data/community-benchmarks.json`.

Do not publish usernames, hostnames, absolute private paths, access tokens or confidential prompts in logs. CPU/GPU strings and model filenames are potentially identifying and should be reviewed before sharing.
