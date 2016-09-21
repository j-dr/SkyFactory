#!/bin/bash -l
#SBATCH -p regular
#SBATCH --A {Repo}
#SBATCH --mail-type=ALL
#SBATCH --mail-user={Email}
#SBATCH -t 2:00:00
#SBATCH -J {SimName}-{SimNum}-ua-Lb{BoxL}
#SBATCH -o {SimName}-{SimNum}-ua-Lb{BoxL}.%j.oe
#SBATCH -N 1
#SBATCH -n 4

mkdir -p {OPath}
cd {OPath}

for lcnum in 000 001 002 003 004 005 006 007
do
    echo "----lightcone$lcnum----"
    htar -xVf {SimName}/{Group}/{SimName}-{SimNum}/Lb{BoxL}/lightcone$lcnum.tar lightcone$lcnum
    while
done
