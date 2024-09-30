# -*- coding: utf-8 -*-
#基本的な関数
#bunpu3用のスクリプト
#
#
#Basic Functions
#
#
#
#from bunpu import *



#1D

#諸元（最小値、最大値、平均値、標準偏差、生成ファイル名）をして1D分布を作成
#Create a distribution from parametar(min,max,mean,)

#v1=bunpu()
#最小値、最大値、平均値、標準偏差、生成ファイル名
v1.bunpu_gene([10],[50],[40],[5],[100])

#z1=bunpu()
z1.bunpu_gene([5],[60],[20],[5],[100])

#ファイルのデータから1D分布を作成する
#Create a distribution from data in a file
#x=bunpu()
#データ抽出するファイル名、生成するグラフ名、無視する行数、抽出する行、最小から最大の間を分割する分割数
x.bunpu_data('kmbday.csv','kmbday',1,[1],[300])
#y=bunpu()
y.bunpu_data('kmbtime.csv','kmbtime',1,[1],[300])

#分布の平均値を出力、
#グラフ名、グラフ出力有無、２次元以上のグラフの視点
meanx = x.bunpu_mean('xmean',1,1)
#分布の平均値をコンソールに表示
print('xmean',meanx)

meanv = v1.bunpu_mean('v1mean',1,1)
print('vmean',meanv)

#相互に独立な分布の加算
#w0=bunpu()
#w0:加算後の分布,x,v1:加算対象の分布
w0=x.bunpu_add(v1)
#グラフの生成
w0.bunpu_graph('w0')
#分布の平均値を出力、
meanw0 = w0.bunpu_mean('w0mean',1,1)
print('w0mean',meanw0)

#相関係数0.5の分布間での加算
#w1=bunpu()
w1=x.bunpu_add(v1,[100],[0.5])
w1.bunpu_graph('w1')
#分布の平均値を出力、
meanw1 = w1.bunpu_mean('w1mean',1,1)
print('w1mean',meanw1)

#数式の実行
w2 = (x+y)*v1
w2.bunpu_graph('w2')
w40 = bunpu()
w40 = y*2.5
w4 = x+w40
w4.bunpu_graph('w4')
mean4 = w4.bunpu_mean('w4mean',1,1)
print('w4mean',mean4)


#相互に独立な分布のかけ算
w3 = v1.bunpu_product(v1)
mean3 = w4.bunpu_mean('w3mean',1,1)
print('w3mean',mean3)


#パーセンタイル
#pxw2:パーセンタイル値、対象の分布、出力グラフ名、グラフに表示される単位名、閾値１、閾値２、パーセンタイルの方向、グラフ表示有無、２次元以上のグラフの視点
pcw2 = w2.bunpu_percent(['w2percent','unit'],[10000],[10000],[1],1,1)
print('w2percent',pcw2)
#ふたつの閾値の間に入る確率
w2.bunpu_percent(['w22percent','unit'],[5000],[10000],[1],1,1)

#分布の比較
#w1がw3を上回る確率を求める
#
w1.bunpu_percent2(w3,['w2percent2','unit'],[1],1)


#2D
#諸元（最小値、最大値、平均値、標準偏差）をして2D分布を作成
#Create a distribution from parametar(min,max,mean,)

#z2=bunpu()
z2.bunpu_gene([10,8],[50,60],[25,40],[4,5],[100,100])
z2.bunpu_graph('z2')
meanz2 = z2.bunpu_mean('z2mean',1,1)
print('z2mean',meanz2)
#y2=bunpu()
y2.bunpu_gene([30,10],[80,70],[55,40],[4,5],[100,100])


#無視する行、抽出する列、分布の分割数を指定して2D分布を求める
#Create a distribution by specifying lines to ignore, columns to extract, and number of distribution divisions in a text file
#pos=bunpu()
pos.bunpu_data('detectposi.csv','pos',1,[1,2],[100,100])
pos.bunpu_graph('pos')
meanpos = pos.bunpu_mean('posmean',1,1)
print('posmean',meanpos)


w5=pos.bunpu_add(z2)
w5.bunpu_graph('w5')
meanw5 = w5.bunpu_mean('w5mean',1,1)
print('w5mean',meanw5)

w6 = (pos+z2)*v1
w6.bunpu_graph('w6')
mean6 = w6.bunpu_mean('w6mean',1,1)
print('w6mean',mean6)


#パーセンタイル
#ベクトル[10,3]の方向で[40,40]を含む平面で分割した確率を求める
pc2 = z2.bunpu_percent(['z2percent','unit'],[40,40],[40,40],[10,3],1,1)
print('z2percent',pc2)
#ベクトル[10,3]の方向で[40,40]と[20,40]を含む平面の間になる確率を求める
pc22 = z2.bunpu_percent(['z22percent','unit'],[20,40],[40,40],[10,3],1,1)
print('z22percent',pc22)

#分布の比較
#分布z2が分布y2に対してベクトル[1,0]の方向で90°の範囲に上回る確率を求める。
#（分布y2をベクトル[1,0]の方向で90°の範囲に累積した累積分布とz2の確率値の積分布）
pc22 = z2.bunpu_percent2(y2,['z2percent2','unit'],[1,0,90],1)
print('z2percent2',pc22)
    
    
#3D
#諸元（最小値、最大値、平均値、標準偏差）をして3D分布を作成
#Create a distribution from parametar(min,max,mean,)

#x3=bunpu()
x3.bunpu_gene([10,8,11],[50,60,55],[20,40,30],[4,5,4],[20,20,20])
x3.bunpu_graph('x3')
#y3=bunpu()
y3.bunpu_gene([-2,-10,-5],[10,5,5],[6,-6,1],[2,2,2],[20,20,20])
#z3=bunpu()
z3.bunpu_gene([-10,-10,-20],[-60,-50,-70],[-30,-38,-40],[2,2,2],[20,20,20])
#breakpoint()
meanx3 = x3.bunpu_mean('x3mean',1,1)
print('x3mean',meanx3)
meany3 = y3.bunpu_mean('y3mean',1,1)
print('y3mean',meany3)

w7 = x3+y3
w7.bunpu_graph('w7')
mean7 = w7.bunpu_mean('w7mean',1,1)
print('w7mean',mean7)
w80 = bunpu()
w80 = y3*2
w8 = x3+w80
w8.bunpu_graph('w8')
mean8 = w8.bunpu_mean('w8mean',1,1)
print('w8mean',mean8)

w9=bunpu()
w9 = x3.bunpu_product(v1)
#breakpoint()
w9.bunpu_graph('w9')
mean9 = w9.bunpu_mean('w9mean',1,1)
print('w9mean',mean9)
#パーセンタイル
#ベクトル[5,1,1]の方向で[40,40,40]を含む平面で分割した確率を求める
pc3 = x3.bunpu_percent(['x3percent','unit'],[40,40,40],[40,40,40],[5,1,1],1,1)
print('x3percent',pc3)
pc32 = x3.bunpu_percent(['x32percent','unit'],[20,40,30],[40,40,40],[5,1,1],1,1)
print('x32percent',pc32)

#分布の比較
#分布w7が分布w8に対してベクトル[1,0.1,0.1]の方向で上下60°左右60°の範囲に上回る確率を求める。
#（分布w8をベクトル[1,0.1,0.1]の方向で上下60°左右60°の範囲に累積した累積分布とw7の確率値の積分布）
pc7 = w7.bunpu_percent2(w8,['w7percent2','unit'],[1,0.1,0.1,60,60],1)
print('w7percent2',pc7)


print('finish')
    
    
    
