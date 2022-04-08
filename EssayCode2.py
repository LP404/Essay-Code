#Imports the files
import numpy as np


Seed = 9865740982869423
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

NoCars = 75

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

def getNoCars():
    global NoCars
    return NoCars


#A euler method integral
def ODE(a,v,x,t,dt,tw,vmax,anMin,hcStop,NoCars,Kappa,C,r,RingRoad):
    #Opens the .CSVs to write the data
    time = open('time.txt' , 'w')
    displacment = open('displacment.txt','w')
    velocity = open('velocity.txt','w')
    acceleration = open('acceleration.txt','w')
    rVals = open('rVals.txt' , 'w')
    CarNum = open('CarNum.txt' , 'w')
    for i in range(len(t)):
        for b in range(NoCars):
            #DeltaX is the difference between the n and n-1 car
            #The NoCars - 1 exists for the final car at the end of the ring
            if b == (NoCars - 1):
                Delx = 0
            elif b == (NoCars - 1) and RingRoad == 1:
                Delx = Delta(x[0],x[b])
            else:
                Delx = Delta(x[b],x[b+1])
            
            #Xc
            if b == (NoCars - 1):
                xc = (1 + r[b]) * v[b] * tw[b] - (v[b]**2/ 2*anMin[b]) + hcStop
            elif b == (NoCars - 1) and RingRoad == 1:
                xc = (1 + r[b]) * v[b] * tw[b] - (v[b]**2/ 2*anMin[b]) + (v[0]**2/ 2*anMin[0]) + hcStop
            else:
                xc = (1 + r[b]) * v[b] * tw[b] - (v[b]**2/ 2*anMin[b]) + (v[b+1]**2/ 2*anMin[b+1]) + hcStop
    
            #In accorance with the theory, determines what value should be taken
            if xc < hcStop:
                xc = (1 + r[b]) * hcStop
            else:
                pass
            
            #The DeltaV for the function
            if b == (NoCars - 1):
                Delv = 0
            elif b == (NoCars - 1) and RingRoad == 1:
                Delv = Delta(v[0],v[b])
            else:
                Delv = Delta(v[b],v[b+1]) 
            
            #Oh my god WTF
            if b == (NoCars - 1):
                dv = Kappa * (Vfunc(xc,Delx,0,vmax,C) - v[b]) + Lam(xc)* Delv
            elif b == (NoCars - 1) and RingRoad == 1:
                dv = Kappa * (Vfunc(xc,Delx,v[b],vmax,C) - v[b]) + Lam(xc)* Delv
            else:
                dv = Kappa * (Vfunc(xc,Delx,v[b+1],vmax,C) - v[b]) + Lam(xc)* Delv      
    
            #Calcualtes the v and n values for the next timestep
            vn = v[b] + dt*dv
            xn = x[b] + x[b] + v[b]*dt + (0.5 * dv * dt**2)
            v[b] = vn
            x[b] = xn
            a[b] = dv
            
            
            if i == (len(t) - 1) and b == (NoCars-1):
                displacment.write(f"{x[b]}")
                velocity.write(f"{v[b]}")
                acceleration.write(f"{a[b]}")  
            else:
                displacment.write(f"{x[b]};")
                velocity.write(f"{v[b]};")
                acceleration.write(f"{a[b]};")
            
        #Writes the data the CSVs
        if i == (len(t) - 1):
            time.write(f"{t[i]}")
        else:
            time.write(f"{t[i]};")
        
        
    #Closes the txt file
    
    for k in range(len(r)):
        if k == (len(r) - 1):
            rVals.write(f"{r[k]}")
        else:
            rVals.write(f"{r[k]};")
    
    rVals.close()
    time.close()
    displacment.close()
    velocity.close()
    acceleration.close()
    
    CarNum.write(f"{NoCars}")
    CarNum.close()
    
    return

def main():
    #Number of cars on the road 
    global NoCars

    #Timestep and final time
    dt = 0.0025
    tFinal = 500

    #The time array
    t = np.linspace(0,tFinal,int(tFinal/dt))

    #Velcocity of the cars are random between 1 and 5 ms-1
    v = SFC64.uniform(1,5,NoCars)

    #Inital distance, cars are staggered by 1m
    # x = np.arange(0,NoCars*15+15,15)
    # x[0] = 1
    # x = np.flip(x)
    x = np.flip(np.arange(1,NoCars+1,1))

    #Records aceletation of cars
    a = np.full(NoCars,0)


    #Maximum velocity a car is allowed to travel
    vmax = 10

    #Deceleration of the Vechile
    anMin = np.full(NoCars,-3)

    #Reaction time of the driver in response to behaviour of the driver in front
    tw = SFC64.uniform(0,1,NoCars)

    hcStop = 8.7

    #Driver Agressivness, less than 0 is agressive 0 is neutral and more than 0 is conservative
    r = SFC64.uniform(-1,1,NoCars)

    #Sensativity Coeffienct
    C = 0.05
    
    #Reaction Coeffienct
    Kappa = 0.41

    #Inital condtions assume cars are equally spaced and are travelling at the same velocity

    #Determines if the ODE treats if it is on a circular road
    RingRoad = 1
    
    ODE(a,v,x,t,dt,tw,vmax,anMin,hcStop,NoCars,Kappa,C,r,RingRoad)
    
    return

if __name__ == "__main__":
    main()