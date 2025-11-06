person = {
   "Name":"Rajdeep",
    "age": 21,
    "City": "Pune"

}


#update

person ["age"] = 22
person ["City"] = "Dehuroad"

#print

for key, value in person.items():
    print(f"{key}: {value}")


