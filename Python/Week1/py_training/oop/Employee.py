class Employee:
    def __init__(self,empid,ename,bp): # self is written bcz of obj present in here
        self.empid = empid #paramters left side of self. is the instance variable and right is the object
        self.ename = ename
        self.bp = bp

    def calc_allowance(self, bp):# allowance is written here
        return (self.bp * 0.1) + (bp * 0.05)

    def cal_ded(self,bp):
        return self.bp * 0.03

    def calc_grosspay(self,bp):
        return self.bp + self.calc_allowance(bp)

    def calc_netpay(self,bp):
        return self.calc_grosspay(bp) - self.cal_ded(bp)

