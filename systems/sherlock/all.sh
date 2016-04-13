#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-all
#SBATCH -o {SimName}{SimNum}-all.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive
