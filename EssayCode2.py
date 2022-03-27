import math as m
import numpy as np
from timeit import default_timer as timer
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.integrate import odeint
plt.rcParams["figure.figsize"] = (10,3)


def Vfunc(x,x1,v,v1,C):
    Var1 = x1 - x
    Var2 = C * Var1
    Var3 = np.tanh(Var2)
    if x < x1:
        Var4 = 1 + Var3
        Var5 = Var4 * v
        return Var5
    else:
        Var6 = v1 - v
        Var7 = v + (Var6 * Var3)
        return Var3
    
def Lam(delX):
    if delX <= 100:
        return 0.5
    else:
        return 0

Kon = 0.41

NoCars = 3
CircuitLength = 20
a = 5
dt = 0.001
tFinal = 500
t = np.linspace(0,tFinal,int(tFinal/dt))
a = np.fill(NoCars,-7)
v = np.fill(NoCars,1)
x = np.fill(NoCars,1)
vPrev = np.fill(NoCars,0)
xPrex = np.fill(NoCars,0)
hcStop = 1
r = np.fill(NoCars,1)

#Inital condtions assume cars are equally spaced and are travelling at the same velocity




def FirstProblem(NoCars,a,OVfunc,hPrev,v,vTarget,t,CircuitLength,dt):
    out = open('Out.txt' , 'w')
    for i in range(len(t)):
        for b in range(NoCars):
            dx = v[b] * tw - (v[b]**2/ 2*a[b]) + (v[b-1]**2/ 2*a[b-1]) + hcStop
            dv = Kon * Vfunc(x,x1) - v[b] + Lam(dx)*delV
            
            
            vn = v[b] + dt*dv
            xn = x[b] + x[b] + v[b]*dt + (0.5 * dv * dt**2)
            
            vPrev[b] = v[b]
            v[b] = vn
            
            xPrev[b] = x[b]
            x[b] = xn
            
        out.write(f"{t[i]} {x} {v} \n")
    out.close()
    return

#FirstProblem(NoCars,a,OVfunc,hPrev,v,vTarget,t,CircuitLength,dt)