

# class StudentDetail:
#       def __init__(self, rollno , sname, m1,m2,m3):
#           self.__rollno = rollno
#           self.__sname = sname
#           self.__m1 = m1
#           self.__m2 = m2
#           self.__m3 = m3
# #__ MEANS PRIVATE DATA WERE WE CAN MAKE THE METHOD PVT
#       def calc_tot(self):
#             return self.__m1 + self.__m2 + self.__m3
#
#       def calc_avg(self):
#             return self.calc_tot()/3

class StudentDetail:
    def __init__(self, rollno, sname, m1, m2, m3):
        self.__rollno = rollno
        self.__sname = sname
        self.__m1 = m1
        self.__m2 = m2
        self.__m3 = m3

    def calc_tot(self):
        return self.__m1 + self.__m2 + self.__m3

    def calc_avg(self):
        return self.calc_tot() / 3

    # getter methods
    def get_rollno(self):
        return self.__rollno

    def get_sname(self):
        return self.__sname
