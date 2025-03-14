from typing import Optional
from flask import request, jsonify
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel
from sqlalchemy import select

from api.users.models import Users
from api.users.models import Students
from database import db


users_app = APIBlueprint("users_app", __name__)
students_app = APIBlueprint("students_app", __name__)


class UserSchema(BaseModel):
    id: int
    password: str
    email: str
    created_at: str
    updated_at: str
    last_login: Optional[str]
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[UserSchema]


class StudentSchema(BaseModel):
    id: Optional[int]
    enrollment_date: str
    min_course_credits: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class StudentList(BaseModel):
    students: list[StudentSchema]


@users_app.get("/users", responses={"200": UserList})
def get_users():
    with db.session() as session:
        users_query = session.execute(select(Users)).scalars().all()
        users_list = [
            UserSchema.from_orm(user).dict()
            for user
            in users_query
        ]
        return {"users": users_list}

#### STUDENT
@users_app.post("/student")
def create_student():
    with db.session() as session:
        content = request.json
        stmt = Students(
            first_name=content["first_name"],
            last_name=content["last_name"],
            enrollment_date=content["enrollment_date"],
            min_course_credits=content["min_course_credits"],
            user_id=content["user_id"],
        )
        session.add(stmt)
        session.commit()
        return {"success": True}


@users_app.get("/students", responses={"200": StudentList})
def get_student():
    with db.session() as session:
        student_query = session.execute(select(Students)).scalars().all()
        student_list = [ StudentSchema.from_orm(students).dict() for students in student_query ]
        return {"users": student_list}


@users_app.get("/student/<string:student_id>")
def get_single_student():
    suid = request.view_args.get("student_id")
    with db.session() as session:
        student_query = session.execute(select(Students).where(Students.id == suid)).scalars()
        student_list = [ StudentSchema.from_orm(students).dict() for students in student_query ]
        return {"users": student_list}
