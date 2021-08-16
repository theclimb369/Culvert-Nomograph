##### Outlet nomograph submerged ######
## Assumption - Full flow 
## Package required: Pynomo 
## Pynomo manual: http://lefakkomies.github.io/pynomo-doc/index.html
#@ Created by YW on 10 August 2021
#! Work in Progress!

import sys
from pyx import text
sys.path.insert(0, "..")
import math
import numpy as np

text.set(mode="latex")
# sys.path[:0] = [".."]
from pynomo.nomographer import Nomographer

### Parameter Setup ###
Ke = 0.5
n = 0.011
C1 = 1 + Ke
C2 = 19.63 * 4**(4.0/3) * n**2
C3 = math.log10(2/9.81/math.pi)
print(C1, C2)

L_min = 20
L_max = 200
D_min = 0.3
D_max = 4.5
E_min = C1 + C2*L_min/D_max**1.33
E_max = C1 + C2*L_max/D_min**1.33
print (E_min, E_max)

### Build Block 1 - D, Reference line, L ###
D1_params = {
    'u_min': 0.3,
    'u_max': 4.5,
    'function': lambda u:1.33*math.log10(u),
    'title': r'$D$ in $m$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    # 'align_x_offset': 0.5,
    'scale_type': 'log',
    'tag': 'Diameter',
}

E1_params = {
    'u_min': 1.54,
    'u_max': 16.5,
    'function': lambda u:math.log10((u-C1)/C2),
    'title': r'',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tag': 'Eq',
}

L1_params = {
    'u_min': L_min,
    'u_max': L_max,
    'function': lambda u:-math.log10(u),
    'title': r'$L$ in $m$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'scale_type': 'log',
}


block_2_params = {
    'block_type': 'type_1',
    'width': 8.0,
    'height': 20.0,
    'f1_params': D1_params,
    'f2_params': E1_params,
    'f3_params': L1_params,
    'proportion':0.5,
    'isopleth_values': [[1.2, 'x', 40]],
}

### Build Block 2 - Q, Reference line, H ###
Q_params = {
    'u_min': 0.07,
    'u_max': 60.0,
    'function': lambda u:2*math.log10(u)+C3,
    'title': r'$Q (m^3/s)$',
    'tick_levels': 3,
    'tick_text_levels': 1,
    'scale_type': 'log',
} 

E_params = {
    'u_min': 1.54,
    'u_max': 16.5,
    'function': lambda u:math.log10(u),
    'title': r'',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tag': 'Eq',
}

H_params = {
    'u_min': 0.1,
    'u_max': 10,
    'function': lambda u:-math.log10(u),
    'title': r'$H$ in $m$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'scale_type': 'log',
}

block_1_params = {
    'block_type': 'type_1',
    'width': 15.0,
    'height': 15.0,
    'f1_params': Q_params,
    'f2_params': E_params,
    'f3_params': H_params,
    'proportion':0.5,
    'isopleth_values': [[1.95, 'x', 'x']],
}

main_params = {
    'filename': 'Outlet_nomo.pdf',
    'paper_height': 20.0,
    'paper_width': 15.0,
    'block_params': [block_2_params, block_1_params],
    # 'block_params': [block_2_params],
    'transformations': [('scale paper',)],
    'title_str': r'$H = (1 + K_e + \frac{19.63 \cdot n^2 \cdot L}{R^1.33}) \cdot (\frac{v^2}{2g})$',
    # 'title_x': 5.0,
    'debug': False, 
}
Nomographer(main_params)
