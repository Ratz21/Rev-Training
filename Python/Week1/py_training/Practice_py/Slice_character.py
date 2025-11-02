def Slice_character(s, start , end):

    try:
        Sliced = s[start:end]
        if not Sliced:
            raise ValueError
        return Sliced

    except:
        return "Error invalid sliced indices"

print(Slice_character("Interview" , 2, 6))

"""
    Slices characters between user-given start and end indices.
    Displays error if indices are invalid.
    """



# Try slicing between start and end.
#
# If slice is empty or invalid, show an error.
#
# Slicing is safe in Python, but empty result may signal invalid range.
#
# 🧠 Interview Notes:
#
# Check understanding of slicing and exception handling.
#
# Could replace try/except with explicit bounds check: