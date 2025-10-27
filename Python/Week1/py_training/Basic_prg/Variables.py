age=22
height=6.1
name="Raj"
is_student=True

# ## printing the variables
#
print("age :",age)
print("Height:",height)
print("Name:",name)

#
# age=21
# height=5'9

# #type checking and conversion

age=25
print(type(age))

age_str=str(age)
print(age_str)
print(type(age_str))


# # Dynamic Typing
var=19 #int
print(type(var))

var="Hello" #str
print(type(var))

var=3.14 #float
print(type(var))

#
# ##input by default each var which takes input is in string
# ## we can convert it to int
#
age=int(input("What is the age"))
print(age,type(age))


## simple calculator

num1=float(input("What is the first number"))
num2=float(input("What is the second number"))

add = num1+num2
difference = num1-num2
quotient = num1/num2

print(sum)
print(difference)
print(quotient)