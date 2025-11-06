sentence = " Python is best programming language Python  developed by Guido Von Rossom Python can be Python in best programming"

words = sentence.split()

unique = []

for word in words:
    if word not  in unique:
        unique.append(word)
print(' '.join(unique))


 
