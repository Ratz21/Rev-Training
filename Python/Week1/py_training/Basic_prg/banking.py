"""
Banking Interest Calculations
"""
#until we dont add from interest_cal its a module after adding
# that its a interest also we can add* for importing other functions
# we cam also add import from func name and add *
# from  interest_calculation import simple_interest_calc , comp_interest_calc
#
# prin = float(input('Principal: '))
# ny = float(input('Years: '))
# roi = float(input('Rate of Interest: '))
#
# si, amt = simple_interest_calc(prin=prin, ny=ny, roi=roi)
# print(f'Simple Interest: {si:.2f}%'

# Simple Interest Calculatorfro
# Taking input from user
from myPackage import *
principal = float(input("Enter the Principal amount: "))
rate = float(input("Enter the Rate of Interest (per year): "))
time = float(input("Enter the Time period (in years): "))

# Formula for Simple Interest
simple_interest = (principal * rate * time) / 100

# Total amount = Principal + Interest
total_amount = principal + simple_interest

# Display results
print(f"\nSimple Interest: {simple_interest:.2f}")
print(f"Total Amount after {time} years: {total_amount:.2f}")
