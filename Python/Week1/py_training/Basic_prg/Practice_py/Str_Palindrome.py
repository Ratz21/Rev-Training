string = input("Enter a string: ")

#normalize it bcz humans write in upper case or lower case

string = string.replace(" ", "").lower()

if string == string[::-1]:
    print("is a palindrome")
else:
    print("is not a palindrome")


"""
string[::-1] → reverses the string using slicing.

.lower() → ignores case (so Madam counts).

.replace(" ", "") → removes spaces in case you’re checking phrases like "nurses run".
"""