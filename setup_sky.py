#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import argparse
import templates
import os

default_tasks = ['UnarchiveLightcone', 'Rockstar', 'PixLC', 'CalcRnn', 'Addgals', 'CalcLens']

def main(num, system, tasks=default_tasks):

    sscripts = []

    for task in tasks:

        task = getattr(templates, task)
        t = task(num, system)
        sscript.append( t.setup() )
    
    
    

