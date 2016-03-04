#!/bin/bash
#SBATCH -p regular
#SBATCH -t 96:00
#SBATCH -j {Simname}{Simnum}-rs-Lb{BoxL}
#SBATCH -o {Simname}{Simnum}-rs-Lb{BoxL}.%j.oe
#SBATCH -A {repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {email}
#SBATCH -n {ncores}
#SBATCH --exclusive

exe={execpath}/rockstar
cd {opath}

rm auto-rockstar.cfg
$exe -c {config} &> server.dat &
perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'

srun $exe -c auto-rockstar.cfg
