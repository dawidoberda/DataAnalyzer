import matplotlib.pyplot as plt
import pandas as pd
import os
from configparser import ConfigParser
from datetime import date


class Histogram:


    excel_path = ''
    df = None

    def __init__(self):
        pass

    """Method to read csv with report and create basic data frame
    :returns True if file exist
    """
    def read_csv(self, path):
        self.excel_path = path
        is_exist = os.path.exists(self.excel_path)
        if is_exist == True:
            self.df = pd.read_excel(self.excel_path)
        return is_exist

    """
        Method to get assembly names stated in report
        :returns assembly names as set
    """
    def get_assembly_set(self):
        assembly_list = self.df['AssemblyName'].tolist()
        assembly_set = set(assembly_list)
        return assembly_set

    """
        Mothod to get step names stated in report
        :returns step names as set
    """
    def get_step_set(self):
        step_lits = self.df['StepName'].tolist()
        step_set = set(step_lits)
        return step_set

    """
        Method to generate histogram
        :arg AssembName: Selected assembly name of which You want to draw histogram for
        :arg errorCode: selected step name of which You want to draw histogram for
    """
    def generate_plot(self, AssemblyName, errorCode):
        is_selected_ass_true = self.df['AssemblyName'] == int(AssemblyName)
        df_sort_ass = self.df[is_selected_ass_true]
        is_selected_status = df_sort_ass['Status'] == 'F'
        df_sort_status = df_sort_ass[is_selected_status]
        is_selected_errorCode = df_sort_status['StepName'] == str(errorCode)
        df_sort_errorCode = df_sort_status[is_selected_errorCode]

        dateList = df_sort_ass['StopTime'].tolist()

        print(f'first date is {dateList[0]}')
        print(f'last date is {dateList[-1]}')

        startDate, startTime = dateList[0].split(" ")
        startDate_year, startDate_day, startDate_month  = startDate.split("-")
        start = date(int(startDate_year), int(startDate_month), int(startDate_day))

        stopDate, stopTime = dateList[-1].split(" ")
        stopDate_year, stopDate_day, stopDate_month = stopDate.split("-")
        stop = date(int(stopDate_year), int(stopDate_month), int(stopDate_day))


        dateDiff = start - stop
        print(dateDiff)
        bin = dateDiff/10
        print(bin)
        print(errorCode)

        #PRZYGOTOWANIE PO TESTERACH
        testerList = df_sort_errorCode['AXLoggerName'].tolist()
        #testerSet = set(testerList)
        testerSet = list(dict.fromkeys(testerList))
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


        #TOTAL PRZYGOTOWANIE
        print("converting..")
        df_sort_errorCode['StopTime'] = pd.to_datetime(df_sort_errorCode['StopTime'], format='%Y-%d-%m %H:%M:%S')
        df_sort_errorCode.set_index('StopTime', drop = False, inplace = True)

        #USTAWIENIA SUBPLOTU
        numberOfTesters = len(testerSet)
        numberOfPlotes = numberOfTesters + 1 #+1 bo jeszcze total
        print(f'Number of plotes : {numberOfPlotes}')
        fig, axes = plt.subplots(nrows = int(numberOfPlotes) , ncols=1, sharey=True)

        #RYSOWANIE
        #TOTAL
        df_sort_errorCode.groupby(pd.Grouper(freq = bin))['SerialNumber'].count().plot(title = errorCode, kind = "bar", ax=axes[0])
        axes[0].set_title('TOTAL')
        #axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Units')
        #axes[0].tick_params(labelrotation = 45)
        axes[0].tick_params(axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False)

        #PO TESTERACH
        for i in range(0, numberOfTesters):
            df_tester_sorted_list[i]['StopTime'] = pd.to_datetime(df_tester_sorted_list[i]['StopTime'], format='%Y-%d-%m %H:%M:%S')
            df_tester_sorted_list[i].set_index('StopTime', drop = False, inplace = True)
            df_tester_sorted_list[i].groupby(pd.Grouper(freq=bin))['SerialNumber'].count().plot(kind = "bar", ax = axes[i+1])
            if i == numberOfTesters -1 :
                axes[i + 1].set_title(testerSet[i])
                axes[i + 1].set_xlabel('Date')
                axes[i + 1].set_ylabel('Units')
                axes[i + 1].tick_params(axis='x', which='both', labelrotation=45, labelsize=5)
            else:
                axes[i+1].set_title(testerSet[i])
                axes[i+1].set_ylabel('Units')
                axes[i+1].tick_params(axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    labelbottom=False)

        fig.tight_layout()
        fig.set_size_inches(10.5, 10.5, forward=True)
        fig.suptitle(str(errorCode))
        plt.subplots_adjust(bottom=0.15, hspace=0.3)
        plt.show()

if __name__ == '__main__':
    histogram = Histogram()
    fileExist = histogram.read_csv('.\\input_data\\raport.xlsx')
    print(f'Is csv file exist :{fileExist}')
    assemblySet = histogram.get_assembly_set()
    print(f'Assembly set : \n {assemblySet}')
    stepSet = histogram.get_step_set()
    print(f'Test Step set : \n {stepSet}')
    histogram.generate_plot(1846771, 'SPDIFAudioInputTest')
