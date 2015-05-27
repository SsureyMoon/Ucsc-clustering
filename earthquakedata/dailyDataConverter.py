from __future__ import division
import pandas
import numpy as np

def interploateWithZero(filename='quakes2010_smaller.csv', sep=' ', column_names=['DATE', 'CODE', 'TIMES'], will_write_file=False):
    data = pandas.read_table(filename, sep, names=column_names)
    date_dataframe = data.set_index('DATE')
    date_dataframe.index = pandas.to_datetime(date_dataframe.index)
    date_dataframe.index.name = None
    del data
    code_set =  set(date_dataframe['CODE'])

    start_date = '2010-01-01'
    end_date = '2010-12-31'
    range_for_data = pandas.date_range(start_date, end_date)

    df_zero = pandas.DataFrame(columns=['CODE', 'TIMES'])
    for code in code_set:
        df_temp = pandas.DataFrame({'CODE': code, 'TIMES':0},index=range_for_data)
        df_zero = pandas.concat([df_zero, df_temp])

    df_total = pandas.DataFrame(columns=['CODE', 'TIMES'])
    for progress, code in enumerate(code_set):
        subset = date_dataframe.loc[date_dataframe['CODE']==code]
        subset2 = df_zero.loc[df_zero['CODE']==code]
        for index, row in subset.iterrows():
            subset2.loc[subset2.index == index, 'TIMES'] = row['TIMES']
        df_total = pandas.concat([df_total, subset2])
        if progress%10 == 0:
            print ('progress: {}%'.format(progress/len(code_set)*100))
    if will_write_file:
        with open(filename.split('.')[0]+"_interpolated.csv", "w+") as wfile:
            df_total.to_csv(wfile, sep=sep, header=False)
    return  df_total


print interploateWithZero('quakes2010_smaller.csv', ' ', ['DATE', 'CODE', 'TIMES'], True)