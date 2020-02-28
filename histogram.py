import matplotlib.pyplot as plt
import pandas as pd
import os
from configparser import ConfigParser
from datetime import date

parser = ConfigParser()
parser.read('conf.ini')
print(parser.sections())
print(parser.options('settings'))

AssemblyName = parser.get('settings', 'assemblyname')
print(AssemblyName)

excel_path = os.path.join('./input_data', 'raport.xlsx')
print((os.path.exists(excel_path)))

df = pd.read_excel(excel_path)

#is_selected_ass_true = df['AssemblyName'] == 1846771
is_selected_ass_true = df['AssemblyName'] == int(AssemblyName)
df_sort_ass = df[is_selected_ass_true]

print("=========")

is_selected_status = df_sort_ass['Status'] == 'F'
df_sort_status = df_sort_ass[is_selected_status]

errorCode = parser.get('settings', 'errorCode')
print(errorCode)

is_selected_errorCode = df_sort_status['StepName'] == str(errorCode)
df_sort_errorCode = df_sort_status[is_selected_errorCode]

dateList = df_sort_ass['StopTime'].tolist()
print(dateList)


print(f'first date is {dateList[0]}')
print(f'last date is {dateList[-1]}')

startDate, startTime = dateList[0].split(" ")
startDate_year, startDate_day, startDate_month  = startDate.split("-")
start = date(int(startDate_year), int(startDate_month), int(startDate_day))
print(start)

stopDate, stopTime = dateList[-1].split(" ")
stopDate_year, stopDate_day, stopDate_month = stopDate.split("-")
stop = date(int(stopDate_year), int(stopDate_month), int(stopDate_day))
print(stop)

dateDiff = start - stop
print(dateDiff)
bin = dateDiff/10
print(bin)

print(df_sort_errorCode.dtypes)
print("converting..")
df_sort_errorCode['StopTime'] = pd.to_datetime(df_sort_errorCode['StopTime'], format='%Y-%d-%m %H:%M:%S')
print(df_sort_errorCode.dtypes)
df_sort_errorCode.set_index('StopTime', drop = False, inplace = True)
print(df_sort_errorCode.head(20))
#df_sort_errorCode.groupby(pd.TimeGrouper(freq = bin))

#TODO: trzeba jakos podzielic to na przedzialy o danej szerokosci i zliczac liczbe elementow w danych przedzialach

# bins = [2.0,4.0,6.0,8.0,10.0,12.0]

# plt.hist(float_list, bins, label='Diff %', histtype='bar', rwidth=0.8)
# plt.xlabel('difference from lower limit [%]')
# plt.legend()
# plt.show()
