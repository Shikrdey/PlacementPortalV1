from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    dob=db.Column(db.Date, nullable=False)
    gender=db.Column(db.String(10), nullable=False)
    linkedin=db.Column(db.String(255), nullable=False, unique=True)
    department=db.Column(db.String(100), nullable=False)
    degree=db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(50),nullable=False, unique=True)
    password=db.Column(db.String,nullable=False)
    status=db.Column(db.String(10), nullable=False, default="Approved") # Approved, Blacklisted
    application=db.relationship("applications", backref="students", lazy=True, cascade="all, delete-orphan")

class recruiters(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    company=db.Column(db.String(150), nullable=False, unique=True)
    location=db.Column(db.String(100), nullable=False)
    hrcontact=db.Column(db.String(20), nullable=False, unique=True)
    website=db.Column(db.String(255), nullable=False, unique=True)
    companytype=db.Column(db.String(50), nullable=False)
    ps=db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(50),nullable=False, unique=True)
    password=db.Column(db.String,nullable=False)
    status=db.Column(db.String(10), nullable=False, default="Pending") # Pending, Approved, Blacklisted
    drive=db.relationship("drives", backref="recruiters", lazy=True, cascade="all, delete-orphan")
   
   
class drives(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    drivename=db.Column(db.String, nullable=False)
    jobtitle=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)
    eligibility=db.Column(db.String, nullable=False)
    deadline=db.Column(db.Date, nullable=False)
    salary=db.Column(db.String, nullable=False)
    status= db.Column(db.String(50), nullable=False, default="Pending") # Pending, Ongoing, Closed, Rejected
    company_id=db.Column(db.Integer, db.ForeignKey("recruiters.id"), nullable=False)
    application=db.relationship("applications", backref="drives", lazy=True, cascade="all, delete-orphan")

class applications(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_added=db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    resume=db.Column(db.String, nullable=False, unique=True)
    position=db.Column(db.String(20), nullable=False)
    cgpa=db.Column(db.String(4), nullable=False)
    year=db.Column(db.String, nullable=False)
    status=db.Column(db.String(20), nullable=False, default="Applied") # Applied, Shortlisted, Accepted, Rejected
    drive_id=db.Column(db.Integer,db.ForeignKey("drives.id"), nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"), nullable=False)

    __table_args__=(db.UniqueConstraint("drive_id","student_id", name="one drive one application"),)