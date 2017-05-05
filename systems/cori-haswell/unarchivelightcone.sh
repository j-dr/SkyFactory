#!/bin/bash -l
#SBATCH -p xfer
#SBATCH -A {Repo}
#SBATCH -M {Cluster}
#SBATCH --mail-type=ALL
#SBATCH --mail-user={Email}
#SBATCH -t 24:00:00
#SBATCH -J {SimName}-{SimNum}-ua-Lb{BoxL}
#SBATCH -o {SimName}-{SimNum}-ua-Lb{BoxL}.%j.oe
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH -N 1
#SBATCH -n 1

mkdir -p {OPath}
cd {OPath}

for lcnum in 000 001 002 003 004 005 006 007
do
    echo "----lightcone$lcnum----"
    htar -xVf /home/b/beckermr/{SimName}/{Group}/{SimName}-{SimNum}/Lb{BoxL}/lightcone$lcnum.tar lightcone$lcnum
done
