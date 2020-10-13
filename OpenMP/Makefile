CC = g++
CFLAGS= -Wall -g -O3 -fopenmp
PRGS = contrast
OBJS = contrast-enhancement.cpp histogram-equalization.cpp  contrast.cpp
LIBS = -lm 

all:  $(PRGS)

$(PRGS): % :  %.cpp
	$(CC) $(CFLAGS) -o $@  $(OBJS) $(LDFLAGS) $(LIBS)

clean:
	rm -rf  *.o  *~ $(PRGS)
