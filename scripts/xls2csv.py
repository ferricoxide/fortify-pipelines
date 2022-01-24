#!/usr/bin/python3

"""Import required Python modules"""
import os
import pandas as pd

sourceFile = os.getenv('OUTPUT_XLS')
destFile   = os.getenv('OUTPUT_CSV')

read_file = pd.read_excel (sourceFile)
read_file.to_csv (destFile,
                  index = None,
                  header = True)
