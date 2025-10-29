"""TRY AND CATCH BLOCK"""
from oop.ArithCalculations import ArithCalculations

n1= int(input("Enter a number:"))
n2= int(input("Enter another number: "))

calc = ArithCalculations(n1,n2)
print(f'{calc.add()}')
print(f'{calc.sub()}')
print(f'{calc.mult()}')


try:
    res= calc.div()
    print(res)

except ZeroDivisionError:
    print('0 in denominator')

else:
    print(res)

finally:
    print('Done!!')