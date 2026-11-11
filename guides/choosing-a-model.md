# Choosing a model for limited memory

1. **Define the task** (chat, coding, multilingual, retrieval, vision). Model quality matters as much as size.
2. **Check the license** of the model and its redistribution/commercial-use constraints.
3. **Understand weight footprint**: weight precision, format metadata, and tensor overhead affect disk and resident memory.
4. **Budget beyond weights**: KV cache grows with context length; runtime, activations, operating system, and other programs also consume memory.
5. **Distinguish RAM, VRAM, and storage**: hybrid execution and SSD-streamed models may fit in RAM while requiring substantially more disk or running slower.
6. **Match model format to runtime**: GGUF, GPTQ, AWQ, MLX, and other formats are not interchangeable by default.
7. **Benchmark your workload**: record first-token latency, prompt processing, and generation throughput with an actual prompt/context size.

Start with a smaller supported model, then work up while monitoring system stability, thermals, and memory usage. No universal RAM cutoff guarantees a given model will run well.
