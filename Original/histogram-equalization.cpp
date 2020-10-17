#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hist-equ.h"


void histogram(int * hist_out, unsigned char * img_in, int img_size, int nbr_bin){
    int i;
    for ( i = 0; i < nbr_bin; i ++){
        hist_out[i] = 0;
    }

    for ( i = 0; i < img_size; i ++){
        hist_out[img_in[i]] ++;
    }
}
// 4 líneas para color y gris (sin declaraciones)
// 4 líneas paralelizables (aunque luego sabemos que al menos 
//                          el primer bucle es tontería de paralelizar)

void histogram_equalization(unsigned char * img_out, unsigned char * img_in, 
                            int * hist_in, int img_size, int nbr_bin){
    int *lut = (int *)malloc(sizeof(int)*nbr_bin);
    int i, cdf, min, d;
    /* Construct the LUT by calculating the CDF */
    cdf = 0;
    min = 0;
    i = 0;
    while(min == 0) {
        min = hist_in[i++];
    }
    d = img_size - min;
    for(i = 0; i < nbr_bin; i ++){
        cdf += hist_in[i];
        //lut[i] = (cdf - min)*(nbr_bin - 1)/d;
        lut[i] = (int)(((float)cdf - min)*255/d + 0.5);
        if(lut[i] < 0) {
            lut[i] = 0;
        }
    }
    
    /* Get the result image */
    for(i = 0; i < img_size; i ++) {
        if(lut[img_in[i]] > 255) {
            img_out[i] = 255;
        } else {
            img_out[i] = (unsigned char)lut[img_in[i]];
        }
        
    }
}
// 15 líneas en total para color y gris (sin declaraciones y en el if-else contando el más largo)
// 3 líneas (el segundo for, el primero no es paralelizable por 
//           la lut depende del cdf acumulado hasta el momento. Aunque de ser así,
//           luego el particionar la imagen para MPI no debería dar los mismos resultados... 
//           Y SI, depende solo de hist_in??? Si fuese así, quizás SI que es paralelizable la parte del cdf...
