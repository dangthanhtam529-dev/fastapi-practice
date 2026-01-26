from mimetypes import init
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, table, true

class Student(SQLModel, table=True):
  id : int | None = Field(default=None , primary_key=True)
  name : str
  age : int

class Course(SQLModel, table=True):
  id : int | None = Field(default=None , primary_key=True)
  name : str
  stu_id : int | None = Field(default=None ,foreign_key="student.id")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_student():
    with Session(engine) as session:
        student1 = Student(name = "liming" , age = 18)
        student2 = Student(name = "zhangsan" , age = 19)
        session.add(student1)
        session.add(student2)
        session.commit()
        session.refresh(student1)
        print(student1)
        session.refresh(student2)
        print(student2)

def create_course():
    with Session(engine) as session:
        course1 = Course(name = "math" , stu_id = 1)
        course2 = Course(name = "chinese" , stu_id = 2)
        session.add(course1)
        session.add(course2)
        session.commit()
        session.refresh(course1)
        print(course1)
        session.refresh(course2)
        print(course2)

def select_student_course():
    with Session(engine) as session:
        statement = select(Student, Course).join(Course)
        results = session.exec(statement)
        for stu, cou in results:
            print({"student": stu, "course": cou})



if __name__ == "__main__":
   

    select_student_course()
