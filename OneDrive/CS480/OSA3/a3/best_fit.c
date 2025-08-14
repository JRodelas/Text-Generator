#include <stdlib.h>
#include "memory.h"

// Allocate memory using Best Fit strategy
int allocate_mem_best_fit(MemoryBlock *head, int pid, int units) {
    MemoryBlock *curr = head;
    MemoryBlock *best = NULL;
    int best_nodes = 0;
    int nodes_traversed = 0;

    while (curr) {
        nodes_traversed++;
        if (curr->process_id == -1 && curr->size_units >= units) {
            if (!best || curr->size_units < best->size_units) {
                best = curr;
                best_nodes = nodes_traversed;
            }
        }
        curr = curr->next;
    }

    if (!best) return -1;

    if (best->size_units == units) {
        best->process_id = pid;
    } else {
        MemoryBlock *new_block = (MemoryBlock *)malloc(sizeof(MemoryBlock));
        if (!new_block) return -1;

        new_block->start_unit = best->start_unit + units;
        new_block->size_units = best->size_units - units;
        new_block->process_id = -1;
        new_block->next = best->next;

        best->size_units = units;
        best->process_id = pid;
        best->next = new_block;
    }

    return best_nodes;
}
