# dict1 = {'a': 1, 'b': 2}
# dict2 = {'b': 3, 'c': 4}
#
# merged = {**dict1, **dict2}
# print(merged)


import numpy as np

dict1 = {'a': 1, 'b':2}
dict2 = {'c': 3 , 'd': 4}

merge = {**dict1 , **dict2}
print(merge)



marks = np.array([[50, 60, 70],
[80, 90, 100]])
bonus = 10
# Broadcasting adds 10 to every element
print(marks + bonus)