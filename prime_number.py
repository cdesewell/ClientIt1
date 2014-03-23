'''
Created on 20 Nov 2013

@author: cde2-sewell
'''
import sys
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
    
    return float(xml_return[0].firstChild.nodeValue)    

def computeLocal(n):
    '''Create number range starting at 3 iterating 2 to square root of n + 1!'''
    
    n_squared = int(math.sqrt(n) + 1)
       
    for x in range(3,n_squared, 2):
        '''Is n modulus x possible ?'''
        prime = n % x
            
        if prime == 0:
            return 0

    return 1

def computeRemote(n):
    '''Create number range starting at 3 iterating 2 to square root of n + 1!'''
      
    n_squared = int(delegate("PlusSquare",[1,n]))
    
    prime = int(delegate("Loop",["And",3,n_squared,2,"Modulus",n,"i"]))
    
    if prime == 0:  
        return 0

    return 1

def is_prime(n, mode, dataFile):
    print('Testing '  + str(n))
    start = datetime.now()
    '''Is n integer ?'''
    n = abs(int(n))
    '''Is n less than 2 ? '''
    if n < 2:
        return 0
    
    '''Is n 2 or 3? '''
    if n == 2 | n == 3:
        return 1
    
    '''Is n 9 ? '''
    if n == 9:
        return 0  
    
    '''Is n even ?'''   
    if 0 == (n % 2):
        return 0

    cpu = psutil.cpu_percent(interval=1)

    if mode == "local":
        print('CPU: ' + str(cpu) + '%' + ' LOCAL')
        result = computeLocal(n)
        
    elif mode == "remote":
        print('CPU: ' + str(cpu) + '%' + ' DELEGATED')
        result = computeRemote(n)
        
    else:
        if cpu >= 50:
	    print('CPU: ' + str(cpu) + '%' + ' DELEGATED')
            result = computeRemote(n)
        else:
	    print('CPU: ' + str(cpu) + '%' + ' LOCAL')
            result = computeLocal(n)

    finish = datetime.now()
    dataFile.writelines(str(finish - start) + ","); 
    return result

mode = (sys.argv[1])
numbers_to_find = 200
numbers_found = 0
n =  150000
define("PlusSquare",open('PlusSquare.xml','r').read())
dataFile = open('data'+mode+'.csv','w')
while numbers_found < numbers_to_find:
    n += 1
     
    result = is_prime(n, mode, dataFile)
     
    if result == 1:
        print(str(n) + ' is a prime!')
        numbers_found += result


dataFile.close()       
print(numbers_found)
