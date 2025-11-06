li=[1,2,3,2,4,5,1,6,3] # list creation
s1=set(li) # set conversion
duplicate=[] # value get stored here
for i in s1: # S1
    if li.count(i)>1: # set count  greater than 1
        duplicate.append(i) # adding the element
print(duplicate)   # printing the element


