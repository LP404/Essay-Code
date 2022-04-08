#Imports libarires
import numpy as np
import matplotlib.pyplot as plt
import EssayCode2 as EC2

#Sets up random number generator
Seed = 9865740982869423
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

NoCars = EC2.getNoCars()
 
#Genrates colours for each car
Colour = [[SFC64.uniform(0,1,1)[0],SFC64.uniform(0,1,1)[0],SFC64.uniform(0,1,1)[0]] for _ in range(NoCars)]

#Imports data
rVals = np.loadtxt('rVals.txt', delimiter = ";")
x = np.loadtxt('displacment.txt', delimiter = ";")
v = np.loadtxt('velocity.txt', delimiter = ";")
a = np.loadtxt('acceleration.txt', delimiter = ";")
t = np.loadtxt('time.txt', delimiter = ";")


#Reshapes fata for plotting
x = x.reshape((len(t),NoCars))
v = v.reshape((len(t),NoCars))
a = a.reshape((len(t),NoCars))

x = x.T
v = v.T
a = a.T


#Gets indicies for cars that have rValues for the three types of dirving style
#If there is no valid rVals it will move on
try: 
    Agg = np.where(rVals > 0)[0]
except:
    TypeError

try:
    Con = np.where(rVals < 0)[0]
except:
    TypeError
    
try:
    Neut = np.where(rVals == 0)[0]
except:
    TypeError


#Plots data
for i in range(len(a)):
    plt.figure(1)
    plt.title('Acceleration of Cars')
    plt.ylabel('Acceleration')
    plt.xlabel('Time')
    plt.scatter(t,a[i],s=1, color = Colour[i])
    plt.figure(2)
    plt.title('Velocity of Cars')
    plt.ylabel('Velocity')
    plt.xlabel('Time')
    plt.scatter(t,v[i],s=1, color = Colour[i])
    plt.figure(3)
    plt.title('Displacment of Cars')
    plt.ylabel('Displacment')
    plt.xlabel('Time')
    plt.scatter(t,x[i],s=1, color = Colour[i])
  
#Data will be plotted provided there is a valid array generated from the previous try else block
try:    
    for i in range(len(Agg)):
        plt.figure(4)
        plt.title('Acceleration of Aggressive Cars')
        plt.ylabel('Acceleration')
        plt.xlabel('Time')
        plt.scatter(t,a[Agg[i]],s=1, color = Colour[i])
        plt.figure(5)
        plt.title('Velocity of Aggressive Cars')
        plt.ylabel('Velocity')
        plt.xlabel('Time')
        plt.scatter(t,v[Agg[i]],s=1, color = Colour[i])
        plt.figure(6)
        plt.title('Displacment of Aggressive Cars')
        plt.ylabel('Displacment')
        plt.xlabel('Time')
        plt.scatter(t,x[Agg[i]],s=1, color = Colour[i])
except:
    NameError
 
try:
    for i in range(len(Con)):
        plt.figure(7)
        plt.title('Acceleration of Conservative Cars')
        plt.ylabel('Acceleration')
        plt.xlabel('Time')
        plt.scatter(t,a[Con[i]],s=1, color = Colour[i])
        plt.figure(8)
        plt.title('Velocity of Conservative Cars')
        plt.ylabel('Velocity')
        plt.xlabel('Time')
        plt.scatter(t,v[Con[i]],s=1, color = Colour[i])
        plt.figure(9)
        plt.title('Displacment of Conservative Cars')
        plt.ylabel('Displacment')
        plt.xlabel('Time')
        plt.scatter(t,x[Con[i]],s=1, color = Colour[i])
except:
    NameError

try:    
    for i in range(len(Neut)):
        plt.figure(10)
        plt.title('Acceleration of Neutral Cars')
        plt.ylabel('Acceleration')
        plt.xlabel('Time')
        plt.scatter(t,a[Neut[i]],s=1, color = Colour[i])
        plt.figure(11)
        plt.title('Velocity of Neutral Cars')
        plt.ylabel('Velocity')
        plt.xlabel('Time')
        plt.scatter(t,v[Neut[i]],s=1, color = Colour[i])
        plt.figure(12)
        plt.title('Displacment of Neutral Cars')
        plt.ylabel('Displacment')
        plt.xlabel('Time')
        plt.scatter(t,x[Neut[i]],s=1, color = Colour[i])
except:
    NameError