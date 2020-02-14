#!/bin/bash
#SBATCH --qos=xfer
#SBATCH --time=24:00:00
#SBATCH --job-name=transfer-c{cnum}
#SBATCH --licenses=SCRATCH
#SBATCH --mail-type=All
#SBATCH --mail-user  joe.derose13@gmail.com

cd /global/cscratch1/sd/jderose/BCC/Chinchilla/Herd/Chinchilla-{cnum}/

for lcnum in 1050 2600 4000
  do
    echo "----Lb${lcnum}----"
    cd Lb${lcnum}
    htar -xvf Chinchilla/Herd/Chinchilla-{cnum}/Lb${lcnum}/pixlc.tar output/pixlc
    htar -xvf Chinchilla/Herd/Chinchilla-{cnum}/Lb${lcnum}/calcrnn.tar output/calcrnn
    htar -xvf Chinchilla/Herd/Chinchilla-{cnum}/Lb${lcnum}/halos.tar output/halos
    if [ $? -eq 0 ]
        then
	    echo "successfully unarchived"
    fi
    cd -
done

