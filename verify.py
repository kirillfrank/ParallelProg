#!/usr/bin/env python3
"""
Верификация результата скалярного произведения через NumPy (BLAS).

Сравниваем вычисленное значение с numpy.dot. Критерий прохождения —
относительная ошибка меньше 1e-4.

Usage: python3 verify.py <input_file> <output_file>
"""
import sys
import numpy as np


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file) as f:
        n = int(f.readline())
        a = np.array([float(f.readline()) for _ in range(n)])
        b = np.array([float(f.readline()) for _ in range(n)])

    with open(output_file) as f:
        computed = float(f.readline())

    reference = float(np.dot(a, b))
    rel_err = abs(computed - reference) / max(abs(reference), 1e-15)

    print(f"Computed  : {computed:.15e}")
    print(f"Reference : {reference:.15e}")
    print(f"Relative error: {rel_err:.3e}")

    if rel_err < 1e-4:
        print("VERIFICATION: OK")
        sys.exit(0)
    else:
        print("VERIFICATION: FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()