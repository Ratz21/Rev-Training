def camel_to_snakecase(s):

    result = ""
    for ch in s:
        if ch.isupper():
            if result:
                result += '_'
            result += ch.lower()

        else:
            result += ch

    return result

print(camel_to_snakecase("camel_to_snakecase"))
