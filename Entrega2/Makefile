CXX = g++
CXXFLAGS = -std=c++11 -O3 -Wall
LDFLAGS = -lm

TARGET = e2.o
SRC = e2.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	@$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)


clean:
	@rm -f $(TARGET)