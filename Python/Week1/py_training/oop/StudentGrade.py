from oop.StudentDetail import StudentDetail

rollno = int(input("Enter roll no: ")) # this a driver class
name = input('Name: ')
m1 = int(input('Mark 1: '))
m2 = int(input('Mark 2: '))
m3 = int(input('Mark 3: '))

stud = StudentDetail(rollno,name,m1,m2,m3)
print(f'{stud.rollno}\n {stud.sname} \n {stud.calc_tot()} \n' f'{stud.calc_avg()}')