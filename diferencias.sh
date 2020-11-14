#!/bin/bash

cd ./Original
make clean
make
./contrast
cd ..
cd ./$1
make clean
make
./contrast
cd ..
diff ./Original/out_hsl.ppm ./$1/out_hsl.ppm
diff ./Original/out_yuv.ppm ./$1/out_yuv.ppm
diff ./Original/out.pgm ./$1/out.pgm
