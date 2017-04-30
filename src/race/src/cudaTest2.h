#ifndef CUDA_BLAH_BLAH
#define CUDA_BLAH_BLAH
#include <stdio.h>
#include "cuda.h"
#include "cuda_runtime.h"

__global__
void saxpy(int n, float a, float *x, float *y);

extern "C" int testMain(void);

#endif

