'''
Created on 2020/12/09

@author: nishidayuki
'''

##流動人口データ収集(内閣官房サイトから)
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
        self.json_url = 'https://opendata.corona.go.jp/api/ReductionRate?date=2020' + date.monthTypeAnalysis() + date.dayTypeAnalysis()

    def saveJson(self): # jsonファイルをローカルに保存していく
        savename = '/Users/nishidayuki/Desktop/新型コロナ関連研究/流動人口データ/' +  date.monthTypeAnalysis() + date.dayTypeAnalysis() + '.json'
        if not os.path.exists(savename):
            req.urlretrieve(self.json_url, savename)
        print(savename)
        if date.monthTypeAnalysis() == '06' and date.dayTypeAnalysis() == '04':
            for i in range(47):
                data_save.preDay_list.append(' ')
                data_save.preDec_list.append(' ')
                data_save.preSp_list.append(' ')
        return savename

class dataSave(): # データ保存
    def __init__(self):
        self.preDay_list = [] # 前日との比較
        self.preDec_list = [] # 緊急事態宣言前との比較
        self.preSp_list = [] # 感染拡大前との比較

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
        data_count = 0
        text_count = 0
        check_string1 = None
        check_string2 = None
        for i in item_list:
            day = i['date']
            pref = i['dataName']
            pre_day = i['comparisonPreDay']
            pre_dec = i['comparisonPreDeclare']
            pre_sp = i['comparisonPreSpread']
            for i in range(0, len(pref) - 3 + 1):
                text_count += 1
                if text_count == 1:
                    check_string2 = pref[i : i + 3]
            text_count = 0
            if check_string2 == check_string1: # 重複が発見された場合
                pass
            else:
                for i in range(0, len(pref) - 3 + 1):
                    text_count += 1
                    if text_count == 1:
                        check_string1 = pref[i : i + 3]
                text_count = 0
                data_count += 1
                data_save.preDay_list.append(float(pre_day))
                data_save.preDec_list.append(float(pre_dec))
                data_save.preSp_list.append(float(pre_sp))

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
file_count = 0
while True:
    url = Url() #urlクラス
    system_print = sytemPrint() # 出力クラス

    try:
        system_print.jsonPrint()
        file_count += 1
        print(file_count)
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
first_xl = 0
pref_count = 0
data_count = 0
for i in range(len(data_save.preDay_list)):
    data_count += 1
    pref_count += 1
    sheet['I' + str(xl_count)] = data_save.preDay_list[int(i)]
    sheet['J' + str(xl_count)] = data_save.preDec_list[int(i)]
    sheet['K' + str(xl_count)] = data_save.preSp_list[int(i)]
    xl_count += 183
    if pref_count == 47:
        pref_count = 0
        first_xl += 1
        xl_count = 0
        xl_count = first_xl + 2
print(data_count)
book.save(path)











