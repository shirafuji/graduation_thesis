###################################
# 2D fig for Vib. Frame Analysis
###################################
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.signal import argrelmax

# Main routine
args = sys.argv
fnameR=args[1] # input data file

f=open(fnameR,'r')
text=f.readline()
text=f.readline()
text=text.strip()
text=text.split()
npoin =int(text[0])  # Number of nodes
nele  =int(text[1])  # Number of elements
nsec  =int(text[2])  # Number of sections
npfix =int(text[3])  # Number of restricted nodes
nlod  =int(text[4])  # Number of loaded nodes
ndoutx=int(text[5])
ndouty=int(text[6])
nfout =int(text[7])
dt    =float(text[8]) # Time increment
nnn   =int(text[9])
nod=2                # Number of nodes per element
nfree=3              # Degree of freedom per node
n=nfree*npoin

x     =np.zeros(npoin,dtype=np.float64)     # Coordinates of nodes
y     =np.zeros(npoin,dtype=np.float64)     # Coordinates of nodes
ae    =np.zeros([6,nsec],dtype=np.float64)      # Section characteristics
node  =np.zeros([nod+1,nele],dtype=np.int)      # Node-element relationship

# section characteristics
text=f.readline()
for i in range(0,nsec):
    text=f.readline()
    text=text.strip()
    text=text.split()
    ae[0,i]=float(text[1]) # E      : Elastic modulus
    ae[1,i]=float(text[2]) # AA     : Section area
    ae[2,i]=float(text[3]) # AI     : Moment of inertia
    ae[3,i]=float(text[4]) # gamma  : Unit weight
    ae[4,i]=float(text[5]) # zeta_m : Coefficient for Rayleigh damping alpha1*[c]
    ae[5,i]=float(text[6]) # zeta_k : Coefficient for Rayleigh damping alpha2*[k]
# coordinates
text=f.readline()
for i in range(0,npoin):
    text=f.readline()
    text=text.strip()
    text=text.split()
    x[i]=float(text[1])
    y[i]=float(text[2])
# element-node
text=f.readline()
for i in range(0,nele):
    text=f.readline()
    text=text.strip()
    text=text.split()
    node[0,i]=int(text[0]) #node_1
    node[1,i]=int(text[1]) #node_2
    node[2,i]=int(text[2]) #section characteristic number
# result
mm=1+ndoutx*3+ndouty*3+nfout*3
ttime  =np.zeros(nnn,dtype=np.float64)
result =np.zeros([nnn,mm],dtype=np.float64)
strt=[]

text=f.readline()
text=text.strip()
text=text.split()
for j in range(0,mm):
    strt=strt+[text[j+2]]
for iii in range(0,nnn):
    text=f.readline()
    text=text.strip()
    text=text.split()
    ttime[iii]=float(text[1])
    for j in range(0,mm):
        result[iii,j]=float(text[2+j])
f.close()

xx=ttime
xmin=np.min(xx)
xmax=np.max(xx)
for j in range(0,mm):
    fnameF='_fig_his_'+strt[j]+'.png'
    yy=result[:,j]
    if np.max(np.abs(yy))<1.0e-6: continue
    ymax=np.max([np.max(yy),np.abs(np.min(yy))])*1.2
    ymin=-ymax
    plt.figure(figsize=(10,3))
    ax=plt.subplot(111)
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.set_xlabel('time (sec)')
    ax.set_ylabel(strt[j])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.plot(xx,yy,'-',color='#0000ff',linewidth=0.5)
    ls1='max={0:.3f}'.format(np.max(yy))
    ls2='min={0:.3f}'.format(np.min(yy))
    ax.plot(xmin,ymin,'.',label=ls1)
    ax.plot(xmin,ymin,'.',label=ls2)
    ax.legend(loc='upper right',numpoints=1,markerscale=0, frameon=False,prop={'family':'monospace','size':12})
    plt.savefig(fnameF, bbox_inches="tight", pad_inches=0.2)
    plt.clf()


for j in range(0,mm):
    fnameF='_fig_fft_'+strt[j]+'.png'
    yy=result[:,j]
    if np.max(np.abs(yy))<1.0e-6: continue
    ndata=nnn
    nn=2
    while nn < ndata:
        nn=nn*2
    xx=np.zeros(nn,dtype=np.float64)
    xx[0:ndata]=xx[0:ndata]+yy[0:ndata]
    spf=np.fft.fft(xx,nn)/nn
    sp0=np.sqrt(spf.real[0:int(nn/2)+1]**2+spf.imag[0:int(nn/2)+1]**2)*dt*nn
    fk0=np.arange(0,nn/2+1)/nn/dt

    maxID=argrelmax(sp0,order=100)
    m=len(fk0[maxID])
    fkm=fk0[maxID]
    print(m)
    ls=[]
    ls=ls+['{0:>10s}'.format('fk(Hz)')]
    if 0<m:
        for i in range(0,m):
            ls=ls+['{0:10.3f}'.format(fkm[i])]

    xmin=0
    xmax=np.max(fk0)
    plt.xlabel('Frequency (Hz)',fontsize=12)
    plt.ylabel(strt[j],fontsize=12)
    plt.xlim(xmin,xmax)
    plt.semilogy(fk0,sp0,linewidth=0.5,color='blue')
    plt.semilogy(fk0[maxID],sp0[maxID],'ro')
    plt.grid(True,ls='-', color='0.65')
    xmin,xmax,ymin,ymax=plt.axis()
    mm=m
    if 12<mm: mm=12
    for i in range(0,mm+1):
        plt.plot(xmin,ymin,'.',label=ls[i])
    plt.legend(bbox_to_anchor=(1.15, 1),loc='upper right',borderaxespad=0,numpoints=1,markerscale=0, frameon=False,prop={'family':'monospace','size':10})
    plt.savefig(fnameF, bbox_inches="tight", pad_inches=0.2)
    plt.clf()

