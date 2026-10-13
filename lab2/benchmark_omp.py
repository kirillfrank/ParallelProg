#!/usr/bin/env python3
"""
Параллельный benchmark: скалярное произведение на OpenMP.

Запускает решатель для каждого (n, threads) с усреднением по 5 запускам.
Считает GFLOPS = 2·n / (time_s · 1e9).
Результаты сохраняются в results.csv.

Usage: python3 benchmark_omp.py
"""
import subprocess
import os
import csv

SIZES   = [1_000_000, 2_000_000, 4_000_000, 8_000_000, 16_000_000, 32_000_000]
THREADS = [1, 2, 4, 6, 8]
REPS    = 5
EXE     = "./dot_product_omp"


def run_once(n, threads):
    input_file  = f"input_{n}.txt"
    output_file = f"output_{n}_{threads}.txt"

    if not os.path.exists(input_file):
        subprocess.run(["python3", "generate_data.py", str(n), input_file],
                       check=True)

    times = []
    result_val = 0.0
    for _ in range(REPS):
        proc = subprocess.run(
            [EXE, input_file, output_file, str(threads)],
            capture_output=True, text=True, check=True,
        )
        parts = dict(kv.split("=") for kv in proc.stdout.strip().split())
        times.append(float(parts["time_ms"]))
        result_val = float(parts["result"])

    return {
        "n":       n,
        "threads": threads,
        "time_ms": min(times),   # берём лучший из REPS
        "result":  result_val,
    }


def main():
    rows = []
    print(f"{'n':>10} {'threads':>8} {'time_ms':>12} "
          f"{'GFLOPS':>10} {'result':>22}")
    for n in SIZES:
        for t in THREADS:
            r = run_once(n, t)
            r["gflops"] = 2.0 * n / (r["time_ms"] / 1000.0) / 1e9
            rows.append(r)
            print(f"{r['n']:>10} {r['threads']:>8} "
                  f"{r['time_ms']:>12.4f} {r['gflops']:>10.3f} "
                  f"{r['result']:>22.10f}")

    with open("results.csv", "w") as f:
        f.write("n,threads,time_ms,gflops,result\n")
        for r in rows:
            f.write(f"{r['n']},{r['threads']},{r['time_ms']},"
                    f"{r['gflops']},{r['result']}\n")

    print("\nSaved to results.csv")


if __name__ == "__main__":
    main()
