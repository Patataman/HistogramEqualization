#!/bin/bash

# $1 = Carpeta $2 = Iteraciones

cd $1

if [ ! -e in.ppm ]; then
  echo "Converting to ppm"
  convert highres.jpg in.ppm
fi
if [ ! -e in.pgm ]; then
  echo "Converting to pgm"
  convert highres.jpg in.pgm
fi

echo "Cleaning executables"
make clean
echo "Compiling"
make

echo "Repeating $2 times"
if [ ! -d times ]; then
  mkdir times
fi

for ((i = 0; i <= $2; i++))
do
  ./contrast >> times/output.txt
done

cat times/output.txt | grep Processing > times/grey_processing.txt
cat times/output.txt | grep Gris > times/grey_time.txt
cat times/output.txt | grep HSL > times/hsl_processing.txt
cat times/output.txt | grep YUV > times/yuv_processing.txt
cat times/output.txt | grep Color > times/color_time.txt
