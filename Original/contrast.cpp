// Líneas totales 59
// Líneas paralelizables 17

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hist-equ.h"

void run_cpu_color_test(PPM_IMG img_in);
void run_cpu_gray_test(PGM_IMG img_in);


int main(){
	
    PGM_IMG img_ibuf_g;
    PPM_IMG img_ibuf_c;
    
    double tiempo = omp_get_wtime();
    
    printf("Running contrast enhancement for gray-scale images.\n");
    img_ibuf_g = read_pgm("in.pgm");
    run_cpu_gray_test(img_ibuf_g);
    free_pgm(img_ibuf_g);
    
    printf("Gris %f \n",omp_get_wtime()-tiempo);
    tiempo = omp_get_wtime();

    printf("Running contrast enhancement for color images.\n");
    img_ibuf_c = read_ppm("in.ppm");
    run_cpu_color_test(img_ibuf_c);
    free_ppm(img_ibuf_c);

    printf("Color %f \n",omp_get_wtime()-tiempo);
    
    return 0;
}
// 6 líneas en total sin contar los tiempos, return y declaración de variables (2) (3 líneas para gris y 3 para color)
// 0 líneas paralelizables (así a primera vista)

void run_cpu_color_test(PPM_IMG img_in)
{
    PPM_IMG img_obuf_hsl, img_obuf_yuv;

    printf("Starting CPU processing...\n");
    double tiempo = omp_get_wtime();

    img_obuf_hsl = contrast_enhancement_c_hsl(img_in);
    printf("HSL processing time: %f (ms)\n", omp_get_wtime()-tiempo /* TIMER */ );

    write_ppm(img_obuf_hsl, "out_hsl.ppm");

    tiempo = omp_get_wtime();
    img_obuf_yuv = contrast_enhancement_c_yuv(img_in);
    printf("YUV processing time: %f (ms)\n", omp_get_wtime()-tiempo /* TIMER */);

    write_ppm(img_obuf_yuv, "out_yuv.ppm");

    free_ppm(img_obuf_hsl);
    free_ppm(img_obuf_yuv);
}
// 6 líneas en total para imagen en color (sin contar tiempos ni declaraciones)
// 0 líneas paralelizables

void run_cpu_gray_test(PGM_IMG img_in)
{
    PGM_IMG img_obuf;

    printf("Starting CPU processing...\n");
    double tiempo = omp_get_wtime();
    img_obuf = contrast_enhancement_g(img_in);
    printf("Processing time: %f (ms)\n",  omp_get_wtime()-tiempo/* TIMER */ );

    write_pgm(img_obuf, "out.pgm");
    free_pgm(img_obuf);
}
// 3 líneas en total para gris (no tiempo ni declaraciones)
// 0 líneas paralelizables


PPM_IMG read_ppm(const char * path){
    FILE * in_file;
    char sbuf[256];
    
    char *ibuf;
    PPM_IMG result;
    int v_max, i;
    in_file = fopen(path, "r");
    if (in_file == NULL){
        printf("Input file not found!\n");
        exit(1);
    }
    /*Skip the magic number*/
    fscanf(in_file, "%s", sbuf);


    //result = malloc(sizeof(PPM_IMG));
    fscanf(in_file, "%d",&result.w);
    fscanf(in_file, "%d",&result.h);
    fscanf(in_file, "%d\n",&v_max);
    printf("Image size: %d x %d\n", result.w, result.h);
    

    result.img_r = (unsigned char *)malloc(result.w * result.h * sizeof(unsigned char));
    result.img_g = (unsigned char *)malloc(result.w * result.h * sizeof(unsigned char));
    result.img_b = (unsigned char *)malloc(result.w * result.h * sizeof(unsigned char));
    ibuf         = (char *)malloc(3 * result.w * result.h * sizeof(char));

    
    fread(ibuf,sizeof(unsigned char), 3 * result.w*result.h, in_file);

    for(i = 0; i < result.w*result.h; i ++){
        result.img_r[i] = ibuf[3*i + 0];
        result.img_g[i] = ibuf[3*i + 1];
        result.img_b[i] = ibuf[3*i + 2];
    }
    
    fclose(in_file);
    free(ibuf);
    
    return result;
}
// 17 líneas para color sin return ni declaraciones
// 8 líneas deberían ser paralelizables (reserva de espacio para cada buffer, lectura y el for)

void write_ppm(PPM_IMG img, const char * path){
    FILE * out_file;
    int i;
    
    char * obuf = (char *)malloc(3 * img.w * img.h * sizeof(char));

    for(i = 0; i < img.w*img.h; i ++){
        obuf[3*i + 0] = img.img_r[i];
        obuf[3*i + 1] = img.img_g[i];
        obuf[3*i + 2] = img.img_b[i];
    }
    out_file = fopen(path, "wb");
    fprintf(out_file, "P6\n");
    fprintf(out_file, "%d %d\n255\n",img.w, img.h);
    fwrite(obuf,sizeof(unsigned char), 3*img.w*img.h, out_file);
    fclose(out_file);
    free(obuf);
}
// 11 líneas para color sin contrar declaraciones
// 5 líneas deberían ser paralelizables (reserva de memoria y el for)

void free_ppm(PPM_IMG img)
{
    free(img.img_r);
    free(img.img_g);
    free(img.img_b);
}
// 3 íneas para color
// 3 líneas paralelizables

PGM_IMG read_pgm(const char * path){
    FILE * in_file;
    char sbuf[256];
    
    
    PGM_IMG result;
    int v_max;//, i;
    in_file = fopen(path, "r");
    if (in_file == NULL){
        printf("Input file not found!\n");
        exit(1);
    }
    
    fscanf(in_file, "%s", sbuf); /*Skip the magic number*/
    fscanf(in_file, "%d",&result.w);
    fscanf(in_file, "%d",&result.h);
    fscanf(in_file, "%d\n",&v_max);
    printf("Image size: %d x %d\n", result.w, result.h);
    

    result.img = (unsigned char *)malloc(result.w * result.h * sizeof(unsigned char));

        
    fread(result.img,sizeof(unsigned char), result.w*result.h, in_file);    
    fclose(in_file);
    
    return result;
}
// 9 ´líneas para gris (no declaraciones ni return)
// 1 línea paralelizable (la lectura)

void write_pgm(PGM_IMG img, const char * path){
    FILE * out_file;
    out_file = fopen(path, "wb");
    fprintf(out_file, "P5\n");
    fprintf(out_file, "%d %d\n255\n",img.w, img.h);
    fwrite(img.img,sizeof(unsigned char), img.w*img.h, out_file);
    fclose(out_file);
}
// 3 líneas para gris (no declaraciones ni prints)
// 0 líneas paralelizables (creo... porque escribir varios a la vez es mala idea)

void free_pgm(PGM_IMG img)
{
    free(img.img);
}
// 1 línea para gris
// 0 líneas paralelizables

