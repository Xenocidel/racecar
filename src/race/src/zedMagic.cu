#include <stdio.h>
#include "cuda.h"
#include "cuda_runtime.h"
#include "zedMagic.h"
#define square(x) x*x
#define THRESHOLD 70

#define AREA H_O*W_O


__global__
void saxpy(int n, float a, float *x, float *y) {
    int i=blockIdx.x*blockDim.x + threadIdx.x;
    if (i<n) y[i]=a*x[i]+y[i];
}

__global__
void edgeMath(unsigned char* bw, float* edges) {
    int index = blockIdx.x*blockDim.x + threadIdx.x;
    int i = index/W_O;
    int j = index%W_O;
    if (i==0 || i==H_O-1) edges[index] = 0;
    else {
        if (j==0 || j==W_O-1) edges[index] = 0;
        else {
            int dx,dy;
            int newW = W_O;
                dx = bw[index+newW+1] + 2*bw[index+1] + bw[index-newW+1] \
                - (bw[index+newW-1] + 2*bw[index-1] + bw[index-newW-1]);
                dy = bw[index-newW-1] + 2*bw[index-newW] + bw[index-newW+1]\
                - (bw[index+newW-1] + 2*bw[index+newW] + bw[index+newW+1]);
                double sgm = (square(dx) + square(dy));
            edges[index] = sgm;
        }
    }
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

extern "C" std::vector<unsigned char> processImage(std::vector<unsigned char> imgData, int func_id) {
    switch(func_id) {
        case CUDA_BASIC: return processImageCuda(imgData);
        case DUMB: return processImageDumb(imgData);
        case DUMB_MIN: return processImageDumb(imgData);
    } return processImageCuda(imgData);
} 


extern "C" std::vector<unsigned char> processImageCuda(std::vector<unsigned char> imgData) {
    // Steps:
    // Read from std::vector format
    // Crop and scale
    // Grayscale    
    // Edge/SGM
    // Black and white
    // Return to std::vector format

    //Reading into an array AND cropping AND scaling at once
    unsigned char *scCrop,*d_scCrop;
    float  *edge,*d_edge;
    std::vector<unsigned char> output; 

    scCrop = (unsigned char*) malloc(AREA*sizeof(unsigned char));
    edge = (float*) malloc(AREA*sizeof(float));
    cudaMalloc(&d_scCrop,AREA*sizeof(unsigned char));
    cudaMalloc(&d_edge,AREA*sizeof(float));
    
    int i,j;
    int W = W_I, H = H_I;

    if (imgData.size() != W*H*3) {
        printf("ERROR dimensions wahwahwah\n");
    } 

    for (i=0;i<H_O;i++) {
        for (j=0;j<W_O;j++) {
            long sum = 0;
            for (int k = 0; k<6; k++) {
                sum += imgData[6*j + k + 6*W*i];
                sum += imgData[6*j + k + 6*W*i + 3*W];
            }
            scCrop[i*W_O + j] = sum/12;
        }
    } //scaled and cropped into array

    cudaMemcpy(d_scCrop,scCrop,AREA*sizeof(unsigned char),cudaMemcpyHostToDevice);
    edgeMath<<<W_O,H_O>>>(d_scCrop,d_edge);
    cudaMemcpy(edge,d_edge,AREA*sizeof(float),cudaMemcpyDeviceToHost);

    double max;
    for (i=0;i<H_O;i++) for (j=0;j<W_O;j++) max = (sqrt(edge[i*W_O + j])>max)? sqrt(edge[i*W_O + j]) : max;
 
    for (i=0;i<H_O;i++) for (j=0;j<W_O;j++) output.push_back( (sqrt(edge[i*W_O + j])/max*255 > THRESHOLD)? 255: 0);


    free(scCrop);
    cudaFree(d_scCrop);
    free(edge);
    cudaFree(d_edge);

    return output;

}

extern "C" std::vector<unsigned char> processImageDumb(std::vector<unsigned char> imgData) {
    std::vector <unsigned char> output;
    output = scaleAndCrop(imgData);
    output = toGrayscale(output);
    output = getEdges(output);
    return output;
}

extern "C" std::vector<unsigned char> processImageMin(std::vector<unsigned char> imgData) {
    std::vector <unsigned char> output;
    output = scaleCropGrayscale(imgData);
    output = getEdges(output);
    return output;
}




#ifdef INPROGRESS
__global__
void findHough(unsigned char* edge, unsigned char* temp) {
    int index = blockIdx.x*blockDim.x + threadIdx.x;
    int i = index/W_O;
    int j = index%W_O;
    int x = j;
    int y = newH -1 -i;
    if (edge[index]) {
                
    }

}


void blah() {
    
  for (i=0;i<newH;i++) {
        for (j=0;j<newW;j++) {
            int x,y;
            x = j;
            y = newH - 1 - i;
            int index = newW*i + j;
            if (edge_img[index]) {
                for (theta=0;theta<180;theta++) {
                    roh = -x*sin(theta*M_PI/180) + y*cos(theta*M_PI/180);
                    roh_min = (roh_min>roh)? roh: roh_min;
                    roh_max = (roh_max<roh)? roh: roh_max;
                    voting[theta].push_back(roh);    
                }
            } 
        }
    }

    int hough_max = 0;
    int final_r, final_t;
    for (theta=0;theta<180;theta++) {
        for (roh=roh_min;roh<roh_max+1;roh++) {
            if (count(voting,theta,roh)>hough_max) {
                hough_max = count(voting,theta,roh);
                final_r = roh;
                final_t = theta;
            }
        }
    }

    printf("r %d, t %d\n", roh, theta);

    for (i=0;i<newH;i++) {
        for (j=0;j<newW;j++) {
            int x = j;
            int y = newH-1-i;
            if (abs(x*sin(final_t*M_PI/180) - y*cos(final_t*M_PI/180) + final_r) < 1) edge.data.push_back(255);
            else edge.data.push_back(0);
        }
    }


}

#endif
