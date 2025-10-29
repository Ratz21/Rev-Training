# Define the TeacherDetail class inheriting from College
from oop.Colllege import College


class TeacherDetail(College):
    def __init__(self, ccode, cname, empid, tname, dept):
        super().__init__(ccode, cname)
        self.empid = empid
        self.tname = tname
        self.dept = dept

    def display(self):
        print(f"College Code: {self._ccode}, College Name: {self._cname}")
        print(f"Emp ID: {self.empid}, Teacher Name: {self.tname}, Department: {self.dept}")

teacher = TeacherDetail(input("Enter College Code: "), input("Enter College Name: "),input ("Enter Emp ID:"),input ("Enter Teacher Name:"),input ("Enter Department:"))
(teacher.display())

# CLASS KEH BAHAR OBJECT AND
# CLASS KEH ANDHAR FUNCTION