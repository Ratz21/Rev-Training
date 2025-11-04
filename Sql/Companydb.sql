CREATE DATABASE CompanyDB;


use CompanyDB;

create table dept(
deptno smallint,
dname varchar(20) not null,
constraint pk_deptno primary key(deptno)
);

create table emp(empno smallint ,
ename varchar(30) not null ,
mgr smallint,
sal numeric(10,2),
comm numeric(7,2),
deptno smallint,
constraint pk_empno primary key(empno),
constraint fk_deptno foreign key(deptno) references dept(deptno)
)

insert into dept values(10,'IT')
insert into dept values(20,'HR')
insert into dept values(30,'SAL')
insert into dept values(40,'MKt')
insert into dept values(50,'OPS')

-- valid inserts (deptno 20 and 30 exist)
INSERT INTO emp (empno, ename, mgr, sal, comm, deptno) VALUES
(1001, 'Alice', NULL, 60000.00, NULL, 10),  -- HR
(1002, 'Bob', 1001, 75000.00, NULL, 20),    -- IT
(1003, 'Charlie', 1002, 50000.00, 500.00, 30), -- Sales
(1004, 'Diana', 1003, 52000.00, 300.00, 30),   -- Sales
(1005, 'Ethan', 1002, 58000.00, NULL, 40),  -- Finance
(1006, 'Fiona', 1005, 62000.00, NULL, 50);  -- Marketing


select * from dept;
select * from emp;

-- it will select only ename and eno fetch data in that column
select empno as 'emp_id', ename as "name" from emp; 

-- it will retrival salary greater than 50000 in desc order
--aggregate functions 
select empno,ename,sal from emp 
where sal>50000
order by sal desc;



--find total salary
select count(empno) as 'No of Emp' , sum(sal) as 'Total', avg (comm) as 'Avg comm' , min(sal) as 'Least sal' , max(sal) as 'Top earner'
from emp 

select empno as 'EmpNum' , ename as 'Name', sal as 'Salary'
from emp 
group by deptno , empno , sal

select deptno as 'Department', sum(sal) as 'total salary'
from emp 
group by deptno

select ename as 'Name', sum(sal) as 'Individual salary ' -- we need to take the columns correctly 
from emp 
group by ename -- we need to mention the column name from which we want to group by from here 


select deptno as 'Department' , sum(sal) as 'total salary'
from emp 
group by deptno 
having sum(sal) > 75000
order by sum(sal) 


INSERT INTO emp (empno, ename, mgr, sal, comm, deptno) VALUES
(1011, 'Jesse', NULL, 60000.00, NULL, 11),  -- HR
(1012, 'Shratz', 1025, 75000.00, NULL, 22),    -- IT
(1013, 'Charlie', 1009, 50000.00, 500.00, null), -- Sales
(1014, 'Raj', 1019, 52000.00, 400.00, null)   -- Sales


--JOINS SUB QUERIES 

insert into dept values(60,'QC')
insert into dept values(50, 'QC')
select e.ename , d.dname 
from emp e inner join dept d 
on d.deptno = e.deptno;





