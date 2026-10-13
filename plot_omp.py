#!/usr/bin/env python3
"""Графики: время, ускорение, GFLOPS от числа потоков. Usage: python3 plot_omp.py"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_results(path="results.csv"):
    data = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            n = int(row["n"]); t = int(row["threads"])
            data.setdefault(n, {})[t] = {
                "time_ms": float(row["time_ms"]),
                "gflops":  float(row["gflops"]),
            }
    return data


def main():
    data = load_results()

    # ---- График 1: время от числа потоков ----
    plt.figure(figsize=(9, 5))
    for n, series in sorted(data.items()):
        ts = sorted(series.keys())
        ys = [series[t]["time_ms"] for t in ts]
        plt.plot(ts, ys, "o-", label=f"n = {n:,}", linewidth=2, markersize=6)
    plt.xlabel("Число потоков", fontsize=12)
    plt.ylabel("Время, мс", fontsize=12)
    plt.title("Время выполнения от числа потоков", fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig("time.png", dpi=150)
    plt.close()
    print("Saved: time.png")

    # ---- График 2: ускорение (speedup) ----
    plt.figure(figsize=(9, 5))
    for n, series in sorted(data.items()):
        ts = sorted(series.keys())
        if 1 not in series:
            continue
        t1 = series[1]["time_ms"]
        speedup = [t1 / series[t]["time_ms"] for t in ts]
        plt.plot(ts, speedup, "s-", label=f"n = {n:,}", linewidth=2, markersize=6)
    # идеальное ускорение
    max_t = max(max(s.keys()) for s in data.values())
    plt.plot([1, max_t], [1, max_t], "k--", alpha=0.5, label="Идеальное")
    plt.xlabel("Число потоков", fontsize=12)
    plt.ylabel("Ускорение (Speedup)", fontsize=12)
    plt.title("Ускорение относительно 1 потока", fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig("speedup.png", dpi=150)
    plt.close()
    print("Saved: speedup.png")

    # ---- График 3: GFLOPS ----
    plt.figure(figsize=(9, 5))
    for n, series in sorted(data.items()):
        ts = sorted(series.keys())
        ys = [series[t]["gflops"] for t in ts]
        plt.plot(ts, ys, "^-", label=f"n = {n:,}", linewidth=2, markersize=6)
    plt.xlabel("Число потоков", fontsize=12)
    plt.ylabel("Производительность, GFLOPS", fontsize=12)
    plt.title("Производительность (GFLOPS) от числа потоков", fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig("gflops.png", dpi=150)
    plt.close()
    print("Saved: gflops.png")


if __name__ == "__main__":
    main()