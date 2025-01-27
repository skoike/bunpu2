#bunpu2用のシミュレーション
#空間を移動するターゲットをミサイルが迎撃する
#ミサイルは位置と速度にバラツキを与える。
#発射時に弾道起動を飛行して、500m以内でターゲットを認識して自律制御にて追尾する
#
#Missile intercepts a target moving in space
#Missiles cause variations in position and speed.
#Fly the ballistic launch when launching, recognize the target within 500m and track it under autonomous control

dlt = 0.1
#est=15+dlt*5*(2+dlt)
kakudo=37*np.pi/180#方位1 Aiming direction 1
#kakudo=41*np.pi/180#方位2 Aiming direction 2
#houi= 40*np.pi/180
houi= 50*np.pi/180
vt0=300
vx0=vt0*np.cos(kakudo)*np.cos(houi)#m/s
vy0=vt0*np.cos(kakudo)*np.sin(houi)#m/s
vz0=vt0*np.sin(kakudo)#m/s
v0=bunpu()
ms = 4
vxmin=vx0-5
vymin=vy0-3
vzmin=vz0-3
vxmax=vx0+7
vymax=vy0+5
vzmax=vz0+5
#v0.bunpu_gene([vx0-5,vy0-3,vz0-3],[vx0+7,vy0+5,vz0+5],[vx0,vy0,vz0],[1.0,0.8,0.8],[ms,ms,ms])
v0.bunpu_gene([vxmin,vymin,vzmin],[vxmax,vymax,vzmax],[vx0,vy0,vz0],[1.0,0.8,0.8],[ms,ms,ms])
v0.bunpu_graph('3d v')
v0.bunpu_file('3d v')
#x0初期位置のバラツキx0: Initial position variation
x0.bunpu_gene([-10,-5,-5],[5,7,5],[0,0,0],[1.0,0.8,0.5],[ms,ms,ms])
x0.bunpu_graph('3d x0')
#幅のない分布 Widthless distribution
#a0 = bunpu()
a0.vector_gene([0,0,-9.8])
#ターゲットの検出誤差 Target detection error
#xy.bunpu_gene([-20.0,-20.0,-30.0],[20,20,25],[0,0,0],[4.1,5.1,5.5],[5,5,5])
xy.bunpu_gene([-20.0,-20.0,-30.0],[20,20,25],[0,0,0],[4.1,5.1,5.5],[ms,ms,ms])
#検出誤差 detection error
minidist0=[0]
simulink=[]
contact=[]
ditect = bunpu()
#ditect.bunpu_gene([-2,-2,-3],[2,2,2],[0,0,0],[0.3,0.2,0.5],[5,5,5])
ditect.bunpu_gene([-2,-2,-3],[2,2,2],[0,0,0],[0.3,0.2,0.5],[ms,ms,ms])
#a = bunpu()
a = a0
v = v0
x = x0
amin = -50
amax = 50
fname='s_amax'
amx.bunpu_gene([20,30,20],[50,60,50],[30,40,30],[3,2,2],[ms,ms,ms])
amx.bunpu_graph(fname)#34
#ターゲットの初期位置 Initial position of target
xtg0=[3000,1000,2000]
#xtg0=[3000,1000,3000]
vtg0=[-100,100,-50]
#ターゲットの前回値 Previous value of target
lastxy=xy
#検出距離の初期値 
xrelmin=40000
acc=a0
#ターゲット接触判定の距離
contact0=20
#ミサイルがターゲットを検出できる距離
#dists=700
dists=500.0#制御あり
#dists=0#制御なし
#ターゲットの前回値
#lastxy=bunpu()
#lastxy=copy.deepcopy(xy)
lastxy=xy
#nv = v0.div[0]*v0.div[1]*v0.div[2]#8/14この計算ができない
nv=ms*ms*ms
#nx = x0.div[0]*x0.div[1]*x0.div[2]
nx=ms*ms*ms
#nxy = xy.div[0]*xy.div[1]*xy.div[2]
nxy=ms*ms*ms
#距離の初期値（最も近い距離を求める）
xrelmin=3000*np.ones((1,nv,nx,nxy))
xrelmin[0][0][0]=40000

