#!/bin/bash

# $1 = Carpeta $2 = Iteraciones

cd $1
echo "Entering $1"

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


if [ $1 == "OpenMP" ]; then
  for ((j = 1; j <= 16; j++))
  do
    echo "OpenMP Threads $j"
    export OMP_NUM_THREADS=$j

    mkdir -p times/$j

    for ((i = 0; i < $2; i++))
    do
      ./contrast >> times/$j/output.txt
    done

    cat times/$j/output.txt | grep Processing > times/$j/grey_processing.txt
    cat times/$j/output.txt | grep Gris > times/$j/grey_time.txt
    cat times/$j/output.txt | grep HSL > times/$j/hsl_processing.txt
    cat times/$j/output.txt | grep YUV > times/$j/yuv_processing.txt
    cat times/$j/output.txt | grep Color > times/$j/color_time.txt

  done
fi

if [ $1 == "MPI" ]; then
  for ((j = 2; j<= 4; j++))
  do
    echo "MPI Processes $j"

    mkdir -p times/$j

    for ((i = 0; i < $2; i++))
    do
      mpirun -np $j contrast >> times/$j/output.txt
    done

    cat times/$j/output.txt | grep Processing > times/$j/grey_processing.txt
    cat times/$j/output.txt | grep Gris > times/$j/grey_time.txt
    cat times/$j/output.txt | grep HSL > times/$j/hsl_processing.txt
    cat times/$j/output.txt | grep YUV > times/$j/yuv_processing.txt
    cat times/$j/output.txt | grep Color > times/$j/color_time.txt
  done
fi

if [ $1 == "Combinado" ]; then
  for ((i = 2; i<= 4; i++))
  do
    echo "MPI Processes $i"
    for ((j = 1; j <= 16; j++))
    do
      echo "OpenMP Threads $j"
      export OMP_NUM_THREADS=$j

      mkdir -p times/$i-$j

      for ((i = 0; i < $2; i++))
      do
        mpirun -np $j contrast >> times/$i-$j/output.txt
      done

      cat times/$i-$j/output.txt | grep Processing > times/$i-$j/grey_processing.txt
      cat times/$i-$j/output.txt | grep Gris > times/$i-$j/grey_time.txt
      cat times/$i-$j/output.txt | grep HSL > times/$i-$j/hsl_processing.txt
      cat times/$i-$j/output.txt | grep YUV > times/$i-$j/yuv_processing.txt
      cat times/$i-$j/output.txt | grep Color > times/$i-$j/color_time.txt
    done
  done
fi

echo "Done"
