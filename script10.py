# -*- coding: utf-8 -*-
#
from bunpu import *
#
#
#レーダークルーズ
#追従制御
dlt0 = 0.01
tm=2500
dim=1
#運動方程式
m=1200#kg
#駆動力最大分布と最小分布
fmin=bunpu()
dtdist=bunpu()
voa = bunpu()

fmax = 1480
fmin.bunpu_gene([-3240],[-2400],[-2800],[100],[50])
#レーダー検出距離データ
dtdist.bunpu_data('fdetect.csv','ditect',1,[7],[50])
#先行車速度分布
voa.bunpu_gene([54],[64],[60],[1.5],[20])
#初期速度
vsi=120*1000/3600
xo0=150#先行車初期位置
kd=0.1# 車間距離による比例乗数
kv=0.1# 車速差による車間制御の比例乗数
ks=0.1# 車速制御の比例乗数
#接近危険距離の車間時間、この距離より短くなる確率を求める
rsktime=1.0
simulink1=[]
simulink2=[]
minidist=[]
for t in range(tm):

    dtdst1,fmin1,voa1 = dtdist.bunpu_simu_start([fmin,voa],dlt0,1)
    #先行車速度と位置

    if t == 0:
        xo2 = bunpu()
        xo2.bunpu_simu_ones(voa1)
        xo1 = xo2.bunpu_simu_prd(xo0)#set 150m
        xo = xo1
        voa0 = voa1.bunpu_simu_div(3.6)
        voa1 = voa0
    xo1=xo.bunpu_simu_integral([voa1],dlt0,1)
    asmin = fmin1.bunpu_simu_div(m)#2~2.7
    asmax = fmax/m
    #目標車間距離
    if t == 0:
        vs0 = bunpu()
        vs0.bunpu_simu_ones(dtdst1)
        vs = vs0.bunpu_simu_prd(vsi)
        thdvs = vs.bunpu_simu_prd(3)
    else:
        thdvs = bunpu()
        thdvs = vs.bunpu_simu_prd(3)#vsの３倍 
    xrelt = thdvs.bunpu_simu_limit([3],2)#linemapのパラメータが3*vsが3mより小さいときに3mとする
    rskdst = vs.bunpu_simu_prd(rsktime)#接近危険距離の車間距離
    #車間距離
    #
    if t == 0:
        xs = bunpu()
        xs.bunpu_simu_zeros(dtdst1)
    xrelr = xo.bunpu_simu_sub(xs)
    cond0 = dtdst1.bunpu_simu_comp([xrelr],0)#dtdst1<=xrelr の場合1、そうでなければ0
    cond1 = dtdst1.bunpu_simu_comp([xrelr],1)#実車間距離が検出距離より小さい場合、つまり減速制御開始
    xrelrlst = xrelr.linemap_extrct()#xrelrのlinemap配列を抽出
    xreld = xrelrlst*cond1+200*cond0#検出車間距離の配列
    
    difxrel0 = xrelt.bunpu_simu_invsub(xreld)#検出車間距離と目標車間距離の差
    difxrel = difxrel0.linemap_extrct()
    difv0 = vs.bunpu_simu_invsub(voa1)#先行車との速度差
    difv = difv0.linemap_extrct()
    asd0 = kv*difv[0]#車間制御マトリックス
    asd1 = kd*difxrel[0]
    asd = asd0+asd1
    ass0 = vs.bunpu_simu_invsub(vsi)#目標車速と実車速の差、速度制御
    ass = ass0.bunpu_simu_prd(ks)#車速制御分布
    as0 = ass.bunpu_simu_limit(asd,1)
    as1 = as0.bunpu_simu_limit(asmax,1)
    as2 = as1.bunpu_simu_limit(asmin,2)
    vz = bunpu()
    vz.bunpu_simu_zeros(as2)
    #as3 = bunpu()
    as3 = vs.bunpu_simu_limit2([as2,vz,vz],0)
    vs1=vs.bunpu_simu_integral([as3],dlt0,1)
    xs1=xs.bunpu_simu_integral([vs1],dlt0,1)
    
    vs = vs1
    xs = xs1
    xo = xo1
    voa =voa1
    fmin=fmin1
    dtdist=dtdst1
    gname = 'timeline_v'
    simulink1=vs.bunpu_simu_graph(voa1,simulink1,t,tm,dlt0,gname,0)
    #if t==2499:
    #    print('s1')
    gname = 'timeline_relx'
    simulink2=xrelr.bunpu_simu_graph(rskdst,simulink2,t,tm,dlt0,gname,0)
    #if t==2499:
    #    print('s2')
    #車間距離が目標車間距離より小さくなる確率を求める
    rsk = xrelr.bunpu_simu_sub(rskdst)
    gname = 'toonearprb'
    minidist=rsk.bunpu_simu_prb(0,minidist,0,t,tm,gname)#
    print(t)

    #ループの終わり

