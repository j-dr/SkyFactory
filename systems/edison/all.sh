#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-all
#SBATCH -o {SimName}{SimNum}-all.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive
