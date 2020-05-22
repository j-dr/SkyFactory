#!/bin/bash
#SBATCH --qos=xfer
#SBATCH --time=24:00:00
#SBATCH --job-name=transfer
#SBATCH --licenses=SCRATCH
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}

cd {OPath}

for lcnum in 1050 2600 4000
do
    echo "----Lb${lcnum}----"
    cd Lb${lcnum}
    htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/Lb${lcnum}/pixlc.tar output/pixlc
    htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/Lb${lcnum}/calcrnn.tar output/calcrnn
    htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/Lb${lcnum}/halos.tar output/halos
    if [ $? -eq 0 ]
    then
        echo "successful, removing files from scratch"
        rm -rf output/pixlc
        rm -rf output/calcrnn
        rm -rf output/halos
    fi
    cd -
done

htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/addgalspostprocess/truth.tar addgalspostprocess/truth
htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/addgalspostprocess/halos.tar addgalspostprocess/halos
htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/calclens.tar calclens
htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/surveymags.tar surveymags

if [ $? -eq 0 ]
then
    echo "successful, removing files from scratch"
    rm -rf addgalspostprocess/truth
    rm -rf addgalspostprocess/halos
    rm -rf calclens
    rm -rf surveymags
fi

for fp in a b
do
    echo "----Y3${fp}----"
    htar -cPVf Chinchilla/Herd/Chinchilla-{cnum}/addgalspostprocess/Y3${fp}.tar addgalspostprocess/Y3${fp}
    if [ $? -eq 0 ]
    then
        rm -rf addgalspostprocess/Y3${fp}
	rm -rf addgalspostprocess/truth_rotated_Y3${fp}
    fi
done
