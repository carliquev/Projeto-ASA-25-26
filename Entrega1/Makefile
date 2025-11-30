CXX = g++
CXXFLAGS = -std=c++11 -O3 -Wall
LDFLAGS = -lm

TARGET = e1.o
SRC = e1.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	@$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

clean:
	@rm -f $(TARGET)
