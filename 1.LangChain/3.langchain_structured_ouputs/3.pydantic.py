from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class Student(BaseModel):
    name: str = 'Obama'  ### default value(optional)
    age: Optional[int] = None   ### default value(mandatory)
    Email: EmailStr
    cgpa: float = Field(gt=0, 
                        lt=10, 
                        default=5, description="Enter CGPA from 0-10")



# new_student = {'name': 'Aman'}
# new_student = {'name': 32}
# new_student = {}

new_student = {'name': 'Aman', 'age': 22}
new_student = {'name': 'Aman', 'age': '22'}   ### convert into required type on its own if possible


new_student = {'name': 'Aman', 'age': 22, 'Email': 'abc'}
new_student = {'name': 'Aman', 'age': 22, 'Email': 'abc@gmail.com'}


new_student = {'name': 'Aman', 'age': 22, 'Email': 'abc@gmail.com'}
new_student = {'name': 'Aman', 'age': 22, 'Email': 'abc@gmail.com', 'cgpa':0}
new_student = {'name': 'Aman', 'age': 22, 'Email': 'abc@gmail.com', 'cgpa':7.8}
new_student = {'name': 'Aman', 'age': 22, 'Email': 'abc@gmail.com', 'cgpa':7.8}


student = Student(**new_student)
print("--------------------",student)
print("--------------------",type(student))
print("--------------------",dict(student))