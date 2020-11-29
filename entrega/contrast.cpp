#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hist-equ.h"


void run_cpu_color_test(PPM_IMG img_in);
void run_cpu_gray_test(PGM_IMG img_in);


int main(int argc, char* argv[])
{
    int rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    double start;
    float msg_start;

    PGM_IMG img_ibuf_g;
    PPM_IMG img_ibuf_c;

    if (rank == 0) {
        printf("Running contrast enhancement for gray-scale images.\n");
        start = MPI_Wtime();
        img_ibuf_g = read_pgm("in.pgm");
        msg_start = MPI_Wtime();
    }
    MPI_Bcast(&img_ibuf_g.w, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&img_ibuf_g.h, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank != 0)
        img_ibuf_g.img = (unsigned char *)malloc(img_ibuf_g.w*img_ibuf_g.h * sizeof(unsigned char));

    MPI_Bcast(img_ibuf_g.img, img_ibuf_g.w*img_ibuf_g.h, MPI_UNSIGNED_CHAR, 0, MPI_COMM_WORLD);

    if (rank == 0)
        printf("MSGGRIS %f \n",MPI_Wtime()-msg_start);

    run_cpu_gray_test(img_ibuf_g);
    free_pgm(img_ibuf_g);

    if (rank == 0) {
        printf("Gris %f \n",MPI_Wtime()-start);
        printf("Running contrast enhancement for color images.\n");
        start = MPI_Wtime();
        img_ibuf_c = read_ppm("in.ppm");
        msg_start = MPI_Wtime();
    }
    MPI_Bcast(&img_ibuf_c.w, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&img_ibuf_c.h, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (rank != 0) {
        img_ibuf_c.img_r = (unsigned char *)malloc(img_ibuf_c.w*img_ibuf_c.h * sizeof(unsigned char));
        img_ibuf_c.img_g = (unsigned char *)malloc(img_ibuf_c.w*img_ibuf_c.h * sizeof(unsigned char));
        img_ibuf_c.img_b = (unsigned char *)malloc(img_ibuf_c.w*img_ibuf_c.h * sizeof(unsigned char));
    }
    MPI_Bcast(img_ibuf_c.img_r, img_ibuf_c.w*img_ibuf_c.h, MPI_UNSIGNED_CHAR, 0, MPI_COMM_WORLD);
    MPI_Bcast(img_ibuf_c.img_g, img_ibuf_c.w*img_ibuf_c.h, MPI_UNSIGNED_CHAR, 0, MPI_COMM_WORLD);
    MPI_Bcast(img_ibuf_c.img_b, img_ibuf_c.w*img_ibuf_c.h, MPI_UNSIGNED_CHAR, 0, MPI_COMM_WORLD);
    if (rank == 0)
        printf("MSGCOLOR %f \n",MPI_Wtime()-msg_start);

    run_cpu_color_test(img_ibuf_c);
    free_ppm(img_ibuf_c);
    if (rank==0){
        printf("Color %f \n",MPI_Wtime()-start);
    }

    MPI_Finalize();
    return 0;
}


void run_cpu_color_test(PPM_IMG img_in)
{
    PPM_IMG img_obuf_hsl, img_obuf_yuv;
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    double start = MPI_Wtime();
    if (rank == 0)
        printf("Starting CPU processing...\n");
    img_obuf_hsl = contrast_enhancement_c_hsl(img_in);
    if (rank == 0) {
        printf("HSL processing time: %f (ms)\n", MPI_Wtime()-start /* TIMER */ );
        write_ppm(img_obuf_hsl, "out_hsl.ppm");
    }

    start = MPI_Wtime();
    img_obuf_yuv = contrast_enhancement_c_yuv(img_in);
    if (rank == 0) {
        printf("YUV processing time: %f (ms)\n", MPI_Wtime()-start /* TIMER */);
        write_ppm(img_obuf_yuv, "out_yuv.ppm");
    }

    if (rank == 0) {
        // SOLO EL 0 TIENE ESTO INICIALIZADO
        free_ppm(img_obuf_hsl);
        free_ppm(img_obuf_yuv);
    }
}


void run_cpu_gray_test(PGM_IMG img_in)
{
    PGM_IMG img_obuf;
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    double start = MPI_Wtime();
    if (rank == 0)
        printf("Starting CPU processing...\n");
    img_obuf = contrast_enhancement_g(img_in);
    if (rank == 0) {
        printf("Processing time: %f (ms)\n", MPI_Wtime()-start /* TIMER */ );
        write_pgm(img_obuf, "out.pgm");
    }

    free_pgm(img_obuf);
}


PPM_IMG read_ppm(const char * path)
{
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

    #pragma omp parallel for
    for(i = 0; i < result.w*result.h; i ++){
        result.img_r[i] = ibuf[3*i + 0];
        result.img_g[i] = ibuf[3*i + 1];
        result.img_b[i] = ibuf[3*i + 2];
    }

    fclose(in_file);
    free(ibuf);

    return result;
}


void write_ppm(PPM_IMG img, const char * path)
{
    FILE * out_file;
    int i;

    char * obuf = (char *)malloc(3 * img.w * img.h * sizeof(char));

    #pragma omp parallel for
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


void free_ppm(PPM_IMG img)
{
    free(img.img_r);
    free(img.img_g);
    free(img.img_b);
}


PGM_IMG read_pgm(const char * path)
{
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


void write_pgm(PGM_IMG img, const char * path)
{
    FILE * out_file;
    out_file = fopen(path, "wb");
    fprintf(out_file, "P5\n");
    fprintf(out_file, "%d %d\n255\n",img.w, img.h);
    fwrite(img.img,sizeof(unsigned char), img.w*img.h, out_file);
    fclose(out_file);
}


void free_pgm(PGM_IMG img)
{
    free(img.img);
}

