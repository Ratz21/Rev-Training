"""Print all numbers in an interval"""


# start = int(input("Enter a number: "))
# end = int(input("Enter a number: "))
#
# print(f"prime numbers between {start} and {end} are:")
#
# # Logic begins
#
# for num in range(start, end+1):
#     if num > 1:   ##Prime nos are greater than 1
#         for i in range(2, int(num**0.5)+1): #this is for sqrt of num
#             if num % i == 0:
#                 break
#             else:
#                  print(num)

start = int(input("Enter a number: "))
end = int(input("Enter a number: " ))

print(f"prime numbers between {start} and {end} are: ")

for num in range(start , end):
    if num > 1:
        for i in range(2, int(num**0.5)+1): #this is for sqrt of num
            if num % i == 0:
                break
            else:
                print(num)





start = int(input("Enter a number: "))
end = int(input("Enter a number: "))

print(f"prime numbers between {start} and {end} are: ")


for num in range (start , end):
    if num > 1:
        for i in range(2, int(num**0.5+1)):
            if num % i == 0:
                break
            else:
                print(num)

"""
You only check divisors up to √num because:

If no smaller divisor exists, no larger one can either.

It saves time and makes your prime checker much faster.

"""








start = int(input("Enter a number: "))
end = int(input("Enter a number: "))

print(f"prime number betweeen {start} and {end} are:")

for num in range(start, end):
    if num > 1:
        for i in range(2, int(num**0.5+1)):
            if num % i == 0:
                break
            else:
                print(num)


start = int(input("Enter a number: "))
end = int(input("Enter a number:")

print(f"prime number between {start} and {end} are: ")

for num in range(start,end):
    if num > 1:
        for i in range(2, int(num**0.5+1)):
            if num % i == 0:
                break
            else:
                print(num)