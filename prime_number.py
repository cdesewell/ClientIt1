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
        print(response)
        
def delegate(method,parameters):
    request_str = 'http://runtime.azurewebsites.net/runtime/' + method
    
    for param in parameters:
        request_str += '/' + str(param)
        
    response = requests.get(request_str)
    dom = xml.dom.minidom.parseString(response.text)
    xml_return = dom.getElementsByTagName('Return')
    print('CPU: ' + str(psutil.cpu_percent(interval=1)) + '%' + ' DELEGATED at ' + str(datetime.now().isoformat()) + ' ' + str(xml_return[0].firstChild.nodeValue)) 
    return float(xml_return[0].firstChild.nodeValue)    
 
def is_prime(n):
    print('Testing '  + str(n))
    '''Is n integer ?'''
    n = abs(int(n))
    '''Is n less than 2 ? '''
    if n < 2:
        return 0
    
    '''Is n 2 ? '''
    if n == 2:
        return 1
    
    '''Is n even ?'''   
    if 0 == (n % 2):
        return 0

    '''Create number range starting at 3 iterating 2 to square root of n + 1!'''
    if psutil.cpu_percent(interval=1) >= 50:
        n_squared = int(delegate("PlusSquare",[1,n]))
        prime = delegate("Loop",["Or",3,n_squared,2,"Modulus",n,"i"])
        if prime != 1:
            return 0

    else:
        print('CPU: ' + str(psutil.cpu_percent(interval=1)) + '%' + ' LOCAL')
        n_squared = int(math.sqrt(n) + 1)
   
        for x in range(3,n_squared, 2):
            '''Is n modulus x possible ?'''
            prime = n % x
            if prime == 0:
                return 0

    return 1
 
 
numbers_to_find = 5
numbers_found = 0
n = 0
define("PlusSquare",open('PlusSquare.xml','r').read())


while numbers_found < numbers_to_find:
    n += 1
    result = is_prime(n)
    if result == 1:
        print(str(n) + ' is a prime!')
        numbers_found += result
          
print(numbers_found)
