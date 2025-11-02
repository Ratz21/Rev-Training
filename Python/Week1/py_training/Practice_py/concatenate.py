def concatenate_choice(s,i,j):
    try:
        return s[i] + s[j]
    except IndexError:
        return "Error Invalid Indices for concatenation"

print(concatenate_choice("abcdefg",0,7))

"""
   Concatenates characters at index i and j from the string s.
   Displays error if indices are invalid.
   """