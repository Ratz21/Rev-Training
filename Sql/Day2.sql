/*CREATE DATABASE RevDB;*/

USE RevDB;

CREATE TABLE Student(StudId VARCHAR(10) , Name CHAR(20), City CHAR(10), Pin INT);

INSERT INTO Student(StudId,Name,City,Pin)
VALUES
('1','Raj','Pune',412101),
('2','Raman','Shinde',22190);


 -- used when we know the ordr of the column DBO(Database Owner Schema)

 insert into dbo.Student VALUES ('3','Ashish','Odisha', 34210);

  Select * FROM Student;

  -- Update the student Address
  update Student Set City ='Mumbai' Where StudId=1;


  --Delete -> it delete the single row 
  -- Truncate Delete all data without removing table structure means columns & rows will still remain.
  -- buffer is temporary storage 

