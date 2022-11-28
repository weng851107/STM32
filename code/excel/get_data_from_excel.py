import pandas as pd
import math
 
df = pd.read_excel("E5522-Trace_curve_EFFL_3.3mm~10.2mm-20210531.xlsx")

row_indexer = 13
row_max = 2111

while row_indexer < row_max:

    '''
    zoom = int(df.iat[row_indexer, 3])
    focus_0_5 = int(df.iat[row_indexer, 15])
    focus_1 = int(df.iat[row_indexer, 13])
    focus_3 = int(df.iat[row_indexer, 11])
    focus_5 = int(df.iat[row_indexer, 9])
    focus_10 = int(df.iat[row_indexer, 7])
    focus_inf = int(df.iat[row_indexer, 5])
    '''

    zoom = round(df.iat[row_indexer, 3])
    focus_0_5 = round(df.iat[row_indexer, 15])
    focus_1 = round(df.iat[row_indexer, 13])
    focus_3 = round(df.iat[row_indexer, 11])
    focus_5 = round(df.iat[row_indexer, 9])
    focus_10 = round(df.iat[row_indexer, 7])
    focus_inf = round(df.iat[row_indexer, 5])

    print("{", end = '')
    print("{0}, {1}, {2}, {3}, {4}, {5}, {6}".format(zoom, focus_0_5, focus_1, focus_3, focus_5, focus_10, focus_inf), end = '')
    print("},", end = '\n')

    row_indexer+=1

'''
zoom = int(df.iat[row_indexer, 3])
focus_0_5 = int(df.iat[row_indexer, 15])
focus_1 = int(df.iat[row_indexer, 13])
focus_3 = int(df.iat[row_indexer, 11])
focus_5 = int(df.iat[row_indexer, 9])
focus_10 = int(df.iat[row_indexer, 7])
focus_inf = int(df.iat[row_indexer, 5])
'''

zoom = round(df.iat[row_indexer, 3])
focus_0_5 = round(df.iat[row_indexer, 15])
focus_1 = round(df.iat[row_indexer, 13])
focus_3 = round(df.iat[row_indexer, 11])
focus_5 = round(df.iat[row_indexer, 9])
focus_10 = round(df.iat[row_indexer, 7])
focus_inf = round(df.iat[row_indexer, 5])

print("{", end = '')
print("{0}, {1}, {2}, {3}, {4}, {5}, {6}".format(zoom, focus_0_5, focus_1, focus_3, focus_5, focus_10, focus_inf), end = '')
print("}", end = '\n')