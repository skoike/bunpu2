#��Ԃ��ړ�����^�[�Q�b�g���~�T�C�����}������
#�~�T�C���͈ʒu�Ƒ��x�Ƀo���c�L��^����B
#���ˎ��ɒe���N�����s���āA500m�ȓ��Ń^�[�Q�b�g��F�����Ď�������ɂĒǔ�����
#
dlt = 0.1
test=15+dlt*5*(2+dlt)
#kakudo=37*np.pi/180#����1
kakudo=41*np.pi/180#����2
houi= 40*np.pi/180
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
#v0.bunpu_gene([vx0-5,vy0-3,vz0-3],[vx0+7,vy0+5,vz0+5],[vx0,vy0,vz0],[1.0,0.8,0.8],[ms,ms,ms],'v3')
v0.bunpu_gene([vxmin,vymin,vzmin],[vxmax,vymax,vzmax],[vx0,vy0,vz0],[1.0,0.8,0.8],[ms,ms,ms],'v3')
breakpoint()
v0.bunpu_graph('3d v')
v0.bunpu_file('3d v')
#x0�����ʒu�̃o���c�L
x0.bunpu_gene([-10,-5,-5],[5,7,5],[0,0,0],[1.0,0.8,0.5],[ms,ms,ms],'x3')
x0.bunpu_graph('3d x0')
#���̂Ȃ����z
#a0 = bunpu()
a0.vector_gene([0,0,-9.8])
#�^�[�Q�b�g�̌��o�덷
#xy.bunpu_gene([-20.0,-20.0,-30.0],[20,20,25],[0,0,0],[4.1,5.1,5.5],[5,5,5],'xtg3')
xy.bunpu_gene([-20.0,-20.0,-30.0],[20,20,25],[0,0,0],[4.1,5.1,5.5],[ms,ms,ms],'xtg3')
#���o�덷
minidist0=[0]
contact=[]
ditect = bunpu()
#ditect.bunpu_gene([-2,-2,-3],[2,2,2],[0,0,0],[0.3,0.2,0.5],[5,5,5],'ditect')
ditect.bunpu_gene([-2,-2,-3],[2,2,2],[0,0,0],[0.3,0.2,0.5],[ms,ms,ms],'ditect')
#a = bunpu()
a = a0
v = v0
x = x0
amin = -50
amax = 50
fname='s_amax'
amx.bunpu_gene([20,30,20],[50,60,50],[30,40,30],[3,2,2],[ms,ms,ms],'a1')
amx.bunpu_graph(fname)#34
#�^�[�Q�b�g�̏����ʒu
xtg0=[3000,1000,2000]
#xtg0=[3000,1000,3000]
vtg0=[-100,100,-50]
#�^�[�Q�b�g�̑O��l
lastxy=xy
#���o�����̏����l
xrelmin=40000
acc=a0
#�^�[�Q�b�g�ڐG����̋���
contact0=20
#�~�T�C�����^�[�Q�b�g�����o�ł��鋗��
#dists=700
dists=500.0#���䂠��
#dists=0#����Ȃ�
#�t�B�[�h�o�b�N����̃Q�C��
gain=200000
k2 = np.zeros(3)
cfflag=0
shw=1
#for�ɂă��[�v���s�����A�X�N���v�g����for�͈�񂾂��g�p�ł���B
#python�Ƃ͈قȂ�A���[�v��Ԃ̓C���f���g�͍s��Ȃ��ŁAforend�Ń��[�v�I�����w�肷��
tm=130
for t in range(tm):
if t == 0:
    y=xy.bunpu_add(xtg0)#���zxy�Ƀx�N�g��xtg0�����Z�A
else:
    vtary = vtg0*dlt
    y=ypos.bunpu_simu_add(vtary)
#���n�񉉎Z�̏����}�g���b�N�X�쐬
acc,vel,pos,ypos=a0.bunpu_simu_start([v,x,y],dlt,shw)
#�ϕ����Z�q�Av=��acc*dt
v=vel.bunpu_simu_integral([acc],dlt,shw)
#�ϕ����Z�q�Ax=��x*dt
x=pos.bunpu_simu_integral([v],dlt,shw)

if t>0:
    x.timeline=x0.timeline

v0=v
a0=acc
a=acc
xrel=ypos.bunpu_simu_sub(x)
filename='cont_prb'
flagx = 0
#�Őڋߋ����̉��Z�A�V�~�����[�V�����I�����ɏ�L�t�@�C�����Őڋߋ������m�����z�����Ƃ߂�
minidist=xrel.bunpu_simu_prb(contact0,minidist0,flagx,t,tm,filename)
minidist0 = minidist
distx = xrel.bunpu_simu_dist()
#�^�[�Q�b�g�Ƃ̋������茋��
comp = xrel.bunpu_simu_comp([dists],0)
#����J�n�t���O
condc = np.sum(comp)
if condc>0:
    distv = vel.bunpu_simu_dist()
    #�^�[�Q�b�g���x
    virtualv0 = ypos.bunpu_simu_sub(lasty)
    virtualv1 = distx/(dlt*distv)
    virtualv2 = [virtualv1,virtualv1,virtualv1]
    virtualv = virtualv0.bunpu_simu_prd(virtualv2)
    #�^�[�Q�b�g���z�ʒu
    virtualy = ypos.bunpu_simu_add(virtualv)
    #���z�^�[�Q�b�g�Ƃ̑��Έʒu
    virtualrelx = virtualy.bunpu_simu_sub(pos)
    vdistx = virtualrelx.bunpu_simu_dist()
    #�O�ςɂ�鐧��ʉ��Z
    op1 = vel.bunpu_simu_outprod(virtualrelx)
    op2 = op1.bunpu_simu_outprod(vel)
    k0 = gain/(distv*vdistx**3)
    k = [k0,k0,k0]#�����������قǏ�����
    
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
    a0 = a01.bunpu_simu_limit(limit0)#96
print(t)#
cond0=xrelmin>distx#98
#�Őڋߋ�������
cond1=~cond0.astype(int)
cond2=cond0.astype(int)
xrelmin=xrelmin*cond1+distx*cond2
gname='timeline_v1'
x.bunpu_simu_graph(ypos,t,tm,gname,1)
#�^�[�Q�b�g�Ƃ̈ʒu���z�i20m�ȓ��ƂȂ钀���m�������߂�j
if t >= 110:
    x.bunpu_simu_readout()
    ypos.bunpu_simu_readout()
    tname='target_'+t
    x.bunpu_twin_graph(ypos,tname,contact0,1)
#�^�[�Q�b�g�̑O��l
lasty = ypos
#���[�v�̏I���
forend

