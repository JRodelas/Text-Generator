#ifndef REQUEST_H
#define REQUEST_H

typedef enum {ALLOCATE, DEALLOCATE} RequestType;

typedef struct{
	RequestType type;
	int process_id;
	int num_units;
} Request;

Request generate_request_ff();
Request generate_request_bf();

#endif
