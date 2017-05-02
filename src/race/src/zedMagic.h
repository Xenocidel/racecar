#ifndef CUDA_BLAH_BLAH
#define CUDA_BLAH_BLAH
#include <stdio.h>
#include <stdlib.h>
#include <vector>

#include "cuda.h"
#include "cuda_runtime.h"

#define W_I 1280
#define H_I 720
#define H_O 198
#define W_O 640

__global__
void saxpy(int n, float a, float *x, float *y);

extern "C" int testMain(void);

extern "C" std::vector<unsigned char> processImage(std::vector<unsigned char> imgData);



#endif

