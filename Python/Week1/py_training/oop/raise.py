age = int(input("Enter your age: "))

if age < 18:
    raise ValueError("Age must be 18 or above to register.")
else:
    print("Access granted.")
