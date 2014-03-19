'''
Created on 20 Nov 2013
 
@author: cde2-sewell
'''

import psutil

for x in range(30):
   
    if psutil.cpu_percent(interval=1) >= 70.0:
        print("CPU usage too high")
        
