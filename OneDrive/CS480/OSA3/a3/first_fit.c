#include <stdlib.h>
#include "memory.h"

// Allocate memory using First Fit strategy
int allocate_mem_first_fit(MemoryBlock *head, int pid, int units) {
    MemoryBlock *curr = head;
    int nodes_traversed = 0;

    while (curr) {
        nodes_traversed++;
        if (curr->process_id == -1 && curr->size_units >= units) {
            if (curr->size_units == units) {
                curr->process_id = pid;
            } else {
                MemoryBlock *new_block = (MemoryBlock *)malloc(sizeof(MemoryBlock));
                if (!new_block) return -1;

                new_block->start_unit = curr->start_unit + units;
                new_block->size_units = curr->size_units - units;
                new_block->process_id = -1;
                new_block->next = curr->next;

                curr->size_units = units;
                curr->process_id = pid;
                curr->next = new_block;
            }
            return nodes_traversed;
        }
        curr = curr->next;
    }
    return -1;
}
