#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "memory.h"
#include "request.h"

#define NUM_REQUESTS 10000 // total num of requests in the simulation
#define REPORT_INTERVAL 100 // Intervals to record performance for CSV file

/** 
 * Names:  
 * Salvador De La Torre - cssc1417
 * Jasmine Rodelas - cssc1454
 */

int main() {
    srand(time(NULL));

    // Open CSV file for writing performance data to graph later on
    FILE *csv_file = fopen("performance.csv", "w");
    if (!csv_file) {
        perror("Error opening performance.csv");
        return 1;
    }

	//Header to read performance data from csv
    fprintf(csv_file, "Step,FF_Fragments,FF_Nodes,FF_Denial,BF_Fragments,BF_Nodes,BF_Denial\n");

    // Memory systems
    MemoryBlock *mem_first = init_memory();
    MemoryBlock *mem_best = init_memory();

    // Stats for First Fit
	int ff_denied = 0;
    int ff_allocations = 0;
    int ff_total_fragments = 0;
    int ff_total_nodes = 0;
    

    // Stats for Best Fit
    int bf_total_fragments = 0;
    int bf_allocations = 0;
	int bf_total_nodes = 0;
    int bf_denied = 0;

    // Simulation loop to generate the requests
    for (int i = 0; i < NUM_REQUESTS; i++) {
        Request req_ff = generate_request_ff();
        Request req_bf = generate_request_bf();

        // First fit algorithm
        if (req_ff.type == ALLOCATE) {
            int nodes_ff = allocate_mem_first_fit(mem_first, req_ff.process_id, req_ff.num_units);
            if (nodes_ff == -1) {
                ff_denied++;
            } else {
                ff_total_nodes += nodes_ff;
                ff_allocations++;
            }
        } else {
            deallocate_mem(mem_first, req_ff.process_id);
        }

        // Best fit algorithm
        if (req_bf.type == ALLOCATE) {
            int nodes_bf = allocate_mem_best_fit(mem_best, req_bf.process_id, req_bf.num_units);
            if (nodes_bf == -1) {
                bf_denied++;
            } else {
                bf_total_nodes += nodes_bf;
                bf_allocations++;
            }
        } else {
            deallocate_mem(mem_best, req_bf.process_id);
        }

        // Fragment stats
        ff_total_fragments += fragment_count(mem_first);
        bf_total_fragments += fragment_count(mem_best);

        // Write performance data every REPORT_INTERVAL to CSV for python script to use
        if ((i + 1) % REPORT_INTERVAL == 0) {
            fprintf(csv_file, "%d,", i + 1);
            fprintf(csv_file, "%.4f,%.4f,%.4f,", 
                ff_total_fragments / (float)(i + 1),
                ff_allocations > 0 ? ff_total_nodes / (float)ff_allocations : 0,
                100.0 * ff_denied / (float)(i + 1));
            fprintf(csv_file, "%.4f,%.4f,%.4f\n", 
                bf_total_fragments / (float)(i + 1),
                bf_allocations > 0 ? bf_total_nodes / (float)bf_allocations : 0,
                100.0 * bf_denied / (float)(i + 1));
        }
    }

    // Close CSV file after loop is done writing
    fclose(csv_file);

    // First fit output text
    printf("End of First Fit Allocation\n");
    printf("Average External Fragments Each Request: %.6f\n", 
           ff_total_fragments / (float)NUM_REQUESTS);
    printf("Average Nodes Transversed Each Allocation: %.6f\n", 
           ff_allocations > 0 ? (ff_total_nodes / (float)ff_allocations) : 0);
    printf("Percentage Allocation Requests Denied Overall: %.6f%%\n",
           100.0 * ff_denied / (float)NUM_REQUESTS);

    // Best fit output text
    printf("End of Best Fit Allocation\n");
    printf("Average External Fragments Each Request: %.6f\n", 
           bf_total_fragments / (float)NUM_REQUESTS);
    printf("Average Nodes Transversed Each Allocation: %.6f\n", 
           bf_allocations > 0 ? (bf_total_nodes / (float)bf_allocations) : 0);
    printf("Percentage Allocation Requests Denied Overall: %.6f%%\n",
           100.0 * bf_denied / (float)NUM_REQUESTS);

    // Free up the memory
    free_memory(mem_first);
    free_memory(mem_best);

    return 0;
}
