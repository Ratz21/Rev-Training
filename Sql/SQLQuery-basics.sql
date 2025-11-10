-- JOINS 

use RevatureDB

CREATE TABLE Employee (
EmpID INT PRIMARY KEY ,
Name VARCHAR(35),
Dept VARCHAR(25),
Salary DECIMAL(10,2)
);






select * from Employee;


-- Make sure the DEPT table exists and has values 10, 20, 30, 40, 50
-- Now populate EMP with realistic data
INSERT INTO Employee (EmpID, Name, Dept, Salary) VALUES
(1001, 'Alice',   'IT',        65000.00),
(1002, 'Bob',     'IT',        50000.00),
(1003, 'Charlie', 'IT',        55000.00),
(1004, 'Diana',   'HR',        48000.00),
(1005, 'Ethan',   'HR',        52000.00),
(1006, 'Fiona',   'Sales',     60000.00),
(1007, 'George',  'Sales',     45000.00),
(1008, 'Hannah',  'Marketing', 58000.00),
(1009, 'Ian',     'Marketing', 47000.00),
(1010, 'Julia',   'Operations',62000.00);

alter table Employee add Mgr int;




select * from Employee;

alter table employee drop column mgr;

delete from Employee where EmpID=1; -- deleting a row 

update Employee set mgr =1001 where EmpID=1
update Employee set mgr =1002 where EmpID=1001;
update Employee set mgr =1003 where EmpID=1002;
update Employee set mgr =1004 where EmpID=1003;
update Employee set mgr =1005 where EmpID=1004;
update Employee set mgr =1006 where EmpID=1005;
update Employee set mgr =1007 where EmpID=1006;
update Employee set mgr =1008 where EmpID=1007;
update Employee set mgr =1009 where EmpID=1008;
update Employee set mgr =1010 where EmpID=1009;


--self join INNER JOIN (self-join to show employee → manager)

/*Use when you want rows that have a matching partner in the other table. 
With a self-join you treat the same table as two separate roles.*/


SELECT 
    e.Name AS Employee,
    m.Name AS Manager
FROM 
    Employee e
JOIN 
    Employee m 
ON 
    e.Mgr = m.EmpID;


SELECT e.EmpID, e.Name AS Employee, m.Name AS Manager
FROM Employee e
LEFT JOIN Employee m
  ON e.Mgr = m.EmpID;

  --left join 
  --Most common: give me all employees and manager info if available.

  select e.empID , e.Name as employee , m.Name as Mgr
  from Employee e
  left join Employee m 
  on e.Mgr = m.EmpID;


  /* A function in SQL Server is a user-defined routine that takes input parameters,
  performs a calculation or operation, and returns a single value or a table.
Unlike stored procedures, functions must return something — 
they can’t just “do stuff” like update a table (that’s the job of stored procedures).*/

-- scalar function 
create or alter function employeeinsertion (@EmpID int , @Name varchar)
returns varchar (20)

as begin 
          insert into emp (EmpID, Name) values (@EmpID ,  @Name)
          return @EmpId + '-' + @Name

end

select * from Employee

-- avg salary fucntion 

create or alter function Avgsal()
returns table 
as 
return (
   select Dept , avg(Salary)  as avgsal from Employee group by Dept);


   /*You use triggers when you want the database to enforce rules or take actions automatically 
   without depending on the application layer.
Common use cases:

Automatically log changes to a history/audit table.

Validate data before saving it.

Maintain referential integrity (like cascading deletes).

Prevent certain operations (like stopping a delete).*/
  
  CREATE TABLE AuditLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    EmpID INT,
    ActionType VARCHAR(10),
    ActionDate DATETIME
);



