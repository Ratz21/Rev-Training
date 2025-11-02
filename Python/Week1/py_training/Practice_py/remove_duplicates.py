def remove_duplicates(s):

    result = ""

    for ch in s:
        if ch not in result:
            result += ch
    return result

print(remove_duplicates("nurses"))


def remove_duplicates(s):
    result = ""

    for ch in s:
        if ch not in result:
            result += ch

    return result
print(remove_duplicates("Bavarian Motor works"))