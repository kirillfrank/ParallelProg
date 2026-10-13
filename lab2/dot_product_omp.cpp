// Лабораторная работа №2. Скалярное произведение векторов
// (параллельная версия на OpenMP)
//
// Дисциплина: Параллельное программирование
// Автор: Франк Кирилл, 6213-100503D
// Дата: 21.10.2026

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <omp.h>

using Vector = std::vector<double>;

// ---------- Чтение векторов ----------
void read_vectors(const std::string& filename, Vector& a, Vector& b) {
    std::ifstream in(filename);
    if (!in) {
        std::cerr << "Cannot open file: " << filename << "\n";
        std::exit(1);
    }
    size_t n;
    in >> n;
    a.resize(n);
    b.resize(n);
    for (size_t i = 0; i < n; ++i) in >> a[i];
    for (size_t i = 0; i < n; ++i) in >> b[i];
}

// ---------- Параллельное скалярное произведение ----------
// OpenMP reduction автоматически собирает частичные суммы
double dot_omp(const Vector& a, const Vector& b) {
    double s = 0.0;
    const long long n = static_cast<long long>(a.size());
    #pragma omp parallel for reduction(+:s) schedule(static)
    for (long long i = 0; i < n; ++i) {
        s += a[i] * b[i];
    }
    return s;
}

int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " <input_file> <output_file> <num_threads>\n";
        return 1;
    }
    const std::string input_file  = argv[1];
    const std::string output_file = argv[2];
    const int num_threads = std::atoi(argv[3]);

    omp_set_num_threads(num_threads);

    // Чтение
    Vector a, b;
    read_vectors(input_file, a, b);
    const size_t n = a.size();

    // Замер
    double t0 = omp_get_wtime();
    const double result = dot_omp(a, b);
    double t1 = omp_get_wtime();

    const double ms = (t1 - t0) * 1000.0;

    // Запись результата
    std::ofstream out(output_file);
    out.precision(17);
    out << result << "\n";
    out.close();

    // Диагностика (парсится benchmark_omp.py)
    std::cout << "n="       << n
              << " threads=" << num_threads
              << " time_ms=" << ms
              << " result="  << result
              << "\n";

    return 0;
}
