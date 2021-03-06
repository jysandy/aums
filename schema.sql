drop table if exists class;
create table class(
	classid integer primary key,
	branch varchar(3),
	semester integer,
	section varchar(1)
	);

drop table if exists student;
create table student(
	rno varchar(20) primary key,
	name varchar(100),
	classid integer references class,
	password varchar(100)
	);

drop table if exists course;
create table course(
	courseno varchar(10) primary key,
	coursename varchar(100)
	);

drop table if exists teacher;
create table teacher(
	teacherid varchar(20) primary key,
	name varchar(100),
	password varchar(100)
	);

drop table if exists attendance_course;
create table attendance_course(
	aid integer primary key,
	teacherid varchar(20) references teacher,
	classid integer references class,
	courseno varchar(10) references course,
	total integer
	);

drop table if exists att_student;
create table att_student(
	aid integer references attendance_course,
	rno varchar(20) references student,
	attended integer
	);

drop view if exists simple_attendance;
create view simple_attendance as 
	select student.rno, course.coursename, course.courseno, att_student.attended, attendance_course.total
	from student inner join attendance_course
	on student.classid=attendance_course.classid
	inner join course
	on attendance_course.courseno=course.courseno
	inner join att_student
	on attendance_course.aid=att_student.aid
	where student.rno=att_student.rno