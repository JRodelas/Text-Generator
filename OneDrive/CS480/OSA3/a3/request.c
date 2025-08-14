#include <stdlib.h>
#include "request.h"

#define MIN_UNITS 3
#define MAX_UNITS 10
#define MAX_PROCESSES 5000

/** 
 * Names:  
 * Salvador De La Torre - cssc1417
 * Jasmine Rodelas - cssc1454
 */

// Separate tracking arrays
static int allocated_ff[MAX_PROCESSES] = {0}; // First fit
static int allocated_bf[MAX_PROCESSES] = {0}; //Best fit

//Generates next request for first fit strategy
Request generate_request_ff() {
	Request req;
	int pid = rand() % MAX_PROCESSES;
	if (allocated_ff[pid]) {
		// If theres already memory then do deallocation request
		req.type = DEALLOCATE;
		req.process_id = pid;
		req.num_units = 0;
		allocated_ff[pid] = 0;
	} else {
		req.type = ALLOCATE;
		req.process_id = pid;
		req.num_units = MIN_UNITS + rand() % (MAX_UNITS - MIN_UNITS + 1);
		allocated_ff[pid] = 1;
	}
	return req;
}

//Generates next request for best fit strategy
Request generate_request_bf() {
	Request req;
	int pid = rand() % MAX_PROCESSES;
	if (allocated_bf[pid]) {
		// If theres already memory then do deallocation request
		req.type = DEALLOCATE;
		req.process_id = pid;
		req.num_units = 0;
		allocated_bf[pid] = 0;
	} else {
		// If there's no memory, then create allocation request
		req.type = ALLOCATE;
		req.process_id = pid;
		req.num_units = MIN_UNITS + rand() % (MAX_UNITS - MIN_UNITS + 1);
		allocated_bf[pid] = 1;
	}
	return req;
}
