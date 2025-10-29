"""Print Pyramid"""
rows= int(input("Enter the number of rows: "))
for i in range(rows):

    for j in range(rows - i - 1):
        print(" ", end="")
        # print stars after spaces
    for k in range(2 * i + 1):
        print("*", end="")
    print() #move to next line

