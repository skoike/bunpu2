#車両のデータレコーダー成立性検討
#記録イベントの作動頻度（作動距離間隔の頻度分布）と車両の日当たり走行距離から記録日数分布をもとめる(1)
#上記が８個のメモリーが全て埋まる日数分布を求める(2)
#上記とお客様入庫までの日数分布からレコーダーが上書きされる確率を求める(3)
#Determine the distribution of recording days from the operating frequency of recording events (frequency distribution of operating distance intervals) and daily mileage of the vehicle (1)
#Find the distribution of days in which all 8 memories above are filled (2)
#Calculate the probability that the recorder will be overwritten from the above and the distribution of days until customer receipt (3)

#ファイルのデータから分布を作成する
#Create a distribution from data in a file
kbd.bunpu_data('kmbday.csv','kmbday',1,[1],[300])
kbt.bunpu_data('kmbtime.csv','kmbtime',1,[1],[300])
#Create a distribution by specifying lines to ignore, columns to extract, and number of distribution divisions in a text file
cday.bunpu_data('cday.csv','cday',1,[1],[300])#無視する行、抽出する列、分布の分割数を指定して分布を求める
#(1)の演算
#Calculation of (1)
daybtime=kbt.bunpu_division(kbd,[300],0,0)#分割、相関係数、面積表示 Division, correlation coefficient, area display
#(2)の演算
#Calculation of (2)
dayb2time=daybtime.bunpu_add(daybtime,[300],0,0)
dayb4time=dayb2time.bunpu_add(dayb2time,[300],0,0)
dayb8time=dayb4time.bunpu_add(dayb4time,[300],0,0)
#(3)の確率演算
#Calculation of (3)
cday.bunpu_percent2(dayb8time,'day',[1],0)
#メモリーが１回記録される日数分布
#Distribution of days in which memory is recorded once
daybtime.bunpu_graph('daybtime')


