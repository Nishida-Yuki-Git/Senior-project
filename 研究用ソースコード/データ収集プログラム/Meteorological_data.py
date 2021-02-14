'''
Created on 2020/10/17

@author: nishidayuki
'''

import requests
from bs4 import BeautifulSoup
import re
import openpyxl

class Time():
    def __init__(self, year, month):
        self.year = year
        self.month = month

class Urlvariable(Time): # ループに使うURL用の変数リスト格納クラス
    def __init__(self, year, month, Ken_count):
        super().__init__(year, month)
        self.Ken_count = Ken_count

class ImportantList(): # 重要な県データ
    def __init__(self):
        self.Ken_name = ['北海道', '青森', '秋田', '岩手', '山形', '宮城', '福島', '新潟', '茨城', '千葉', '栃木', '群馬', '東京', '神奈川', '山梨', '長野', '静岡', '富山', '岐阜', '石川', '愛知', '三重', '京都', '奈良', '大阪', '和歌山', '兵庫', '鳥取', '岡山', '香川', '徳島', '島根', '広島', '高知', '愛媛', '山口', '大分', '宮崎', '熊本', '佐賀', '長崎', '鹿児島', '沖縄']
        self.no_list = [14, 31, 32, 33, 35, 34, 36, 54, 40, 45, 41, 42, 44, 46, 49, 48, 50, 55, 52, 56, 51, 53, 61, 64, 62, 65, 63, 69, 66, 72, 71, 68, 67, 74, 73, 81, 83, 87, 86, 85, 84, 88, 91]
        self.block_list = [47412, 47575, 47582, 47584, 47588, 47590, 47595, 47604, 47629, 47682, 47615, 47624, 47662, 47670, 47638, 47610, 47656, 47607, 47632, 47605, 47636, 47651, 47759, 47780, 47772, 47777, 47770, 47746, 47768, 47891, 47895, 47741, 47765, 47893, 47887, 47784, 47815, 47830, 47819, 47813, 47817, 47827, 47936]

class OutputList(): # エクセル記述に使用するデータ格納リスト
    def __init__(self):
        self.temp_output_list = [] # 気温
        self.rh_output_list = [] # 相対湿度
        self.ab_hu_output_list = [] # 絶対湿度

class Clowling(): # URLを操作
    def __init__(self):
        self.temp_datasets = None
        self.rh_datasets = None
        self.main_clowling_url = 'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=' + str(ken.no_list[url.Ken_count]) + '&block_no=' + str(ken.block_list[url.Ken_count]) + '&year=' + str(url.year) + '&month=' + str(url.month) + '&day=1&view=a2'

    def UrlRequest(self):
        response = requests.get(self.main_clowling_url)
        response.encoding = response.apparent_encoding
        return response

    def HtmlParser(self):
        bs = BeautifulSoup(self.UrlRequest().text, 'html.parser')
        self.temp_datasets = bs.select('td.data_0_0') #気温
        self.rh_datasets = bs.select('td.data_0_0') # 相対湿度

