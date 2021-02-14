'''
Created on 2020/10/25

@author: nishidayuki
'''

import csv
import math
import os
import numpy as np

class Data(): # データクラス
    def __init__(self):
        self.temp_data_list = []
        self.IF_data_list = []

class Average(): # 平均クラス
    def __init__(self):
        self.temp_ave = None
        self.IF_ave = None

    def averageCalc(self):
        temp_total = 0
        IF_total = 0
        for (temp, IF) in zip(data.temp_data_list, data.IF_data_list):
            temp_total += float(temp)
            IF_total += float(IF)
        self.temp_ave = temp_total / len(data.temp_data_list)
        self.IF_ave = IF_total / len(data.IF_data_list)

class Deviation(): # 偏差クラス
    def __init__(self):
        self.temp_deviation_list = []
        self.IF_deviation_list = []

    def deviationCalc(self):
        for (temp, IF) in zip(data.temp_data_list, data.IF_data_list):
            self.temp_deviation_list.append(float(temp) - float(ave.temp_ave))
            self.IF_deviation_list.append(float(IF) - float(ave.IF_ave))

class Dispersion(): # 分散クラス
    def __init__(self):
        self.S_temp2 = None
        self.S_IF2 = None

    def dispersionCalc(self):
        temp = 0
        IF = 0
        for (temp_dev, IF_dev) in zip(dev.temp_deviation_list, dev.IF_deviation_list):
            temp += float(temp_dev) * float(temp_dev)
            IF += float(IF_dev) * float(IF_dev)
        self.S_temp2 = temp / len(dev.temp_deviation_list)
        self.S_IF2 = IF / len(dev.IF_deviation_list)

class standardDeviation(): # 標準偏差クラス
    def __init__(self):
        self.S_temp = None
        self.S_IF = None

    def standardDevationCalc(self):
        self.S_temp = math.sqrt(disp.S_temp2)
        self.S_IF = math.sqrt(disp.S_IF2)

class Covariance(): # 共分散クラス
    def __init__(self):
        self.S_temp_IF = None

    def covarianceCalc(self):
        dev_total = 0
        for (temp_dev, IF_dev) in zip(dev.temp_deviation_list, dev.IF_deviation_list):
            dev_total += float(temp_dev) * float(IF_dev)
        self.S_temp_IF = dev_total / len(dev.temp_deviation_list)

class regressionLine(): # 回帰直線クラス
    def __init__(self):
        self.inclination = None
        self.intercept = None

    def inclinationCalc(self):
        inc = float(co.S_temp_IF) / float(disp.S_temp2)
        self.inclination = inc

    def interceptCalc(self):
        itc = float(ave.IF_ave) - (((float(co.S_temp_IF) / float(disp.S_temp2))) * float(ave.temp_ave))
        self.intercept = itc

    def regressionLinePrint(self, path):
        self.inclination = '{:.4f}'.format(float(self.inclination))
        self.intercept = '{:.4f}'.format(float(self.intercept))
        print(' ')
        print('-----------------------------------')
        print(os.path.basename(path).split('.', 1)[0]) # ファイル名
        print('回帰直線')
        print('y = ' + str(self.inclination) + 'x + ' + str(self.intercept))

class Coefficient(): # 係数クラス
    def __init__(self):
        self.correlation_coef = None # 相関係数
        self.determination_coef = None # 決定係数

    def correlationCalc(self):
        r = float(co.S_temp_IF) / (float(sd.S_temp) * float(sd.S_IF))
        self.correlation_coef = r
        return r

    def determinationCalc(self):
        rr = float(self.correlationCalc()) * float(self.correlationCalc())
        self.determination_coef = rr

    def coefPrint(self):
        self.correlation_coef = '{:.4f}'.format(float(self.correlation_coef))
        self.determination_coef = '{:.4f}'.format(float(self.determination_coef))
        print('相関係数')
        print(self.correlation_coef)
        print('決定係数')
        print(self.determination_coef)
        print('-----------------------------------')

##二次曲線回帰クラス
class Exponentiation(): # 冪乗クラス
    def __init__(self):
        self.x_0_sum = None
        self.x_1_sum = None
        self.x_2_sum = None
        self.x_3_sum = None
        self.x_4_sum = None

    def XZeroCalc(self):
        x_zeroList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_zeroList.append(dt ** (0))
        for i in x_zeroList:
            dataSum += i
        self.x_0_sum = dataSum

    def XOneCalc(self):
        x_oneList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_oneList.append(dt ** (1))
        for i in x_oneList:
            dataSum += i
        self.x_1_sum = dataSum

    def XTwoCalc(self):
        x_twoList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_twoList.append(dt ** (2))
        for i in x_twoList:
            dataSum += i
        self.x_2_sum = dataSum

    def XThreeCalc(self):
        x_threeList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_threeList.append(dt ** (3))
        for i in x_threeList:
            dataSum += i
        self.x_3_sum = dataSum

    def XFourCalc(self):
        x_fourList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_fourList.append(dt ** (4))
        for i in x_fourList:
            dataSum += i
        self.x_4_sum = dataSum

