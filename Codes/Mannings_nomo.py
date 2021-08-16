### Usage ###
# Nomogprahs based on Mannings Equation 
# Comparison between BlackMAX PP/SewerMAX for n = 0.009 (DN225 – DN600) & RCP Class 2  
### Created by YW on July 21 2021 ###

import numpy as np
from scipy import interpolate
import math
import matplotlib  
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt

n1 = 0.009 ## Manning coefficient
n2 = 0.013 # Class 2 mannings

pipe1 = 'BlackMAX PP'
pipe2 = 'RCP Class 2'
pipe3 = 'RCP Class 4'
# Set up output file paths & names
fig1nm = 'Nomograph_%s.pdf' % (pipe1) 
fig2nm = 'Nomograph_%s vs %s.pdf' % (pipe1, pipe2) 
fig3nm = 'Nomograph_%s vs %s.pdf' % (pipe1, pipe3) 

S = np.array([1.0/4, 1.0/5, 1.0/6, 1.0/7, 1.0/8, 1.0/9, 1.0/10, 1.0/20, 1.0/30, 1.0/40, 1.0/50, 1.0/60, 1.0/70, 1.0/80, 1.0/90, 1.0/100, 1.0/200, 1.0/300, 1.0/400, 1.0/500, 1.0/600, 1.0/700, 1.0/800, 1.0/900, 1.0/1000, 1.0/2000, 1.0/3000, 1.0/4000, 1.0/5000, 1.0/6000, 1.0/7000, 1.0/8000, 1.0/9000, 1.0/10000])
q = [0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
V = [0.5, 0.6, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0]

D1 = [0.225, 0.3, 0.373, 0.447, 0.522, 0.596] # BlackMAX D actual 
D1_label = [0.225, 0.3, 0.375, 0.450, 0.525, 0.6] #BlackMAX D labe (DN)
D2 = [0.225, 0.3, 0.375, 0.45, 0.525, 0.6, 0.75] #CLASS 2 
D3 = [0.225, 0.29, 0.365, 0.44, 0.51, 0.58, 0.75] #CLASS 4 Concrete - 25 years life

const1 = math.pi/(4**(5.0/3)*n1)
const2 = math.pi * 4 * n1**3

###### Plot ##########
fig, ax = plt.subplots(figsize=(8, 12))

### BlackMAX PP Diameter lines ###
for d in D1: 
    q1 =const1 * d**(8.0/3) * S**(1.0/2)
    ax.loglog(S, q1, '#0054A6')

### BlackMAX PP velocity lines ###
for v in V: 
    q_v = const2 * v**4 * S**(-1.5)
    ax.loglog(S, q_v, '#0054A6')    

### Concrete 2 Diameter lines ###
for d in D2: 
    q2 =math.pi/(4**(5.0/3)*n2) * d**(8.0/3) * S**(1.0/2)
    ax.loglog(S, q2, '#FF9B1A')

###  Concrete 2 velocity lines ###
v_c = 1
v_c1 = 0.6
v_c2 = 6

q_vc = math.pi * 4 * n2**3 * v_c**4 * S**(-1.5)
q_vc1 = math.pi * 4 * n2**3 * v_c1**4 * S**(-1.5)
q_vc2 = math.pi * 4 * n2**3 * v_c2**4 * S**(-1.5)

ax.loglog(S, q_vc, 'red')    
ax.loglog(S, q_vc1, 'red')   
ax.loglog(S, q_vc2, 'red')   

### Labels 
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
ax.set_title('Nomograph - %s vs %s' % (pipe1, pipe2), y=1.02, pad=20)

for d in D1_label:
    v = 0.5
    s_l = 4**(4.0/3) * n1**2 * v**2 / d** (4.0/3)
    q_l = v * math.pi * (d-0.03)  **2 /4 
    ax.text(s_l, q_l, "BMAX "+ str(int(d*1000)), rotation=330, size=6, color='#0054A6',
            horizontalalignment='left',
            verticalalignment='baseline',
            multialignment='center')

for d in D2:
    v = 0.5
    s_l = 4**(4.0/3) * n2**2 * v**2 / d** (4.0/3)
    q_l = v * math.pi * (d-0.03) **2 /4 
    ax.text(s_l, q_l, "C2 "+ str(int(d*1000)), rotation=330, size=6, color='#FF9B1A',
            horizontalalignment='left',
            verticalalignment='baseline',
            multialignment='center')

for v in V:
    d = 1.6
    s_l = 4**(4.0/3) * n1**2 * v**2 / d** (4.0/3)
    q_l = (v-0.1) * math.pi * d**2 /4
    # print (s_l, q_l)

    if v == 0.5:
        ax.text(min(S), q_l, str(v), rotation=48, size=6,
            horizontalalignment='left',
            verticalalignment='baseline',
            )
    else:
        ax.text(s_l, q_l, str(v), rotation=48, size=6,
        horizontalalignment='left',
        verticalalignment='baseline',
        )

ax.text(0.1, 60, "velocity (m/s)", rotation=55, size=10, 
            horizontalalignment='left',
            verticalalignment='top',
            )

ax.grid(True, which="both", ls='-' )

fig.savefig(fig2nm)
plt.show()
