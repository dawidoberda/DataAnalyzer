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
print(errorCode)

#PRZYGOTOWANIE PO TESTERACH
testerList = df_sort_errorCode['AXLoggerName'].tolist()
testerSet = set(testerList)
print(f'Used testers : {testerSet}')

is_selected_tester_list = []
for tester in testerSet:
    print('creating series')
    print(tester)
    is_selected_tester_list.append(df_sort_errorCode['AXLoggerName'] == str(tester))

df_tester_sorted_list = []
#print(f'series of results for tester : \n {is_selected_tester_list}')
for tester_series in is_selected_tester_list:
    df_tester_sorted_list.append(df_sort_errorCode[tester_series])

#print(df_tester_sorted_list)

#TOTAL PRZYGOTOWANIE
print("converting..")
df_sort_errorCode['StopTime'] = pd.to_datetime(df_sort_errorCode['StopTime'], format='%Y-%d-%m %H:%M:%S')
df_sort_errorCode.set_index('StopTime', drop = False, inplace = True)

#USTAWIENIA SUBPLOTU
#TODO: trzeba dodac w przygotowanie po testerach zliczanie ile ma byc tych subplotow i zrobic rysowanie subplotow

#RYSOWANIE
#TOTAL
df_sort_errorCode.groupby(pd.Grouper(freq = bin))['SerialNumber'].count().plot(title = errorCode, kind = "bar")


#USTAWIENIA WYKRESU
plt.xlabel('Date')
plt.ylabel('Units')

plt.tight_layout()
plt.xticks(rotation = 45)

plt.show()

#TODO: niby dzial. dorobic jakis interface do tego. i sprawdzic na wiekszym pliku i dla innych danych

# bins = [2.0,4.0,6.0,8.0,10.0,12.0]

# plt.hist(float_list, bins, label='Diff %', histtype='bar', rwidth=0.8)
# plt.xlabel('difference from lower limit [%]')
# plt.legend()
# plt.show()
