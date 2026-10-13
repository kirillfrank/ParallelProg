CXX      ?= g++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra -fopenmp
TARGET   := dot_product_omp

all: $(TARGET)

$(TARGET): dot_product_omp.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGET) *.o input_*.txt output_*.txt results.csv *.png

.PHONY: all clean
