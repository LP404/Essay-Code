import math as m
import numpy as np
from timeit import default_timer as timer
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
plt.rcParams["figure.figsize"] = (10,3)


#Force function, takes coordinates as inputs
def force1(x,y,z):
    
    #Calculates force
    V = - 4 * m.pi**2 * (np.sqrt(x**2 + y**2 + z**2))**3
    
    #Calculates forces in x,y and z directions
    Vx = V * x / np.sqrt(x**2 + y**2 + z**2)
    Vy = V * y / np.sqrt(x**2 + y**2 + z**2)
    Vz = V * z / np.sqrt(x**2 + y**2 + z**2)
    
    #mass = 1, therefore there is no need to divide by mass as F = a in this case
    return Vx, Vy, Vz

#Finds angular momentum, takes positions and velocities as inputs
def AngMo(x,y,z,vx,vy,vz):
    m = 1
    #Calcualtes force
    V = (vx,vy,vz)*m
    X = (x,y,z)
    
    #Cross product of X and V vectors
    L =  np.cross(X,V)
    
    #Square root of dot product of itself (L)
    L = np.sqrt(L.dot(L))
    
    return L
    

#Verlet function
def Verlet3(t0,tfinal,Pos,Vel,dt):
    #Establishes inital conditions
    t = t0
    x = Pos[0]
    y = Pos[1]
    z = Pos[2]
    
    vx = Vel[0]
    vy = Vel[1]
    vz = Vel[2]
    
    #Calculates starting angular momentum
    L = AngMo(x, y, z, vx, vy, vz)
    
    #Opens a .txt to write data to
    out = open('Task1.txt' , 'w')
    
    #Calculates positions, velocites and accelerations for the body
    #Calculates inital forces
    fx , fy, fz  = force1(x,y,z)
    while t <= tfinal:
        
        
        #Calculates half step veloctiy for x,y,z
        vxhalf = vx + dt/2 * fx
        vyhalf = vy + dt/2 * fy
        vzhalf = vz + dt/2 * fz
        
        #Calculates x,y,z for current time step
        xn = x + dt*vxhalf
        yn = y + dt*vyhalf
        zn = z + dt*vzhalf
        
        #Writes positions, accelerations and angular momentum to the.txt
        out.write(f"{xn} {yn} {zn} {fx} {fy} {fz} {L} \n")
        
        #Calculates accelerations to find veloctiy for current time step
        fx , fy, fz = force1(xn,yn,zn)
        
        vxn = vxhalf + dt/2* fx
        vyn = vyhalf + dt/2* fy
        vzn = vzhalf + dt/2* fz 
        
        #Assigns values for new x,y,z to the variables occupied by previous x,y,z values for next loop
        x = xn
        y = yn
        z = zn
        
        #Does the same as above but for velocites
        vx = vxn
        vy = vyn
        vz = vzn
        
        #Calculates angular momentum for current positions and velocities
        L = AngMo(x, y, z, vx, vy, vz)
        
        #Increases time by one timestep
        t += dt
    
    
    #Closes .txt once all values are written to it
    out.close()


#Inital conditions, unused.
T = 1
omega = (2 * m.pi) / T
dt = 1e-4
output_stride = 100
Natom = 1
t0 = 0
tFinal = 1

#Calls Verlet integrator with inital conditions
Verlet3(t0,tFinal,(-1,0,0),(0,2*m.pi,0),dt)

#Reads in data from txt
DataIn = pd.read_csv('Task1.txt', sep = " ", header = None).T.to_numpy()

#Plots orbit in 3D with appropriate labels, headings and legend
plt.figure(1, figsize = (9,9))
ax = plt.axes(projection='3d')
ax.scatter3D(0,0,0, color = 'red', label = 'Orgin of Force')
ax.plot3D(DataIn[0], DataIn[1], DataIn[2], label = ' Orbit ')
ax.set_xlabel('x(t)')
ax.set_ylabel('y(t)')
ax.set_zlabel('z(t)')
ax.set_title("Model of orbiting body", loc = 'center')
ax.legend(loc = 'upper right')

#Plots how x and y change over time with appropriate labels, headings and legend
plt.figure(2)
plt.plot(np.arange(0,1+1e-4,1e-4), DataIn[0], label="x(t)")
plt.plot(np.arange(0,1+1e-4,1e-4), DataIn[1], label ="y(t)")
plt.legend(loc="best")
plt.title(" Behaviour along x(t) and y(t) ")
plt.ylabel('x,y co-ordinate')
plt.xlabel('t (s)')
plt.grid()
plt.show()

#Plots angular momentum with appropriate labels, headings and legend
plt.figure(3)
plt.plot(np.arange(0,1+1e-4,1e-4), DataIn[6])
plt.grid()
plt.title('Angular momentum vs time', loc = 'right')
plt.xlabel('T, time')
plt.ylabel('Angular momentum, $kgm^2/sec$')
