#!/bin/bash
#SBATCH -p regular
#SBATCH -t 96:00
#SBATCH -J {SimName}{SimNum}-rs-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-rs-Lb{BoxL}.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

exe={ExecDir}/rockstar
parentexe={ExecDir}/util/find_parents
cd {OPath}

rm auto-rockstar.cfg
$exe -c {Config} &> server.dat &
perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'

srun -n {NCores} $exe -c auto-rockstar.cfg

$parentexe {BoxL} out_0.list
