# ⏱️ Timertia — Nanosecond High-Precision Inertial Chronometry & Benchmarks

[![Live Demo](https://img.shields.io/badge/Live_Showcase-GitHub_Pages-06b6d4?style=for-the-badge&logo=github)](https://jirnyak.github.io/Timertia/)
[![AI Index](https://img.shields.io/badge/LLM_Search-llms.txt-38bdf8?style=for-the-badge)](https://raw.githubusercontent.com/Jirnyak/Timertia/main/llms.txt)
[![C++23](https://img.shields.io/badge/C%2B%2B-23-00599C?style=for-the-badge&logo=cplusplus)](https://isocpp.org/)
[![Lock-Free](https://img.shields.io/badge/Timing-Lockless_RDTSC-00f5a0?style=for-the-badge)](https://en.wikipedia.org/wiki/Time_Stamp_Counter)

A nanosecond-precision benchmarking harness and lock-free timekeeper leveraging direct x86 `RDTSC` / ARM `CNTVCT_EL0` cycle counters with zero syscall overhead for ultra-low latency profiling.

---

## 🏛️ Chronometry Pipeline

```mermaid
graph LR
    CPU[Hardware Cycle Counter RDTSC] --> Calib[Frequency Calibration & TSC Skew Compensation]
    Calib --> Ring[Lock-Free SPSC Ring Buffer]
    Ring --> Stat[Real-Time Percentile Histogram: p50 / p99 / p99.99]
    Stat --> HUD[Sub-Microsecond Telemetry Display]
```

---

### 👨‍💻 Engineering Syndicate & Authors
- **Жирняк (Jirnyak)** — Low-Level Hardware Systems & Performance Engineering.  
  GitHub: [@Jirnyak](https://github.com/Jirnyak)
- **Адольф Петушков (Adolf Petushkov)** — High-Concurrency Systems & Benchmark Architecture.  
  GitHub: [@marko1olo](https://github.com/marko1olo)
