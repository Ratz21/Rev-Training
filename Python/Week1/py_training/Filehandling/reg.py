"""REGEX PATTERN"""

import re

text = "I have 2 apples and 15 bananas"
pattern = r'\d+'   # \d+ means one or more digits

result = re.findall(pattern, text)
print(result)
