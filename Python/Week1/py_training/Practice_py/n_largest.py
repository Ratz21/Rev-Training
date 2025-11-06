import heapq  #heapq.nlargest() is optimized using a heap (faster for large lists).

                  # Returns top N largest elements in descending order.

num = [10,80,70,30,20]

n = 3

largest_n = heapq.nlargest(n, num)
print(largest_n)

