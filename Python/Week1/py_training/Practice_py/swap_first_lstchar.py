def swap_first_lstchar(s):

    if len(s) < 2:
        return "error: Not enough character to swap"
    return s[-1] + s[1:-1]+s[0]


print(swap_first_lstchar("Bavarian"))

"""Logic:

Strings are immutable, so create a new one.

s[-1] gives last char, s[0] first, s[1:-1] middle part.

Handle short strings separately.

🧠 Interview Notes:

Quick string slicing test.

Must check boundary conditions (len < 2)."""