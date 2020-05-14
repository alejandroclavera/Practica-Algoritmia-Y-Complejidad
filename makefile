# the compiler: gcc for C program, define as g++ for C++
CC = gcc

# compiler flags:
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -shared -fPIC

# the build target executable:
TARGET = alineamiento

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o library/$(TARGET).so $(TARGET).c

clean:
	$(RM) $(TARGET)
