from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int


newPerson: Person = {'name' : 'Aman', 'Age' : 22}

print(newPerson)

newPerson: Person = {'name' : 'Aman', 'Age' : '22'}

print(newPerson)