'''
Created on 20 Nov 2013

@author: cde2-sewell
'''
 
import math
import psutil
import requests
import xml.dom.minidom
from datetime import datetime
 
if __name__ == '__main__':
    pass

def define(name,problem):
    response = requests.get('http://runtime.azurewebsites.net/runtime/' + name)
    
    if response.status_code != 200:
        response = requests.post('http://runtime.azurewebsites.net/runtime/define/'+ name,data=problem)
        
        
def delegate(method,parameters):
    request_str = 'http://runtime.azurewebsites.net/runtime/' + method
    
    for param in parameters:
        request_str += '/' + str(param)
        
    response = requests.get(request_str)
    dom = xml.dom.minidom.parseString(response.text)
    xml_return = dom.getElementsByTagName('Return')
    print('CPU: ' + str(psutil.cpu_percent(interval=1)) + '%' + ' DELEGATED at ' + str(datetime.now().isoformat()) + ' ' + str(xml_return[0].firstChild.nodeValue)) 
    return int(xml_return[0].firstChild.nodeValue)    
 
def is_prime(n):
   
    '''Is n integer ?'''
    n = abs(int(n))
    '''Is n less than 2 ? '''
    if n < 2:
        return 0
    '''Is n 2 ? '''
    if n == 2:
        return 1
    
    '''Is n even ?'''   
    if psutil.cpu_percent(interval=1) >= 50:
        is_even = delegate("Modulus",[n,2])       
    else:
        is_even = n % 2
        print('CPU: ' + str(psutil.cpu_percent(interval=1)) + '%' + ' LOCAL')
        
    if is_even == 0:
        return 0
        
    '''Create number range starting at 3 iterating 2 to square root of n!'''
    if psutil.cpu_percent(interval=1) >= 50:
        n_sqrt = delegate("PlusSquare",[1,n])
    else:
        n_sqrt = int( math.sqrt(n) + 1)
        print('CPU: ' + str(psutil.cpu_percent(interval=1)) + '%' + ' LOCAL')

    for x in range(3,n_sqrt, 2):
        '''Is n modulus x possible ?'''
        if psutil.cpu_percent(interval=1) >= 50:
            prime = delegate("Modulus",[n_sqrt,x])
        else:
            prime = n_sqrt % x
            print('CPU: ' + str(psutil.cpu_percent(interval=1)) + '%' + ' LOCAL') 

        if prime == 0:  
            return 0
        
    print (n)
    return 1
 
 
numbers_to_find = 10000
numbers_found = 0

define("PlusSquare",open('PlusSquare.xml','r').read())

for n in range(0, numbers_to_find):
    numbers_found += is_prime(n)
    
print (numbers_found)
