#車両のデータレコーダー成立性検討
#記録イベントの作動頻度（作動距離間隔の頻度分布）と車両の日当たり走行距離から記録日数分布をもとめる(1)
#上記が８個のメモリーが全て埋まる日数分布を求める(2)
#上記とお客様入庫までの日数分布からレコーダーが上書きされる確率を求める(3)

kbd.bunpu_data('kmbday.csv','kmbday',1,[1],[300])
kbt.bunpu_data('kmbtime.csv','kmbtime',1,[1],[300])
cday.bunpu_data('cday.csv','cday',1,[1],[300])
#(1)の演算
daybtime=kbt.bunpu_division(kbd,[300],0,0)#分割、相関係数、面積表示
#(2)の演算
dayb2time=daybtime.bunpu_add(daybtime,[300],0,0)
dayb4time=dayb2time.bunpu_add(dayb2time,[300],0,0)
dayb8time=dayb4time.bunpu_add(dayb4time,[300],0,0)
#(3)の確率演算
cday.bunpu_percent2(dayb8time,'day',[1],0)
#メモリーが１回記録される日数分布
daybtime.bunpu_graph('daybtime')


