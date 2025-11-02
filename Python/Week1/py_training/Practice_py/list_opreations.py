def demo_list():

    arr = [10,20,30,40,50]
    slice1 = arr[0:2]
    slice2 = arr[2:4]
    slice3 = arr[0:3]
    arr.append(69)
    arr.append(81)
    arr.extend([70,90])
    arr.insert(0,5)

    return arr,slice1,slice2,slice3 #return always inside function
print(demo_list())

"""arr = [...] creates a mutable sequence.

arr[i:j] returns elements from index i to j-1. Negative indices allowed.

arr[::k] uses step k (k can be negative to reverse).

append(x) is O(1) amortized; extend(iterable) concatenates; insert(index, x) is O(n) because elements shift.

Complexity

Slicing O(k) where k = number of items in slice (creates new list).

append amortized O(1); insert(0,x) O(n)."""