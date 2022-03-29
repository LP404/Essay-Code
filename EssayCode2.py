#Imports the files
import math as m
import numpy as np
from timeit import default_timer as timer
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.integrate import odeint
plt.rcParams["figure.figsize"] = (10,3)

#Seed = int(t.time())
Seed = 22061910
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

#Optimal speed function
def Vfunc(xc,xNext,vNext,vMax,C):
    Var1 = xNext - xc
    Var2 = C * Var1
    Var3 = np.tanh(Var2)
    if xNext < xc:
        Var4 = 1 + Var3
        Var5 = Var4 * vNext
        return Var5
    else:
        Var6 = vMax - vNext
        Var7 = vNext + (Var6 * Var3)
        return Var7

#Detmines is lambda is valid
def Lam(delX):
    if delX <= 100:
        return 0.5
    else:
        return 0

#Function for finding the difference between two values
def Delta(a,b):
    return (a - b)

#Number of cars on the road 
NoCars = 25

#Timestep and final time
dt = 0.001
tFinal = 1000

#The time array
t = np.linspace(0,tFinal,int(tFinal/dt))

#Velcocity of the cars are random between 1 and 5 ms-1
v = SFC64.uniform(1,5,NoCars)

#Inital distance, cars are staggered by 1m
x = np.flip(np.arange(0,NoCars,1))

#Records aceletation of cars
a = np.full(NoCars,0)


#Maximum velocity a car is allowed to travel
vmax = 14.66

#Deceleration of the Vechile
a = np.full(NoCars,-6)

#Reaction time of the driver in response to behaviour of the driver in front
tw = SFC64.uniform(0,1,NoCars)

hcStop = 8.7

#Driver Agressivness, less than 0 is agressive 0 is neutral and more than 0 is conservative
r = SFC64.uniform(-1,1,NoCars)

#Sensativity Coeffienct
Kon = 1

#Inital condtions assume cars are equally spaced and are travelling at the same velocity

#Determines if the ODE treats if it is on a circular road
RingRoad = True

#A euler method integral
def ODE(a,v,x,t,dt,tw,hcStop,NoCars,Kon,r,RingRoad):
    #Opens the txt to write the data
    out = open('Out.txt' , 'w')
    out1 = open('OutRVAL.txt' , 'w')
    for i in range(len(t)):
        for b in range(NoCars):
            #DeltaX is the difference between the n and n-1 car
            #The NoCars - 1 exists for the final car at the end of the ring
            if b == NoCars - 1:
                Delx = 0
            elif b == NoCars - 1 and RingRoad == True:
                Delx = Delta(x[0],x[b])
            else:
                Delx = Delta(x[b],x[b+1])
            
            #Xc
            if b == NoCars - 1:
                xc = (1 + r[b]) * v[b] * tw[b] - (v[b]**2/ 2*a[b]) + hcStop
            elif b == NoCars - 1 and RingRoad == True:
                xc = (1 + r[b]) * v[b] * tw[b] - (v[b]**2/ 2*a[b]) + (v[0]**2/ 2*a[0]) + hcStop
            else:
                xc = (1 + r[b]) * v[b] * tw[b] - (v[b]**2/ 2*a[b]) + (v[b+1]**2/ 2*a[b+1]) + hcStop
    
            #In accorance with the theory, determines what value should be taken
            if xc < hcStop:
                xc = (1 + r[b]) * hcStop
            else:
                pass
            
            #The DeltaV for the function
            if b == NoCars - 1:
                Delv = 0
            elif b == NoCars - 1 and RingRoad == True:
                Delv = Delta(v[0],v[b])
            else:
                Delv = Delta(v[b],v[b+1]) 
            
            #Oh my god WTF
            if b == NoCars - 1:
                dv = Kon * Vfunc(xc,Delx,0,vmax,Kon) - v[b] + Lam(xc)* Delv
            elif b == NoCars - 1 and RingRoad == True:
                dv = Kon * Vfunc(xc,Delx,v[b],vmax,Kon) - v[b] + Lam(xc)* Delv
            else:
                dv = Kon * Vfunc(xc,Delx,v[b+1],vmax,Kon) - v[b] + Lam(xc)* Delv      
    
            #Calcualtes the v and n values for the next timestep
            vn = v[b] + dt*dv
            xn = x[b] + x[b] + v[b]*dt + (0.5 * dv * dt**2)
            v[b] = vn
            x[b] = xn
            a[b] = dv
            
        #Writes the data the txt
        out.write(f"{t[i]} {x} {v} {a} \n")
    #Closes the txt file
    out1.write(f"{r}")
    out.close()
    out1.close()
    return

def main():
    ODE(a,v,x,t,dt,tw,hcStop,NoCars,Kon,r,RingRoad)
    
    return

if __name__ == "__main__":
    main()