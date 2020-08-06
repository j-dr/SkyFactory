#!/bin/bash

if [$# -ne 1]; 
    then echo "Please provide your email as a command line argument"
fi

email=$1

mkdir exec
cd exec
git clone https://github.com/j-dr/pixLC.git pixlc
git clone https://github.com/j-dr/calcrnn.git
git clone https://github.com/j-dr/pyaddgals addgals
git clone https://github.com/j-dr/calclens

module unload PrgEnv-gnu
module load PrgEnv-intel cray-fftw cfitsio cray-hdf5 gsl

cd calcrnn && make && cd -
cd calclens && make && cd -
cd ..

sed -i "s,JobBase.*,JobBase: ${PWD}/chinchilla-herd/," systems/cori-haswell/cori-haswell.yaml
#sed -i "s,ExecDir.*,ExecDir: ${PWD}/exec/," systems/cori-haswell/cori-haswell.yaml
sed -i "s,Email.*,Email: ${email}," systems/cori-haswell/cori-haswell.yaml 
