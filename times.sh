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

if [ $1 == "Original" ]; then
    mkdir -p times/1

    for ((i = 0; i < $2; i++))
    do
      ./contrast >> times/1/output.txt
    done

    cat times/1/output.txt | grep Processing > times/1/grey_processing.txt
    cat times/1/output.txt | grep Gris > times/1/grey_time.txt
    cat times/1/output.txt | grep HSL > times/1/hsl_processing.txt
    cat times/1/output.txt | grep YUV > times/1/yuv_processing.txt
    cat times/1/output.txt | grep Color > times/1/color_time.txt
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
  for ((i = 2; i<= 2; i++))
  do
    np=$((2 ** $i))
    echo "MPI Processes $np"
    for ((j = 2; j <= 2; j++))
    do
      proc=$((2 ** $j))
      echo "OpenMP Threads $proc"
      export OMP_NUM_THREADS=$proc

      mkdir -p times/$np/$proc

      for ((w = 0; w < $2; w++))
      do
        mpirun -np $np -hostfile hosts contrast >> times/$np/$proc/output.txt
      done

      cat times/$np/$proc/output.txt | grep Processing > times/$np/$proc/grey_processing.txt
      cat times/$np/$proc/output.txt | grep Gris > times/$np/$proc/grey_time.txt
      cat times/$np/$proc/output.txt | grep HSL > times/$np/$proc/hsl_processing.txt
      cat times/$np/$proc/output.txt | grep YUV > times/$np/$proc/yuv_processing.txt
      cat times/$np/$proc/output.txt | grep Color > times/$np/$proc/color_time.txt
      cat times/$np/$proc/output.txt | grep MSGGRIS > times/$np/$proc/msg_time_gris.txt
      cat times/$np/$proc/output.txt | grep MSGCOLOR > times/$np/$proc/msg_time_color.txt

    done
  done
fi

echo "Done"
