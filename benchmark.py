#!/usr/bin/env python3
"""
Автоматизация серии экспериментов.

Для каждого размера n:
  1. Генерирует тестовые данные (если их нет).
  2. Запускает решатель dot_product.
  3. Собирает время и результат.
Результаты сохраняются в results.csv.

Usage: python3 benchmark.py
"""
import subprocess
import os

SIZES = [100_000, 250_000, 500_000,
         1_000_000, 2_000_000, 4_000_000,
         8_000_000, 16_000_000]
EXE = "./dot_product"


def run_once(n):
    input_file  = f"input_{n}.txt"
    output_file = f"output_{n}.txt"

    if not os.path.exists(input_file):
        subprocess.run(["python3", "generate_data.py", str(n), input_file],
                       check=True)

    result = subprocess.run(
        [EXE, input_file, output_file],
        capture_output=True, text=True, check=True,
    )

    parts = dict(kv.split("=") for kv in result.stdout.strip().split())
    return {
        "n":       int(parts["n"]),
        "time_ms": float(parts["time_ms"]),
        "result":  float(parts["result"]),
    }


def main():
    rows = []
    print(f"{'n':>10} {'time_ms':>12} {'result':>22}")
    for n in SIZES:
        r = run_once(n)
        rows.append(r)
        print(f"{r['n']:>10} {r['time_ms']:>12.4f} {r['result']:>22.10f}")

    with open("results.csv", "w") as f:
        f.write("n,time_ms,result\n")
        for r in rows:
            f.write(f"{r['n']},{r['time_ms']},{r['result']}\n")

    print("\nSaved to results.csv")


if __name__ == "__main__":
    main()