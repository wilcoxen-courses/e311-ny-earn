#! /bin/python3
#  Spring 2020 (PJW)
#
#  Concatenating strings in two columns of a dataframe.
#

import pandas as pd

#
#  Build a simple test data frame with two columns, 'left' and 'right'
#

frame = pd.DataFrame()

frame['left'] = ['one=','two=','three=']
frame['right'] = ['1','2','3']

#
#  Concatenate the strings row by row
#

frame['concat'] = frame['left'] + frame['right']

#
#  Show the result
#

print(frame)
