'''
Created on 2020/12/16

@author: nishidayuki
'''

#オーストラリア気象データ収集
from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS
import re
import openpyxl

class Year(): #year
    def __init__(self):
        self.url_year = 2020
        self.index_num = 0

class urlList(): #url_list
    def __init__(self):
        self.cityName_list = ['canberra',
                              'sydney',
                              'melbourne',
                              'adelaide',
                              'brisbane']
        print(self.cityName_list[year.index_num], year.url_year)

        self.max_url_list = ['http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-990070334&p_stn_num=070351',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-872394768&p_stn_num=066037',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-1480725183&p_stn_num=086038',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-106330725&p_stn_num=023034',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-334992408&p_stn_num=040913']

        self.min_url_list = ['http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=123&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-990070530&p_stn_num=070351',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=123&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-872394964&p_stn_num=066037',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=123&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-1480725379&p_stn_num=086038',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=123&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-106330921&p_stn_num=023034',
                             'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=123&p_display_type=dailyDataFile&p_startYear=' + str(year.url_year) + '&p_c=-334992604&p_stn_num=040913']

class outputList():
    def __init__(self):
        self.canberra_max_list = []
        self.canberra_min_list = []
        self.sydney_max_list = []
        self.sydney_min_list = []
        self.melbourne_max_list = []
        self.melbourne_min_list = []
        self.adelaide_max_list = []
        self.adelaide_min_list = []
        self.brisbane_max_list = []
        self.brisbane_min_list = []
        self.fiveCity_max_aveList = []
        self.fiveCity_min_aveList = []

class Scraping():
    def __init__(self):
        self.max_datasets = None
        self.min_datasets = None

    def MaxUrlRequest(self):
        driver.get(url_list.max_url_list[year.index_num])
        time.sleep(1)
        page_source = driver.page_source
        soup = BS(page_source, 'html.parser')
        return soup

    def MaxHtmlParser(self):
        self.max_datasets = self.MaxUrlRequest().select('td')

    def MinUrlRequest(self):
        driver.get(url_list.min_url_list[year.index_num])
        time.sleep(1)
        page_source = driver.page_source
        soup = BS(page_source, 'html.parser')
        return soup

    def MinHtmlParser(self):
        self.min_datasets = self.MinUrlRequest().select('td')

