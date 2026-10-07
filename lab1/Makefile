CXX      ?= c++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra
TARGET   := dot_product

all: $(TARGET)

$(TARGET): dot_product.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGET) *.o input_*.txt output_*.txt results.csv

.PHONY: all clean
