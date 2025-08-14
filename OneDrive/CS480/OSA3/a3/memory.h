#ifndef MEMORY_H
#define MEMORY_H

#define TOTAL_UNITS 128
#define UNIT_SIZE 2

typedef struct MemoryBlock{
	int start_unit;
	int size_units;
	int process_id;
	struct MemoryBlock *next;
} MemoryBlock;

MemoryBlock* init_memory();
void free_memory(MemoryBlock *head);

int allocate_mem_first_fit(MemoryBlock *head, int process_id, int num_units);
int allocate_mem_best_fit(MemoryBlock *head, int process_id, int num_units);
int deallocate_mem(MemoryBlock *head, int process_id);
int fragment_count(MemoryBlock *head);

#endif

