#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rs-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-rs-Lb{BoxL}.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive

exe={ExecDir}/rockstar
parentexe={ExecDir}/util/find_parents
cd {OPath}

rm auto-rockstar.cfg
$exe -c {Config} &> server.dat &
perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'

srun -n {NCores} $exe -c auto-rockstar.cfg

$parentexe out_0.list 10000 > out_0.parents

sh {ExecDir}/scripts/reformat_rockstar.sh out_0.list
sh {ExecDir}/scripts/reformat_rockstar.sh out_0.parents
