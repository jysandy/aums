drop table if exists class;
create table class(
	classid number(3) primary key,
	branch varchar(3),
	semester number(1),
	section varchar(1)
	);

drop table if exists student;
create table student(
	rno varchar(20) primary key,
	name varchar(100),
	classid number(3) references class,
	password varchar(100)
	);

drop table if exists course;
create table course(
	courseno varchar(10) primary key,
	coursename varchar(100)
	);

drop table if exists teacher;
create table teacher(
	teacherid varchar(20),
	name varchar(100),
	password varchar(100)
	);

#This combines the 'teaches' and 'att_total' tables
drop table if exists attendance_course;
create table attendance_course(
	aid number(5) primary key,
	teacherid varchar(20) references teacher,
	classid number(3) references class,
	courseno varchar(10) references course,
	total number(5)
	);

drop table if exists att_student;
create table att_student(
	aid number(5) references attendance_course,
	rno varchar(20) references student,
	attended number(5)
	);

#For a given roll number, get attended classes and total classes for each course.
create view simple_attendance as 
	select student.rno, course.coursename, att_student.attended, attendance_course.total
	from student inner join attendance_course
	on student.classid=attendance_course.classid
	inner join course
	on attendance_course.courseno=course.courseno

