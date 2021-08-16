##### Inlet nomograph submerged ######
## Package required: Pynomo 
## Pynomo manual: http://lefakkomies.github.io/pynomo-doc/index.html
#@ Created by YW on 12 August 2021

import sys
from pyx import text
sys.path.insert(0, "..")
import math
import numpy as np

text.set(mode="latex")
# sys.path[:0] = [".."]
from pynomo.nomographer import Nomographer

### Parameter Setup ###
# Square edge w/ headwall
C = 0.0398
Y = 0.67
C1 = 1.811**2 * 16 / math.pi**2 * C
C2 = Y - 0.01
# Groove end w/ headwall
C_G = 0.0292
Y_G = 0.74
C1_G = 1.811**2 * 16 / math.pi**2 * C_G
C2_G = Y_G - 0.01
# Groove end projecting
C_GP = 0.0317
Y_GP = 0.69
C1_GP = 1.811**2 * 16 / math.pi**2 * C_GP
C2_GP = Y_GP - 0.01

### Build Block 1 - D, Q, HW/D - Square Edge w Headwall ###
D_params = {
    'tag': "Diameter",
    'u_min': 0.3,
    'u_max': 4.5,
    'function': lambda u:5*math.log10(u),
    'title': r' D (m)',
    'title_draw_center': True,  
    'tick_side':'left',
    'extra_params': [{'u_min': 0.3,             
                    'u_max': 1.5,           
                    'tick_levels': 3,        
                    'tick_text_levels': 3,   
                    },                       
                    {'u_min': 1.5,             
                    'u_max': 4.5,           
                    'tick_levels': 3,        
                    'tick_text_levels': 2,   
                    }                        
                    ], 
    'tick_levels': 3,
    'tick_text_levels': 2,
}

Q_params = {
    'tag': "Flow",
    'u_min': 0.03,
    'u_max': 300.0,
    'function': lambda u:-2*math.log10(u),
    'title': r'$Q (m^3/s)$',
    'title_draw_center': True,  
    'extra_params': [{'u_min': 0.03,             
                    'u_max': 0.05,           
                    'tick_levels': 3,        
                    'tick_text_levels': 3,   
                    },                       
                    {'u_min': 0.05,             
                    'u_max': 10.0,           
                    'tick_levels': 4,        
                    'tick_text_levels': 2,   
                    },    
                    {'u_min': 10.0,             
                    'u_max': 300.0,           
                    'tick_levels': 3,        
                    'tick_text_levels': 2,   
                    }                       
                    ], 
    'tick_side':'left',
    'tick_levels': 3,
    'tick_text_levels': 1,
    'scale_type': 'log',
}

HW_params = {
    'tag': 'HW',
    'u_min': 0.75,
    'u_max': 6,
    'function': lambda u:math.log10(u-C2)-math.log10(C1),
    'title': r'',
    'tick_levels': 2,
    'tick_text_levels': 2,
    'extra_params': [{'u_min': 0.75,             
                'u_max': 0.8,           
                'tick_levels': 4,        
                'tick_text_levels': 4,   
                },   
                {'u_min': 0.8,             
                'u_max': 1.5,           
                'tick_levels': 4,        
                'tick_text_levels': 3,   
                },                      
                {'u_min': 1.5,             
                'u_max': 6.0,           
                'tick_levels': 2,        
                'tick_text_levels': 2,   
                }                        
                ], 
    # 'scale_type': 'log',
    'tick_side':'left',
    'title_x_shift': 1
}

block_1_params = {
    'block_type': 'type_1',
    'height': 15.0,
    'width': 10.0,
    'f1_params': D_params,
    'f2_params': Q_params,
    'f3_params': HW_params,
    'proportion':0.5,
    # 'isopleth_values': [[1.05, 3.4, 'x']],
}

### Build Block 2 & 3 HW/D conversion ###
def old_HW(HW):
    return C/C_G*(HW-C2_G)+C2 # HW = F(HW')
       
# def new_HW(HW):
#     return C_G/C*(HW-C2)+C2_G #HW' = F(HW)

def SQtoGP_HW(HW):
    return C/C_GP*(HW-C2_GP)+C2 # HW = F(HW')

HW_Groove={
    'tag':'HW',
    'u_min': 0.75,
    'u_max': 6,
    'function': lambda u:math.log10(old_HW(u)-C2)-math.log10(C1),
    'title': r'',
    'tick_levels': 2,
    'tick_text_levels': 2,
    'extra_params': [{'u_min': 0.75,            
                'u_max': 0.8,          
                'tick_levels': 4,        
                'tick_text_levels': 4,   
                },   
                {'u_min': 0.8,            
                'u_max': 1.5,           
                'tick_levels': 4,        
                'tick_text_levels': 3,   
                },                      
                {'u_min': 1.5,            
                'u_max': 6.0,           
                'tick_levels': 2,        
                'tick_text_levels': 2,   
                }                        
                ], 
    'tick_side':'left',
    'align_func':old_HW,
    'align_x_offset': 2,
    'title_y_shift':-18
}


HWG_block={
    'block_type': 'type_8',
    'f_params': HW_Groove,
    # 'isopleth_values': [['x']],
}

HW_GrooveP={
    'tag':'HW',
    'u_min': 0.75,
    'u_max': 6,
    'function': lambda u:math.log10(SQtoGP_HW(u)-C2)-math.log10(C1),
    'title': r'$HW/D$',
    'title_draw_center': True,  
    'tick_levels': 2,
    'tick_text_levels': 2,
    'extra_params': [{'u_min': 0.75,            
                'u_max': 0.8,          
                'tick_levels': 4,        
                'tick_text_levels': 4,   
                },   
                {'u_min': 0.8,            
                'u_max': 1.5,           
                'tick_levels': 4,        
                'tick_text_levels': 3,   
                },                      
                {'u_min': 1.5,            
                'u_max': 6.0,           
                'tick_levels': 2,        
                'tick_text_levels': 2,   
                }                        
                ],  
    'tick_side':'left',
    'align_func':SQtoGP_HW,
    'align_x_offset': 4,
}

HWGP_block={
    'block_type': 'type_8',
    'f_params': HW_GrooveP,
    # 'isopleth_values': [['x']],
}

main_params = {
    'filename': 'Inlet_nomo_multi.pdf',
    'paper_height': 20.0,
    'paper_width': 10.0,
    'block_params': [block_1_params, HWG_block, HWGP_block],
    'transformations': [('rotate', 0.01),('scale paper',)],
    'extra_texts': [{'x': 8.5,                                         
    'y': 4.5,                                          
    'text': 'Groove end projecting',                            
    'width': 5,                                        
    'pyx_extra_defs': [text.size.tiny]   
    },
    {'x': 7,                                            
    'y': 1.5,                                          
    'text': 'Groove end w HW',                            
    'width': 5,                                         
    'pyx_extra_defs': [text.size.tiny]   
    },
    {'x': 6,                                          
    'y': 4.5,                                          
    'text': 'Square edge w HW',                            
    'width': 5,                                         
    'pyx_extra_defs': [text.size.tiny]   
    }],
    'title_x': 8.0,
    'title_y': 19.3,
    'title_str': r'$\frac{HW}{D} = c ({\frac{1.811 Q}{AD^{0.5}}})^2 + Y - 0.01$',
    'debug': False,
}
Nomographer(main_params)
