Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
# dsa in py

lst=[10,20,30,69,71]
lst.append(30)
lst.remove(20)
print(lst)
[10, 30, 69, 71, 30]

lst.pop()
30
lst.pop(69)
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    lst.pop(69)
IndexError: pop index out of range
>>> lst.pop(-3)
30
>>> lst.pop(-1)
71
>>> # pop always moves from end to first In Last out filo
>>> 
>>> lst.reverse()
>>> print(lst)
[69, 10]
>>> 
>>> lst1= [3,79,78,21,45]
>>> lst1.append(21)
>>> print (lst1)
[3, 79, 78, 21, 45, 21]
>>> lst2= [23,21,34]
>>> lst.extend([4,5,6])
>>> print(lst2)
[23, 21, 34]
>>> 
>>> set1{7,3,8,9,10}
SyntaxError: invalid syntax
>>> set1 = {5,7,8,10,9}
>>> set1.add(7)
>>> print(set1)
{5, 7, 8, 9, 10}
>>> set1.add(9)
>>> print(set1)
{5, 7, 8, 9, 10}
>>> set1.add(11)
>>> print(set1)
{5, 7, 8, 9, 10, 11}
>>> set2={81,23,67,81}
>>> set1.union(set2)
{67, 5, 7, 8, 9, 10, 11, 81, 23}
>>> 
>>> # sroting a set
>>> 
>>> sorted(set1)
[5, 7, 8, 9, 10, 11]
