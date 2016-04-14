#!/bin/bash -l
#SBATCH -p regular
#SBATCH -t 12:00
#SBATCH -J {SimName}{SimNum}-all
#SBATCH -o {SimName}{SimNum}-all.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive
