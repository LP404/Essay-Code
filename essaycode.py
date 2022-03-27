import math as m
import numpy as np
from timeit import default_timer as timer
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.integrate import odeint
plt.rcParams["figure.figsize"] = (10,3)


def OVfunc(h,vTarget):
    if h < 0:
        return 0
    elif h <= 1 and h >= 0:
        return 0
    elif h > 1:
        return (vTarget * (((h-1)**3) / (1 + (h-1)**3)))
    
def OVfuncUnrestricted(h,vTarget):
        return (vTarget * (((h-1)**3) / (1 + (h-1)**3)))

def FinalHeadway(CircuitLength, headway):
    return (CircuitLength - sum(headway[0:-1]))

#Function can be used for multiple calculations, no need to make multiple functions
def DiffFunc(v1,v0):
    return v1 - v0

def Ovfunc2(vTarget,k,w,n):
        return (w / (2*np.cos((w - (k*np.pi / n))) * np.sin((k * np.pi) / n)))
    
def Ovfunc3(vTarget,k,n):
        return ((k * np.pi)/ n) / 2 * np.sin((k * np.pi) / n)

NoCars = 3
CircuitLength = 20
a = 5
dt = 0.001
tFinal = 500
t = np.linspace(0,tFinal,int(tFinal/dt))
vTarget = 8
AvgHeadway = CircuitLength / NoCars    
Vals0 = np.array([np.full(NoCars,AvgHeadway),np.full(NoCars,vTarget)])
hPrev = np.full(NoCars,AvgHeadway)





#Inital condtions assume cars are equally spaced and are travelling at the same velocity



h = np.full(NoCars,AvgHeadway)
hPrev = np.full(NoCars,AvgHeadway)
v = np.full(NoCars,vTarget)


def FirstProblem(NoCars,a,OVfunc,hPrev,v,vTarget,t,CircuitLength,dt):
    out = open('Task1.txt' , 'w')
    for i in range(len(t)):
        for b in range(NoCars):
            dv = (a* (OVfunc(hPrev[b],vTarget) - v[b]))
            vn = v[b] + (dv * dt)
            print(vn)
            v[b] = vn
            
            if b == NoCars-1:
                pass
            else: 
                dh = DiffFunc(v[b+1],v[b])

            
            
            hn = h[b] + (dh * dt)
            hPrev[b] = h[b]
            h[b] = hn
        
            print(hn)
        h[-1] = FinalHeadway(CircuitLength, h)
        out.write(f"{t[i]} {v} {h} \n")
    out.close()
    return

k = 1
w = 1

#r can start at 0 since car velcoties are the same

rPrev = np.full(NoCars,0)
r = np.full(NoCars,0)
a1 = -w * np.arctan((w - (k * np.pi)/ NoCars))
v2 = np.full(NoCars,vTarget)

def SecondProblem(NoCars,a,OVfunc3,rPrev,v,vTarget,k,r,dt):
    out = open('Task2.txt' , 'w')
    for i in range(len(t)):
        for b in range(NoCars):
            VarNar = Ovfunc3(vTarget,k,NoCars)
            dv = -a*v[b] + (a * VarNar * rPrev[b])
            vn = v[b] + (dv * dt)
            v[b] = vn
            
            
            if b == NoCars-1:
                dr = DiffFunc(v[0],v[b])
            else: 
                dr = DiffFunc(v[b+1],v[b])
            
            rPrev[b] = r[b]
            rn = r[b] + (dt * dr)
            r[b] = rn
        out.write(f"{t[i]} {r} {v} {VarNar} \n")
    out.close()   
    return
 
#FirstProblem(NoCars,a,OVfunc,hPrev,v,vTarget,t,CircuitLength,dt)
SecondProblem(NoCars,a,Ovfunc3,rPrev,v,vTarget,k,r,dt)