class XYmultiplication(): # xyを求めるクラス
    def __init__(self):
        self.xy_0_sum = None
        self.xy_1_sum = None
        self.xy_2_sum = None
        self.xy_list = []

    def XYZeroCalc(self):
        x_zeroList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_zeroList.append(dt ** (0))
        for i, j in zip(x_zeroList, data.IF_data_list):
            dataSum += (i * j)
        self.xy_0_sum = dataSum
        self.xy_list.append(dataSum)

    def XYOneCacl(self):
        x_oneList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_oneList.append(dt ** (1))
        for i, j in zip(x_oneList, data.IF_data_list):
            dataSum += (i * j)
        self.xy_1_sum = dataSum
        self.xy_list.append(dataSum)

    def XYTwoCacl(self):
        x_twoList = []
        dataSum = 0
        for dt in data.temp_data_list:
            x_twoList.append(dt ** (2))
        for i, j in zip(x_twoList, data.IF_data_list):
            dataSum += (i * j)
        self.xy_2_sum = dataSum
        self.xy_list.append(dataSum)

class InverseMatrix(): # 逆行列の計算クラス
    def __init__(self):
        self.matrix_list = [] # 逆行列の値リスト

    def MatrixCalc(self):
        a_list = [[ex.x_0_sum, ex.x_1_sum, ex.x_2_sum], [ex.x_1_sum, ex.x_2_sum, ex.x_3_sum], [ex.x_2_sum, ex.x_3_sum, ex.x_4_sum]]
        inv_a = np.linalg.inv(a_list)
        for i in inv_a:
            self.matrix_list.append(i[0])
            self.matrix_list.append(i[1])
            self.matrix_list.append(i[2])

class CurveCalc(): # 二次曲線の計算クラス
    def __init__(self):
        self.a0 = None
        self.a1 = None
        self.a2 = None

    def curveCalcMethod(self):
        xy_index_list = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        a0_num = 0
        a1_num = 0
        a2_num = 0
        for i, j in zip(range(0, 9), xy_index_list):
            if i in range(0, 7, 3):
                a0_num += (Inverse.matrix_list[i] * multi.xy_list[j-1])
            elif i in range(1, 8, 3):
                a1_num += (Inverse.matrix_list[i] * multi.xy_list[j-1])
            elif i in range(2, 9, 3):
                a2_num += (Inverse.matrix_list[i] * multi.xy_list[j-1])
            else:
                print('エラー')
        self.a0 = a0_num
        self.a1 = a1_num
        self.a2 = a2_num

    def curvePrint(self):
        print('二次曲線')
        a0_new = '{:.4f}'.format(self.a0)
        a1_new = '{:.4f}'.format(self.a1)
        a2_new = '{:.4f}'.format(self.a2)
        print('y = ' + str(a2_new) + ' x^2 + (' + str(a1_new) + ') x + (' + str(a0_new) + ')')

class CurveCoef(): # 二次曲線の係数計算クラス
    def __init__(self):
        self.reg_variation = None # 回帰変動の値
        self.resi_fluc = None # 残差変動の値

    def RegressionVariationCalc(self): # 回帰変動
        reg_var_sum = 0
        for x in data.temp_data_list:
            pre_y = (float(curve.a2) * (x ** (2))) + (float(curve.a1) * x) + (float(curve.a0))
            reg_var_sum += ((pre_y - ave.IF_ave) ** (2))
        self.reg_variation = reg_var_sum

    def ResidualFluctuation(self): # 残差変動
        resi_sum = 0
        for data_x, data_y in zip(data.temp_data_list, data.IF_data_list):
            pre_y = (float(curve.a2) * (data_x ** (2))) + (float(curve.a1) * data_x) + (float(curve.a0))
            resi_sum += ((data_y - pre_y) ** (2))
        self.resi_fluc = resi_sum

    def DeterminationCoef(self): # 決定係数
        r2 = (self.reg_variation / (self.reg_variation + self.resi_fluc))
        r2 = '{:.4f}'.format(r2)
        print('決定係数')
        print(r2)
        print('-----------------------------------')
        print(' ')


#csvのパス
path_list = []

for path in path_list:
    data = Data() # データクラスのインスタンス
    ##CSV読み込み処理
    with open(path, encoding = "utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            data.temp_data_list.append(float(row[0]))
            data.IF_data_list.append(float(row[1]))

    ##単回帰分析インスタンス
    ave = Average() # 平均計算クラスのインスタンス
    dev = Deviation() # 偏差クラスのインスタンス
    disp = Dispersion() # 分散クラスのインスタンス
    sd = standardDeviation() # 標準偏差クラスのインスタンス
    co = Covariance() # 共分散クラスのインスタンス
    reg = regressionLine() # 回帰直線クラスのインスタンス
    coef = Coefficient() # 係数クラスのインスタンス

    ave.averageCalc()
    dev.deviationCalc()
    disp.dispersionCalc()
    sd.standardDevationCalc()
    co.covarianceCalc()
    reg.inclinationCalc()
    reg.interceptCalc()
    reg.regressionLinePrint(path)
    coef.determinationCalc()
    coef.coefPrint()


    #二次曲線回帰インスタンス
    ex = Exponentiation() # 冪乗クラス
    multi = XYmultiplication() # xyの掛け算クラス
    Inverse = InverseMatrix() # 逆行列の計算クラス
    curve = CurveCalc() # 二次曲線の計算クラス
    curve_coef = CurveCoef() # 二次曲線の係数クラス

    ex.XZeroCalc()
    ex.XOneCalc()
    ex.XTwoCalc()
    ex.XThreeCalc()
    ex.XFourCalc()
    multi.XYZeroCalc()
    multi.XYOneCacl()
    multi.XYTwoCacl()
    Inverse.MatrixCalc()
    curve.curveCalcMethod()
    curve.curvePrint()
    curve_coef.RegressionVariationCalc()
    curve_coef.ResidualFluctuation()
    curve_coef.DeterminationCoef()