class Calc(): # データを抽出して計算->OutputListへ
    def __init__(self):
        self.temp_list = [] # 平均気温
        self.rh_list = [] # 相対湿度
        self.ab_hu_list = [] # 絶対湿度

    def TempDataScraping(self):
        first_data = 0 # 欠損補完データ
        first_count = 0
        count = 0
        for temp_data in clowl.temp_datasets:
            count += 1
            count -= 10
            if count == 0 or count % 18 == 0:
                temp = re.search('.*\d+.\d', temp_data.text)
                if temp is not None:
                    temp = temp.group()
                    print(ken.Ken_name[url.Ken_count] + str(url.year) + str(url.month), '気温', temp)
                    first_count += 1
                    if first_count == 1:
                        first_data += float(temp)
                    else:
                        pass
                elif temp is None:
                    print(' ')
                    print(ken.Ken_name[url.Ken_count] + str(url.year) + str(url.month))
                    print(temp_data)
                    print(' ')
                    temp = first_data
                self.temp_list.append(temp)
            else:
                pass
            count += 10

    def RhDataScraping(self):
        first_data = 0 # 欠損補完データ
        first_count = 0
        count = 0
        for rh_data in clowl.rh_datasets:
            count += 1
            count -= 16
            if count == 0 or count % 18 == 0 and rh_data is not None:
                rh = re.search('\d+', rh_data.text)
                if rh is not None:
                    rh = rh.group()
                    print(ken.Ken_name[url.Ken_count] + str(url.year) + str(url.month), '相対湿度', rh)
                    first_count += 1
                    if first_count == 1:
                        first_data += float(rh)
                    else:
                        pass
                elif rh is None:
                    print(' ')
                    print(ken.Ken_name[url.Ken_count] + str(url.year) + str(url.month))
                    print(rh_data)
                    print(' ')
                    rh = first_data
                self.rh_list.append(rh)
            else:
                pass
            count += 16

    def AbHumidCalc(self):
        for (temp, rh) in zip(self.temp_list, self.rh_list):
            ab_hu = 217 * (6.1078 * (10 ** (7.5 * float(temp) / (float(temp) + 237.3)))) / (float(temp) + 273.15) * (int(rh) / 100)
            self.ab_hu_list.append(ab_hu)

    def OutputData(self):
        data_count = 0 # データの数を一日ごとにカウント
        temp_ave = 0 # 気温の平均データ
        rh_ave = 0 # 相対湿度の平均データ
        ab_hu_ave = 0 # 絶対湿度の平均データ
        for (temp, rh, ab_hu) in zip(self.temp_list, self.rh_list, self.ab_hu_list):
            data_count += 1
            temp_ave += float(temp)
            rh_ave += int(rh)
            ab_hu_ave += float(ab_hu)
            if data_count == 29:
                break
            elif data_count % 7 == 0:
                output.temp_output_list.append(temp_ave / 7)
                output.rh_output_list.append(rh_ave / 7)
                output.ab_hu_output_list.append(ab_hu_ave / 7)
                temp_ave = 0
                rh_ave = 0
                ab_hu_ave = 0
            else:
                pass

class Roop(): # ループ処理
    def __init__(self):
        self.end = None
    def YearMonthMethod(self):
        url.month += 1
        if url.Ken_count == 42 and url.year == 2019 and url.month == 13:
            self.end = '終了'
        elif url.year == 2019 and url.month == 13:
            url.Ken_count += 1
            url.year = 2010
            url.month = 1
        elif url.month == 13:
            url.year += 1
            url.month = 1
        else:
            pass

##メイン処理
url = Urlvariable(2010, 1, 0) # ループ用変数
ken = ImportantList() # 重要リスト
output = OutputList() # 出力リスト
while True:
    clowl = Clowling() # クローリング処理
    clowl.HtmlParser()

    calc = Calc() # 計算処理
    calc.TempDataScraping()
    calc.RhDataScraping()
    calc.AbHumidCalc()
    calc.OutputData()

    roop = Roop() # ループ処理
    roop.YearMonthMethod()
    if roop.end == '終了':
        print(roop.end)
        break

# エクセル書き込み
path = ''
book = openpyxl.load_workbook(path)
sheet = book['']

data_count = 0 # データの個数をカウント
xl_count = 4 # データのセル行をカウント
ken_name_count = 0 # 県名リストのアクセス番号
year_count = 2010
month_count = 1
week_count = 1

for (temp, rh, ab_hu) in zip(output.temp_output_list, output.rh_output_list, output.ab_hu_output_list):
    data_count += 1
    if data_count == 1:
        ##項目を記入
        sheet['A' + str(xl_count)] = ken.Ken_name[ken_name_count]
        ken_name_count += 1

        sheet['B' + str(xl_count - 1)] = '年'
        sheet['C' + str(xl_count - 1)] = '月・週'
        sheet['D' + str(xl_count - 1)] = '外気温(℃)'
        sheet['E' + str(xl_count - 1)] = '相対湿度(%)'
        sheet['F' + str(xl_count - 1)] = '絶対湿度(g/kg)'
        sheet['G' + str(xl_count - 1)] = 'IF感染者数(人)'

    if month_count == 1 and week_count == 1:
        sheet['B' + str(xl_count)] = str(year_count) + '年'
        year_count += 1
        if year_count == 2020:
            year_count = 2010

    # 日付を記入
    sheet['C' + str(xl_count)] = str(month_count) + '月' + '第' + str(week_count) + '週'
    week_count += 1
    if week_count == 5:
        month_count += 1
        if month_count == 13:
            month_count = 1
        week_count = 1

    # データ記入
    temp = '{:.1f}'.format(temp)
    rh = '{:.1f}'.format(rh)
    ab_hu = '{:.1f}'.format(ab_hu)

    sheet['D' + str(xl_count)] = temp
    sheet['E' + str(xl_count)] = rh
    sheet['F' + str(xl_count)] = ab_hu

    xl_count += 1

    if data_count == 480: # 480個ごとに区切っていく
        data_count = 0
        xl_count += 3

book.save(path)










































