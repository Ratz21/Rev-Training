

from oop.Employee import Employee



empid = int(input('Emp id: '))
ename = input('EName:')
bp = float(input('Basic pay: '))


employee = Employee(empid,ename,bp)
employee.calc_grosspay(bp)
employee.calc_netpay(bp)


print(f'Emp id : {empid} \n Name: {employee.ename} \n'
      f'Gross pay: {employee.calc_grosspay(employee.bp)} \n'
      f'Net pay: {employee.calc_netpay(employee.bp)}')