#フィードバック制御のゲイン
gain=1000
k2 = np.zeros(3)
cfflag=0
shw=1
#forにてループを行うが、スクリプト中にforは一回だけ使用できる。
#pythonとは異なり、ループ区間はインデントは行わないで、forendでループ終了を指定する→pythonと同じインデントでループ範囲を指定するように変更5/30
#A loop is performed using for, but for can only be used once in a script.
#Unlike python, the loop section is not indented, and the end of the loop is specified with forend.
tm=130
for t in range(tm):
    if t == 0:
        #Add vector xtg0 to distribution xy,
        y=xy.bunpu_add(xtg0)#分布xyにベクトルxtg0を加算、
    else:
        vtary = vtg0*dlt
        y=ypos.bunpu_simu_add(vtary)
    #Creating an initial matrix for time series operations
    #時系列演算の初期マトリックス作成
    acc,vel,pos,ypos=a0.bunpu_simu_start([v,x,y],dlt,shw)
    #integral operator,v=∫acc*dt
    #積分演算子、v=∫acc*dt
    v=vel.bunpu_simu_integral([acc],dlt,shw)
    #integral operator,x=∫x*dt
    #積分演算子、x=∫x*dt
    x=pos.bunpu_simu_integral([v],dlt,shw)
    v0=v
    a0=acc
    a=acc
    #rel=bunpu()
    xrel=ypos.bunpu_simu_sub(x)
    filename='cont_prb'
    flagx = 0
    #最接近距離の演算、シミュレーション終了時に上記ファイル名で接近距離＊確率分布をもとめる
    minidist=xrel.bunpu_simu_prb(contact0,minidist0,flagx,t,tm,filename)
    minidist0 = minidist
    distx = xrel.bunpu_simu_dist()
    if t>0:
        x.timeline=x0.timeline
        ddistx = lastdistx-distx#１ステップの接近距離
    #lastdistx = copy.deepcopy(distx)
    lastdistx = distx
    #ターゲットとの距離判定結果
    comp = xrel.bunpu_simu_comp([dists],0)
    #制御開始フラグ
    condc = np.sum(comp)
    if condc>0:
        distv = vel.bunpu_simu_dist()
        #ターゲット速度
        #vrtualv0 = bunpu()
        #vrtualv = bunpu()
        virtualv0 = ypos.bunpu_simu_sub(lasty)
        vdistx = distx/ddistx
        vdistlist = [vdistx,vdistx,vdistx]
        #virtualv = virtualv0.bunpu_simu_prd(np.array([distx/ddistx,distx/ddistx,distx/ddistx]))
        virtualv = virtualv0.bunpu_simu_prd(vdistlist)
        #ターゲット仮想位置
        #vrtualy = bunpu()
        virtualy = ypos.bunpu_simu_add(virtualv)
        #仮想ターゲットとの相対位置
        #vrtualrelx = bunpu()
        virtualrelx = virtualy.bunpu_simu_sub(pos)
        vdistx = virtualrelx.bunpu_simu_dist()
        #外積による制御量演算
        #op1 = bunpu()
        op1 = vel.bunpu_simu_outprod(virtualrelx)
        #op2 = bunpu()
        op2 = op1.bunpu_simu_outprod(vel)
        k0 = gain/(distv*vdistx**2)
        k = [k0,k0,k0]#距離が遠いほど小さい
        
        if cfflag == 0:
            cfflag = 1
            a00 = op2.bunpu_simu_prd(k)
        else:
            diffop = op2.bunpu_simu_sub(lastop)
            diffk = diffop.bunpu_simu_prd(k2)
            a01 = op2.bunpu_simu_add(diffk)
            a00 = a01.bunpu_simu_prd(k)#i=92
        lastop = op2
        a01 = a00.bunpu_simu_comp_prd(comp)#94
        limit0 = [200,200,200]
        a0 = a01.bunpu_simu_limit(limit0,0)#96
    print(t)#
    cond0=xrelmin>distx#98
    #最接近距離判定
    cond1=~cond0.astype(int)
    cond2=cond0.astype(int)
    xrelmin=xrelmin*cond1+distx*cond2
    gname='timeline_v1'
    simulink=x.bunpu_simu_graph(ypos,simulink,t,tm,dlt,gname,3,1)
    #ターゲットとの位置分布（20m以内となる逐次確率を求める）
    if t >= 110:
        x.bunpu_simu_readout()
        ypos.bunpu_simu_readout()
        tname='target_'+t
        x.bunpu_twin_graph(ypos,tname,contact0)
    #ターゲットの前回値
    lasty = ypos
    #ループの終わり
    


