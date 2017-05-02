#include <stdio.h>
#include "cuda.h"
#include "cuda_runtime.h"
#include "zedMagic.h"
#define square(x) x*x
#define THRESHOLD 70




__global__
void saxpy(int n, float a, float *x, float *y) {
    int i=blockIdx.x*blockDim.x + threadIdx.x;
    if (i<n) y[i]=a*x[i]+y[i];
}

extern "C" int testMain(void) {
    int N=30000;//1<<20;
    float *x, *y, *d_x, *d_y;
    
    x=(float*)malloc(N*sizeof(float));
    y=(float*)malloc(N*sizeof(float));

    cudaMalloc(&d_x, N*sizeof(float));
    cudaMalloc(&d_y, N*sizeof(float));
    
    for (int i=0;i<N;i++) {
        x[i]=1.0f;
        y[i]=2.0f;  
    }

    cudaMemcpy(d_x,x,N*sizeof(float),cudaMemcpyHostToDevice);
    cudaMemcpy(d_y,y,N*sizeof(float),cudaMemcpyHostToDevice);


    saxpy<<<(N+255)/256, 256>>>(N,2.0f,d_x,d_y);

    cudaMemcpy(y,d_y,N*sizeof(float),cudaMemcpyDeviceToHost);

    float maxError=0.0f;
    for (int i=0;i<N;i++) 
        maxError=max(maxError,abs(y[i]-4.0f));

    cudaFree(d_x);
    cudaFree(d_y);
    free(x);
    free(y);
    return 0;
}


extern "C" std::vector<unsigned char> processImage(std::vector<unsigned char> imgData) {
    // Steps:
    // Read from std::vector format
    // Crop and scale
    // Grayscale    
    // Edge/SGM
    // Black and white
    // Return to std::vector format

    //Reading into an array AND cropping AND scaling at once
    unsigned char *scCrop,*d_scCrop;
    std::vector<unsigned char> output; 

    scCrop = (unsigned char*) malloc(3*H_O*W_O*sizeof(unsigned char));
    cudaMalloc(&d_scCrop,3*H_O*W_O*sizeof(unsigned char));
    
    printf("allocated mem\n");
    if (scCrop==NULL) printf("Error allocating memory: allocated to NULL\n");

    int i,j;
    int W = W_I, H = H_I;
    int cropH=H*55/100;
    int newH=cropH/2;
    int newW=W/2;

    if (imgData.size() != W*H*3) {
        printf("ERROR dimensions wahwahwah\n");
    } 

    for (i=0;i<H_O;i++) {
        for (j=0;j<W_O*3;j++) {
            long sum=0;
            sum=sum+imgData[(2*j)   + 3*W*(2*i)  ];
            sum=sum+imgData[(2*j+3) + 3*W*(2*i)  ];
            sum=sum+imgData[(2*j)   + 3*W*(2*i+1)];
            sum=sum+imgData[(2*j+3) + 3*W*(2*i+1)];
            scCrop[i*W_O*3 + j] = (sum/4);
        }
    }

    printf("scaled and cropped into array\n");


    for (i=0;i<H_O;i++) {
        for (j=0;j<W_O*3;j++) {
            output.push_back(scCrop[i*W_O*3 + j]);
        }
    }

    printf("read from array into vector\n");

    free(scCrop);
    cudaFree(d_scCrop);

    std::vector <unsigned char> scaled; //to scale down image

    /*
    scaled = scaleAndCrop(imgData);
    * OR
    */

    scaled = output;
    
    std::vector <unsigned char> bw; // to hold raw bw
    
    bw = toGrayscale(scaled);

    
    std::vector <unsigned char> edges; // to hold scaled, thresholded sgm 
    edges = getEdges(bw);

    return edges;

}



