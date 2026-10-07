#!/usr/bin/env python3
"""
Генератор тестовых векторов для задачи скалярного произведения.

Каждый вектор заполняется случайными числами из [-1, 1].
Размер n задаётся первым аргументом командной строки.

Usage: python3 generate_data.py <n> <output_file>
"""
import sys
import numpy as np


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <n> <output_file>")
        sys.exit(1)

    n = int(sys.argv[1])
    output_file = sys.argv[2]

    rng = np.random.default_rng(seed=42)
    a = rng.uniform(-1.0, 1.0, size=n)
    b = rng.uniform(-1.0, 1.0, size=n)

    with open(output_file, "w") as f:
        f.write(f"{n}\n")
        for x in a:
            f.write(f"{x:.17g}\n")
        for x in b:
            f.write(f"{x:.17g}\n")

    print(f"Generated vectors n={n} -> {output_file}")


if __name__ == "__main__":
    main()