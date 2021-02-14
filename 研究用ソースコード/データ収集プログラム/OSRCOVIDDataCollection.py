'''
Created on 2020/12/18

@author: nishidayuki
'''

##オーストラリア新型コロナウイルス感染者数データ収集
import urllib.request as req
import os.path
import json
import openpyxl

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Date(): # 日付クラス->date
    def __init__(self):
        self.month_list = ['06', '07', '08', '09', 10, 11]
        self.day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        self.month_num = 0
        self.day_num = 0

    def monthTypeAnalysis(self): # 月リストの中身のtypeを解析
        month = self.month_list[self.month_num]
        if type(month) == int:
            month = str(month)
        else:
            pass
        return month

    def dayTypeAnalysis(self): # 日リストの中身のtypeを解析
        day = self.day_list[self.day_num]
        if type(day) == int:
            day = str(day)
        else:
            pass
        return day

class Url(): # urlクラス->url
    def __init__(self):
        self.json_url = 'https://opendata.corona.go.jp/api/OccurrenceStatusOverseas?date=2020' + date.monthTypeAnalysis() + date.dayTypeAnalysis()

    def saveJson(self): # jsonファイルをローカルに保存していく
        savename = '/Users/nishidayuki/Desktop/新型コロナ関連研究/オーストラリア/コロナデータ/' +  date.monthTypeAnalysis() + date.dayTypeAnalysis() + '.json'
        if not os.path.exists(savename):
            req.urlretrieve(self.json_url, savename)
        return savename

class dataSave(): # データ保存
    def __init__(self):
        self.infectedNum_list = [] # 累計感染者数
        self.deceasedNum_list = [] # 死亡者数

class sytemPrint(): # 出力クラス->system_print
    def __init__(self):
        pass

    def jsonAnalysis(self): # 保存したローカルのjsonファイルを解析
        s = open(url.saveJson(), 'r', encoding='utf-8')
        data = json.load(s)
        return data

    def jsonPrint(self): # データ保存と出力確認
        j = self.jsonAnalysis()
        item_list = j['itemList']
        for i in item_list:
            if i['dataName'] == '豪州':
                infected = i['infectedNum']
                dead = i['deceasedNum']
                data_save.infectedNum_list.append(infected)
                data_save.deceasedNum_list.append(dead)

class Roop(): # ループ処理クラス->roop
    def __init__(self):
        self.breakPoint = None # ループ終了

    def roopMethod(self): # 日付リストのインデックス番号を操作
        date.day_num += 1
        if date.month_num == 5 and date.day_num == 31:
            self.breakPoint = '終了'
            return self.breakPoint
        elif date.day_num == 31:
            date.day_num = 0
            date.month_num += 1
        else:
            pass


#メイン処理
date = Date() # 日付クラス
data_save = dataSave() # エクセル書き込み用データ
while True:
    url = Url() #urlクラス
    system_print = sytemPrint() # 出力クラス

    try:
        system_print.jsonPrint()
    except:
        pass

    roop = Roop() # ループ処理クラス
    if roop.roopMethod() == '終了':
        print('終了です')
        break


#エクセル書き込み処理
path = ''
book = openpyxl.load_workbook(path)
sheet = book['']
xl_count = 2
for (infected, dead) in zip(data_save.infectedNum_list, data_save.deceasedNum_list):
    sheet['T' + str(xl_count)] = infected
    sheet['U' + str(xl_count)] = dead
    xl_count += 1
book.save(path)
