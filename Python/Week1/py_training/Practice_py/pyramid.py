"""Print Pyramid"""
rows= int(input("Enter the number of rows: "))
for i in range(rows):

    for j in range(rows - i - 1):
        print(" ", end="")
        # print stars after spaces
    for k in range(2 * i + 1):
        print("*", end="")
    print() #move to next line

rows = int(input("Enter the number of rows: "))

for i in range rows:

    for j in range(rows - i - 1):
        print(" " , end="")

    for k in range(2 * i + 1):
        print("*" , end="")



        # rows = int(input("Enter the number of rows:"))
        #
        # for i in range rows:
        #
        #     for j in range(rows - i -1):
        #         print(" ", end="")
        #
        #     for k in range(2*i + 1):
        #         print("*", end="")



  def pascals_triangle(n):
     if n <= 0:
          return []
     triangle = [[1]]

     for i in range(1,n):
         prev = tirangle[-1]

         row [1]

         for j in range(1,len(prev)):
             row.append(prev[j-1] + prev[j])

        row.append(1)
        triangle.append(row)
     return triangle

if __num__ == "__main__":
    print(pascals_triangle(5)))












