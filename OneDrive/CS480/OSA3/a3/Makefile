CC = gcc
CFLAGS = -Wall -Wextra -std=c11

OBJS = main.o memory.o request.o first_fit.o best_fit.o 

all: sim
sim: $(OBJS)
	$(CC) $(CFLAGS) -o sim $(OBJS)

main.o: main.c memory.h request.h
memory.o: memory.c memory.h
request.o: request.c request.h
first_fit.o: first_fit.c memory.h
best_fit.o: best_fit.c memory.h

clean:
	rm -f *.o sim