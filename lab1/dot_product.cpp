// Лабораторная работа №1. Скалярное произведение двух векторов
//
// Дисциплина: Параллельное программирование
// Автор: (Франк Кирилл, 6213-100503D)
// Дата: (14.09.2026)

#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <cstdlib>

using Vector = std::vector<double>;

// ---------- Чтение двух векторов из файла ----------
// Формат: первая строка — n,
// далее n строк с элементами вектора a,
// далее n строк с элементами вектора b.
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

// ---------- Скалярное произведение ----------
// Основной вычислительный цикл алгоритма: O(n).
// Именно он будет распараллелен в лабораторной работе №2 (OpenMP).
double dot(const Vector& a, const Vector& b) {
    double s = 0.0;
    const size_t n = a.size();
    for (size_t i = 0; i < n; ++i) {
        s += a[i] * b[i];
    }
    return s;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0]
            << " <input_file> <output_file>\n";
        return 1;
    }
    const std::string input_file = argv[1];
    const std::string output_file = argv[2];

    // 1. Чтение векторов
    Vector a, b;
    read_vectors(input_file, a, b);
    const size_t n = a.size();

    // 2. Замер времени стартует непосредственно перед основным циклом
    auto t0 = std::chrono::high_resolution_clock::now();

    const double result = dot(a, b);

    auto t1 = std::chrono::high_resolution_clock::now();
    const double ms =
        std::chrono::duration<double, std::milli>(t1 - t0).count();

    // 3. Запись результата
    std::ofstream out(output_file);
    out.precision(17);
    out << result << "\n";
    out.close();

    // 4. Диагностика в stdout (парсится benchmark.py)
    std::cout << "n=" << n
        << " time_ms=" << ms
        << " result=" << result
        << "\n";

    return 0;
}
