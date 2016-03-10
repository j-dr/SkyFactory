#!/bin/bash -l
#SBATCH -M {Cluster}
#SBATCH -p xfer
#SBATCH --mail-type=ALL
#SBATCH --mail-user={Email}
#SBATCH -t 2:00:00
#SBATCH -J {SimName}-{SimNum}-ua-Lb{BoxL}
#SBATCH -o {SimName}-{SimNum}-ua-Lb{BoxL}.%j.oe

mkdir -p {OPath}
cd {OPath}

for lcnum in 000 001
do
    echo "----lightcone$lcnum----"
    htar -xVf {SimName}-{SimNum}/{Group}/{SimName}-{SimNum}/Lb{BoxL}/lightcone$lcnum.tar lightcone$lcnum
done
