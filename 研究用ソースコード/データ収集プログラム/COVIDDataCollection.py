'''
Created on 2020/11/06

@author: nishidayuki
'''

#コロナデータ収集プログラム
from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS
import re
import openpyxl

class Collection(): # データ収集クラス, インスタンス->collec
    def __init__(self, chromeDriver):
        self.chromeDriver = chromeDriver
        self.pref = [] # 県リスト
        self.month = [] # 月リスト
        self.day = [] # 日リスト
        self.infected = [] # 総感染者リスト
        self.newInfected = [] # 新規感染者数リスト
        self.population = [] # 人口リスト
        self.perHundredThousandPeople = [] #人口10万人あたりの総感染者数リスト
        self.newPerHundredThousand = [] # 人口10万人あたりの新規感染者数リスト

    def Analysis(self):
        page_source = self.chromeDriver.page_source
        soup = BS(page_source, 'html.parser')
        covid_text = soup.select('td.ember-view')
        return covid_text

class dataOrganization(): # データ整理クラス, インスタンス->do
    def __init__(self):
        self.covid_datasets = None # 成形前元データ
        self.pref_data_list = [] # 県リスト
        self.month_data_list = [] # 月リスト
        self.day_data_list = [] # 日リスト
        self.infected_data_list = [] # 総感染者リスト
        self.newInfected_data_list = [] # 新規感染者数リスト
        self.population_data_list = [] # 人口リスト
        self.perHundredThousandPeople_data_list = [] #人口10万人あたりの総感染者数リスト
        self.newPerHundredThousand_data_list = [] # 人口10万人あたりの新規感染者数リスト

    def extractAll(self): # 抽出した素材を保存
        self.covid_datasets = collec.Analysis()

    def prefectureExtraction(self): # 県データを全て抽出
        count = 0
        for pref_data in self.covid_datasets:
            count += 1
            count -= 3
            if count == 0 or count % 19 == 0:
                pref = re.match('\S+', pref_data.text)
                pref = pref.group()
                self.pref_data_list.append(pref)
            count += 3

    def monthExtraction(self): # 月データを全て抽出
        count = 0
        for month_data in self.covid_datasets:
            count += 1
            count -= 6
            if count == 0 or count % 19 == 0:
                month = re.match('\S+', month_data.text)
                month = month.group()
                self.month_data_list.append(month)
            count += 6

    def dayExtraction(self): # 日データを全て抽出
        count = 0
        for day_data in self.covid_datasets:
            count += 1
            count -= 7
            if count == 0 or count % 19 == 0:
                day = re.match('\S+', day_data.text)
                day = day.group()
                self.day_data_list.append(day)
            count += 7

    def infectedPeopleExtraction(self): # 感染者数データを全て抽出
        count = 0
        for infected_data in self.covid_datasets:
            count += 1
            count -= 8
            if count == 0 or count % 19 == 0:
                infected = re.match('\S+', infected_data.text)
                infected = infected.group()
                self.infected_data_list.append(infected)
            count += 8

    def newInfedctedExtraction(self): # 新規感染者数データを全て抽出
        count = 0
        for newInfected_data in self.covid_datasets:
            count += 1
            count -= 13
            if count == 0 or count % 19 == 0:
                newInfected = re.match('\S+', newInfected_data.text)
                if newInfected is None:
                    newInfected = 0
                else:
                    newInfected = newInfected.group()
                self.newInfected_data_list.append(newInfected)
            count += 13

    def perHundredThousandPeopleExtraction(self): # 人口10万人あたりの感染者数を抽出
        count = 0
        for people10_data in self.covid_datasets:
            count += 1
            count -= 18
            if count == 0 or count % 19 == 0:
                people10 = re.match('\S+', people10_data.text)
                people10 = people10.group()
                self.perHundredThousandPeople_data_list.append(people10)
            count += 18

    def newPerHundredThousandCalc(self): # 人口10万人あたりの新規感染者数を算出する
        new_infected_count = 0
        population_count = 0
        newInfected_list = []
        population_list = []
        for newInfected_data in self.covid_datasets:
            new_infected_count += 1
            new_infected_count -= 13
            if new_infected_count == 0 or new_infected_count % 19 == 0:
                newInfected = re.match('\S+', newInfected_data.text)
                if newInfected is None:
                    newInfected = 0
                else:
                    newInfected = newInfected.group()
                newInfected_list.append(newInfected)
            new_infected_count += 13
        for population_data in self.covid_datasets:
            population_count += 1
            population_count -= 17
            if population_count == 0 or population_count % 19 == 0:
                population = re.match('\S+', population_data.text)
                population = population.group()
                population_list.append(population)
            population_count += 17
        for (newInfected, population) in zip(newInfected_list, population_list):
            newPerHundredThousand = (float(newInfected) * 100000) / float(population)
            self.population_data_list.append(population)
            self.newPerHundredThousand_data_list.append(newPerHundredThousand)