class Calc():
    def __init__(self):
        self.maxData_list = []
        self.minData_list = []
        self.maxAve_list = []
        self.minAve_list = []

    def MaxDataMonthly(self, month):
        print('------------------')
        notMatch_count = 0
        match_count = 0
        for dt in sp.max_datasets:
            if re.match('\d+.\d', dt.text) == None:
                notMatch_count += 1
            else:
                match_count += 1
            if match_count == 1:
                break

        del sp.max_datasets[:notMatch_count]

        data_count = 0
        first_count = 0
        first_data = None
        day_count = 0
        for maxData in sp.max_datasets:
            maxData = maxData.text
            data_count += 1
            data_count -= month
            if data_count == 0 or data_count % 12 == 0:
                day_count += 1
                first_count += 1
                if first_count == 1 and re.search('\d+.\d', maxData) != None:
                    first_data = maxData
                else:
                    first_data = 27.5

                if re.search('\d+.\d', maxData) == None:
                    maxData = first_data
                print(str(day_count)+'日', maxData, str(month) + "月のデータ")
                try:
                    self.maxData_list.append(float(maxData))
                except:
                    maxData = first_data
                    self.maxData_list.append(float(maxData))
            else:
                pass
            data_count += month
            if day_count == 28:
                    break
        print('------------------')

    def MinDataMonthly(self, month):
        print('------------------')
        notMatch_count = 0
        match_count = 0
        for dt in sp.min_datasets:
            if re.match('\d+.\d', dt.text) == None:
                notMatch_count += 1
            else:
                match_count += 1
            if match_count == 1:
                break

        del sp.min_datasets[:notMatch_count]

        data_count = 0
        first_count = 0
        first_data = None
        day_count = 0
        for minData in sp.min_datasets:
            minData = minData.text
            data_count += 1
            data_count -= month
            if data_count == 0 or data_count % 12 == 0:
                day_count += 1
                first_count += 1
                if first_count == 1 and re.search('\d+.\d', minData) != None:
                    first_data = minData
                else:
                    first_data = 12.5

                if re.search('\d+.\d', minData) == None:
                    minData = first_data
                print(str(day_count)+'日', minData, str(month) + "月のデータ")
                try:
                    self.minData_list.append(float(minData))
                except:
                    minData = first_data
                    self.minData_list.append(float(minData))
            else:
                pass
            data_count += month
            if day_count == 28:
                    break
        print('------------------')

    def MaxFourAve(self):
        data_count = 0
        ave_data = 0
        for maxData in self.maxData_list:
            data_count += 1
            ave_data += maxData
            if data_count % 7 == 0:
                ave = ave_data / 7
                self.maxAve_list.append(ave)
                #print(ave)
                ave_data = 0


    def MinFourAve(self):
        data_count = 0
        ave_data = 0
        for minData in self.minData_list:
            data_count +- 1
            ave_data += minData
            if data_count % 7 == 0:
                ave = ave_data / 7
                self.minAve_list.append(ave)
                #print(ave)
                ave_data = 0

    def DataSave(self):
        for (maxAve, minAve) in zip(self.maxAve_list, self.minAve_list):
            if year.index_num == 0:
                output.canberra_max_list.append(maxAve)
                output.canberra_min_list.append(minAve)
            elif year.index_num == 1:
                output.sydney_max_list.append(maxAve)
                output.sydney_min_list.append(minAve)
            elif year.index_num == 2:
                output.melbourne_max_list.append(maxAve)
                output.melbourne_min_list.append(minAve)
            elif year.index_num == 3:
                output.adelaide_max_list.append(maxAve)
                output.adelaide_min_list.append(minAve)
            elif year.index_num == 4:
                output.brisbane_max_list.append(maxAve)
                output.brisbane_min_list.append(minAve)
            else:
                print('エラー')

    def FiveMaxListCreate(self):
        for (a, b, c, d, e) in zip(output.canberra_max_list, output.sydney_max_list, output.melbourne_max_list, output.adelaide_max_list, output.brisbane_max_list):
            fiveAve = a+b+c+d+e
            output.fiveCity_max_aveList.append(fiveAve / 5)
            print(fiveAve)

    def FiveMinListCreate(self):
        for (a, b, c, d, e) in zip(output.canberra_min_list, output.sydney_min_list, output.melbourne_min_list, output.adelaide_min_list, output.brisbane_min_list):
            fiveAve = a+b+c+d+e
            output.fiveCity_min_aveList.append(fiveAve / 5)
            print(fiveAve)

class Roop():
    def __init__(self):
        self.breakPoint = None

    def roopMethod(self):
        '''
        year.url_year += 1
        if year.index_num == 4 and year.url_year == 2020:
            self.breakPoint = '終了'
            return self.breakPoint
        elif year.url_year == 2020:
            year.url_year = 2010
            year.index_num += 1
        else:
            pass
        '''
        year.index_num += 1
        if year.index_num == 5:
            self.breakPoint = '終了'
            return self.breakPoint
        else:
            pass

year = Year()
output = outputList()
driver = webdriver.Chrome('')

while True:
    url_list = urlList()
    sp = Scraping()

    sp.MaxHtmlParser()
    sp.MinHtmlParser()

    calc = Calc()
    for i in range(12):
        calc.MaxDataMonthly(i+1)
        calc.MinDataMonthly(i+1)

    calc.MaxFourAve()
    calc.MinFourAve()

    calc.DataSave()

    roop = Roop()
    if roop.roopMethod() == '終了':
        break

calc.FiveMaxListCreate()
calc.FiveMinListCreate()

##エクセル書き込み処理
path = ''
book = openpyxl.load_workbook(path)
sheet = book['']

xl_count = 2

for (a, b, c, d, e, f, g, h, i, j, k, l) in zip(output.canberra_max_list, output.canberra_min_list, output.sydney_max_list, output.sydney_min_list, output.melbourne_max_list, output.melbourne_min_list, output.adelaide_max_list, output.adelaide_min_list, output.brisbane_max_list, output.brisbane_min_list, output.fiveCity_max_aveList, output.fiveCity_min_aveList):
    sheet['D' + str(xl_count)] = a
    sheet['E' + str(xl_count)] = b
    sheet['F' + str(xl_count)] = c
    sheet['G' + str(xl_count)] = d
    sheet['H' + str(xl_count)] = e
    sheet['I' + str(xl_count)] = f
    sheet['J' + str(xl_count)] = g
    sheet['K' + str(xl_count)] = h
    sheet['L' + str(xl_count)] = i
    sheet['M' + str(xl_count)] = j
    sheet['N' + str(xl_count)] = k
    sheet['O' + str(xl_count)] = l
    xl_count += 1

book.save(path)
































