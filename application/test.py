
# Python code demonstrate the working of sorted() 
# and itemgetter 
  
# importing "operator" for implementing itemgetter 
import operator
from operator import itemgetter, attrgetter 
  
# Initializing list of dictionaries 
lis = [
    { "name" : "Nandini", "age" : 20, 'k1': {'k2', 1}},  
    { "name" : "Manjeet", "age" : 20, 'k1': {'k2', 3}}, 
    { "name" : "Nikhil" , "age" : 19, 'k1': {'k2', 2}}
]

lis.sort(key=lambda x: x['k1']['k2'])
print(lis)