class dateAnalysis(): # 月日解析クラス, インスタンス->date
    def __init__(self):
        self.pref_list = [] # 県リスト
        self.month_list = [] # 月リスト
        self.day_list = [] # 日リスト
        self.infected_list = [] # 総感染者リスト
        self.newInfected_list = [] # 新規感染者数リスト
        self.population_list = [] # 人口リスト
        self.perHundredThousandPeople_list = [] #人口10万人あたりの総感染者数リスト
        self.newPerHundredThousand_list = [] # 人口10万人あたりの新規感染者数リスト

    def monthAnalysisMethod(self):
        index_num_list = []
        index_count = 0
        for month in do.month_data_list: # まずは条件外の番号を調べていく
            if int(month) <= 3 or 11 <= int(month):
                index_num_list.append(index_count)
            index_count += 1
        for num in index_num_list:
            do.pref_data_list[num] = 'こんにちは'
            do.month_data_list[num] = 'こんにちは'
            do.day_data_list[num] = 'こんにちは'
            do.infected_data_list[num] = 'こんにちは'
            do.newInfected_data_list[num] = 'こんにちは'
            do.population_data_list[num] = 'こんにちは'
            do.perHundredThousandPeople_data_list[num] = 'こんにちは'
            do.newPerHundredThousand_data_list[num] = 'こんにちは'
        self.pref_list = [i for i in do.pref_data_list if i != 'こんにちは']
        self.month_list = [i for i in do.month_data_list if i != 'こんにちは']
        self.day_list = [i for i in do.day_data_list if i != 'こんにちは']
        self.infected_list = [i for i in do.infected_data_list if i != 'こんにちは']
        self.newInfected_list = [i for i in do.newInfected_data_list if i != 'こんにちは']
        self.population_list = [i for i in do.population_data_list if i != 'こんにちは']
        self.perHundredThousandPeople_list = [i for i in do.perHundredThousandPeople_data_list if i != 'こんにちは']
        self.newPerHundredThousand_list = [i for i in do.newPerHundredThousand_data_list if i != 'こんにちは']

    def dayAnalysisMethod(self):
        index_num_list = []
        index_count = 0
        for day in self.day_list:
            if 29 <= int(day):
                index_num_list.append(index_count)
            index_count += 1
        for num in index_num_list:
            self.pref_list[num] = 'こんにちは'
            self.month_list[num] = 'こんにちは'
            self.day_list[num] = 'こんにちは'
            self.infected_list[num] = 'こんにちは'
            self.newInfected_list[num] = 'こんにちは'
            self.population_list[num] = 'こんにちは'
            self.perHundredThousandPeople_list[num] = 'こんにちは'
            self.newPerHundredThousand_list[num] = 'こんにちは'
        self.pref_list = [i for i in self.pref_list if i != 'こんにちは']
        self.month_list = [i for i in self.month_list if i != 'こんにちは']
        self.day_list = [i for i in self.day_list if i != 'こんにちは']
        self.infected_list = [i for i in self.infected_list if i != 'こんにちは']
        self.newInfected_list = [i for i in self.newInfected_list if i != 'こんにちは']
        self.population_list = [i for i in self.population_list if i != 'こんにちは']
        self.perHundredThousandPeople_list = [i for i in self.perHundredThousandPeople_list if i != 'こんにちは']
        self.newPerHundredThousand_list = [i for i in self.newPerHundredThousand_list if i != 'こんにちは']

class dataPrint(): # 出力クラス, インスタンス->dp
    def __init__(self):
        pass

    def dataPrintMethod(self):
        ken_list = ['鹿児島県', '沖縄県']
        for (pref, month, day, infected, newInfected, people, perH, newPer) in zip(date.pref_list, date.month_list, date.day_list, date.infected_list, date.newInfected_list, date.population_list, date.perHundredThousandPeople_list, date.newPerHundredThousand_list):
            #print(pref, month, day, infected, newInfected, people, perH, newPer)
            if pref == '宮崎県':
                continue
            else:
                print(day)
                collec.pref.append(pref)
                collec.month.append(month)
                collec.day.append(day)
                collec.infected.append(infected)
                collec.newInfected.append(newInfected)
                collec.population.append(people)
                collec.perHundredThousandPeople.append(perH)
                collec.newPerHundredThousand.append(newPer)
            if pref == '沖縄県' and month == '10' and day == '31':
                breakPoint = '終了'
                return breakPoint

class Click(): # インスタンス->click(このクラスで、breakさせるための処理を実装)
    def __init__(self):
        pass

    def clickAction(self):
        click_button = collec.chromeDriver.find_element_by_link_text('›')
        click_button.click()

    def timeSleep(self):
        time.sleep(2)

#Chrome立ち上げ
driver = webdriver.Chrome('')

page_count = 0
url = 'https://coronavirus-esrijapan-ej.hub.arcgis.com/datasets/全期間・検査陽性者の状況別集計（ポイント版・都道府県別）/data?page=' + str(page_count)
driver.get(url)

time.sleep(15)

#固定インスタンス
collec = Collection(driver)

#ループ処理
while True:
    do = dataOrganization()
    do.extractAll()
    do.prefectureExtraction()
    do.monthExtraction()
    do.dayExtraction()
    do.infectedPeopleExtraction()
    do.newInfedctedExtraction()
    do.perHundredThousandPeopleExtraction()
    do.newPerHundredThousandCalc()

    date = dateAnalysis()
    date.monthAnalysisMethod()
    #date.dayAnalysisMethod()

    dp = dataPrint()
    if dp.dataPrintMethod() == '終了':
        print('収集完了')
        break
    else:
        pass

    click = Click()

    click.clickAction()
    click.timeSleep()

#下にエクセル処理など
path = ''
book = openpyxl.load_workbook(path)
sheet = book['']
xl_count = 0
for (infected, newInfected, people, perH, newPer) in zip(collec.infected, collec.newInfected, collec.population, collec.perHundredThousandPeople, collec.newPerHundredThousand):
    sheet['I' + str(xl_count)] = infected
    sheet['J' + str(xl_count)] = newInfected
    sheet['K' + str(xl_count)] = people
    sheet['L' + str(xl_count)] = perH
    sheet['M' + str(xl_count)] = newPer
    xl_count += 1
book.save(path)








