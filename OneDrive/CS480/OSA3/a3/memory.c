#include <stdio.h>
#include <stdlib.h>
#include "memory.h"

/** 
 * Names:  
 * Salvador De La Torre - cssc1417
 * Jasmine Rodelas - cssc1454
 */

MemoryBlock* init_memory(){
    MemoryBlock *head = (MemoryBlock *)malloc(sizeof(MemoryBlock));
    if (!head) {
        perror("malloc");
        exit(1);
    }
    head->start_unit = 0;
    head->size_units = TOTAL_UNITS;
    head->process_id = -1;
    head->next = NULL;
    return head;
}

void free_memory(MemoryBlock *head){
    MemoryBlock *curr = head;
    while (curr){
        MemoryBlock *temp = curr;
        curr = curr->next;
        free(temp);
    }
}

int deallocate_mem(MemoryBlock *head, int pid) {
    MemoryBlock *curr = head, *prev = NULL;
    while (curr) {
        if (curr->process_id == pid) {
            curr->process_id = -1;

            // merge with next free
            if (curr->next && curr->next->process_id == -1) {
                MemoryBlock *next = curr->next;
                curr->size_units += next->size_units;
                curr->next = next->next;
                free(next);
            }

            // merge with prev free
            if (prev && prev->process_id == -1) {
                prev->size_units += curr->size_units;
                prev->next = curr->next;
                free(curr);
            }

            return 1;
        }
        prev = curr;
        curr = curr->next;
    }
    return -1;
}

int fragment_count(MemoryBlock *head) {
    int count = 0;
    MemoryBlock *curr = head;
    while (curr) {
        if (curr->process_id == -1 && (curr->size_units == 1 || curr->size_units == 2)) {
            count++;
        }
        curr = curr->next;
    }
    return count;
}
