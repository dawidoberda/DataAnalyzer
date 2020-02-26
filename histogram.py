import matplotlib.pyplot as plt
import pandas as pd
import os
from configparser import ConfigParser

parser = ConfigParser()
parser.read('conf.ini')
print(parser.sections())
print(parser.options('settings'))

AssemblyName = parser.get('settings', 'assemblyname')
print(AssemblyName)

excel_path = os.path.join('./input_data', 'raport.xlsx')
print((os.path.exists(excel_path)))

df = pd.read_excel(excel_path)
#df['AssemblyName'] = df['AssemblyName'].astype(str)

#print(df.head(10))
#is_selected_ass_true = df['AssemblyName'] == 1846771
is_selected_ass_true = df['AssemblyName'] == int(AssemblyName)
df_sort_ass = df[is_selected_ass_true]
print(df_sort_ass.head(10))


#print(df_filtered_assemblyname.head(20))

#
# bins = [2.0,4.0,6.0,8.0,10.0,12.0]

# plt.hist(float_list, bins, label='Diff %', histtype='bar', rwidth=0.8)
# plt.xlabel('difference from lower limit [%]')
# plt.legend()
# plt.show()
