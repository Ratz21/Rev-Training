def demo_person_dict():
    person = {
        "name": "Rajdeep",
        "age": 22,
        "City" : "Seattle"
    }
    person["age"] = 23
    person["profession"] = "Engineer"

    for k ,v in person.items():
        print(f"{k}: {v}")

print(demo_person_dict())