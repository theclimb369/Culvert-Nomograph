### Usage ###
# Nomogprahs based on Colebrook White Equations
# BlackMAX PP/SewerMAX for n = 0.009 (DN225 – DN600)
### Created by YW on July 21 2021 ###
### Updated on XX ###

import numpy as np
from scipy import interpolate
import math
import matplotlib  
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from scipy.optimize import fsolve


k = 0.06 * 10**(-3)  ## equivalent hydraulic roughness m
mu = 1.01 * 10 ** (-6) ## kinematic viscosity of water m^2/s 
g = 9.8 ## gravity (m/s^2)
pipe1 = 'BlackMAX PP'
pipe2 = 'SewerMAX+ PP'


# Set up output file paths & names
fig1nm = 'Nomograph ColeBrook %s k-%.2f.pdf' % (pipe2, k*10**3) 

S = np.array([1.0/4, 1.0/5, 1.0/6, 1.0/7, 1.0/8, 1.0/9, 1.0/10, 1.0/20, 1.0/30, 1.0/40, 1.0/50, 1.0/60, 1.0/70, 1.0/80, 1.0/90, 1.0/100, 1.0/200, 1.0/300, 1.0/400, 1.0/500, 1.0/600, 1.0/700, 1.0/800, 1.0/900, 1.0/1000, 1.0/2000, 1.0/3000, 1.0/4000, 1.0/5000, 1.0/6000, 1.0/7000, 1.0/8000, 1.0/9000, 1.0/10000])
q = [0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
V = [0.5, 0.6, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0]

# D1 = [0.225, 0.3, 0.373, 0.447, 0.522, 0.596] # BlackMAX D actual 
D1 = [0.224, 0.297, 0.370, 0.433, 0.516] # BlackMAX D actual 
D1_label = [0.225, 0.3, 0.375, 0.450, 0.525, 0.6] #BlackMAX D labe (DN)

const1 = -math.pi * g**(1.0/2) / 2**(1.0/2)
const2 = k  / 3.7
const3 = 2.51 * mu / (2*g) ** (1.0/2)

###### Plot ##########
fig, ax = plt.subplots(figsize=(8, 12))

### BlackMAX PP Diameter lines - ColeBrook_white equation ###
for d in D1: 
    q1 =const1 * d**(5.0/2) * S**(1.0/2) * np.log10(const2 * d**(-1.0/2) + const3 * d**(-3.0/2) * S**(-1.0/2))
    # print (q)
    ax.loglog(S, q1, '#0054A6')

### BlackMAX PP velocity lines - ColeBrook-white approximation ###
for v in V: 
    # Approach I - approximation # 
    y = np.log10(1.558 / (v**2/(2*g*S*k)) ** 0.8 + 15.045 / (v**3/(2*g*S*mu)) ** 0.73)
    Dv = v**2 / (8 * g * S * y**2)
    Qv = v* math.pi * Dv**2 / 4.0
    ax.loglog(S, Qv, '#0054A6')

    # Approach II - fsolve #
    func = lambda D : v + 2*(2*g*D*S)**(0.5) * np.log10(const2 * D**(-1.0/2) + const3 * D**(-3.0/2) * S**(-1.0/2)) 
    D_initial_guess = Dv
    D_solution = fsolve(func, D_initial_guess)
    Q_cal = v* math.pi * D_solution**2 / 4.0
    # print ("The solution for V=%f S=%f is D = %f Q=%f Dv = %f Qv=%f " % (v, S, D_solution, Q_cal, Dv, Qv))
    ax.loglog(S, Q_cal, 'red')   
    
###  S~(D,V) approxi ColeBrook-white ###
# Sf = v**2 / (8*g*d*(np.log10(k/(3.7*d) + (6.28*mu/(v*d))**0.89))**2)
 
### Labeling ### 
ylabel1 = []

for i in q:
    ylabel1.append(str(i))
xlabel = []
xlabel1 = []
den = [4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
for i in den:
    deno = str(i)
    xlabel1.append("%.2f %%" % (1/i*100))
    xlabel.append(str(1) + "/" + str(deno))

ax1 = ax.twiny()
ax.set_xlim(max(S), min(S)) 
ax1.set_xlim(ax.get_xlim())
ax.set_ylim(0.005, 100) 
ax.set_yticks(q)
ax.set_xticks(S)
ax1.set_xscale('log')
ax1.set_xticks(S)
ax.set_yticklabels(ylabel1, Fontsize=5) 
ax.set_xticklabels(xlabel, rotation=90, Fontsize=5) 
ax1.set_xticklabels(xlabel1, rotation=90, Fontsize=5) 
ax.set_xlabel('Slope')
ax.set_ylabel('Flow')
ax.set_title('Nomograph (Colebrook white) - %s (k= %.2f mm)' % (pipe2, k*10**3), y=1.02, pad=20)


for d in D1_label:
    v = 0.5
    s_l = v**2 / (8*g*d*(np.log10(k/(3.7*d) + (6.28*mu/(v*d))**0.89))**2)
    # q_l =const1 * d**(5.0/2) * s_l**(1.0/2) * np.log10(const2 * d**(-1.0/2) + const3 * d**(-3.0/2) * s_l**(-1.0/2))

    q_l = v * math.pi * (d-0.03)  **2 /4 
    ax.text(s_l, q_l, "BMAX "+ str(int(d*1000)), rotation=330, size=6,
            horizontalalignment='left',
            verticalalignment='baseline',
            multialignment='center')

ax.text(0.1, 60, "velocity (m/s)", rotation=55, size=10,
            horizontalalignment='left',
            verticalalignment='top',
            )

ax.grid(True, which="both", ls='-' )

fig.savefig(fig1nm)
plt.show()
