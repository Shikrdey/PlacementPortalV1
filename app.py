from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, students, recruiters, drives, applications
from datetime import datetime


app = Flask(__name__,static_folder="static")

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
app.config["SECRET_KEY"]="MAD1"
db.init_app(app)



@app.route("/")
def hero():
    return render_template("hero.html")

@app.route("/profile", methods=["POST","GET"])
def profile():
    if request.method=="POST":
        if request.form.get("designation")=="student":
            return redirect(url_for("student_signup"))
        else:
            return redirect(url_for("company_signup"))

    return render_template("profile.html")


@app.route("/student_signup", methods=["POST","GET"])
def student_signup():
    if request.method=="POST":
        data=request.form
        name=data.get("name").strip()
        dob=datetime.strptime(data.get("dob"), "%Y-%m-%d").date()
        gender=data.get("gender")
        linkedin=data.get("linkedin").strip()
        department=data.get("department")
        degree=data.get("degree")
        email=data.get("email").strip()
        password=data.get("password").strip()
        if name=="" or linkedin=="" or email=="" or password=="":
            flash("Kindly enter valid data.","warning")
            return redirect(url_for("student_signup"))
        check=students.query.filter_by(email=email).first()
        if not check:
            student_detail=students(name=name, dob=dob, gender=gender, linkedin=linkedin, department=department, degree=degree, email=email, password=password)
            db.session.add(student_detail)
            db.session.commit()
            student=students.query.filter_by(email=email).first()
            session["student_id"]=student.id
            session["student_email"]=student.email
            flash("Student registered successfully","success")
            return redirect(url_for("studenthome"))
        else:
            flash("Student already exist. Please login","info")
            return redirect(url_for("login"))
    return render_template("student_signup.html")


@app.route("/company_signup",  methods=["POST","GET"])
def company_signup():
    if request.method=="POST":
        data=request.form
        company=data.get("company").strip()
        location=data.get("location").strip()
        hrcontact=data.get("hrcontact").strip()
        website=data.get("website").strip()
        companytype=data.get("companytype")
        ps=data.get("ps")
        email=data.get("email").strip()
        password=data.get("password").strip()
        if company=="" or location=="" or hrcontact=="" or website=="" or email=="" or password=="":
            flash("Kindly enter valid data.","warning")
            return redirect(url_for("company_signup"))
        check=recruiters.query.filter_by(email=email).first()
        check_contact=recruiters.query.filter_by(hrcontact=hrcontact).first()
        check_website=recruiters.query.filter_by(website=website).first()
        check_company=recruiters.query.filter_by(company=company).first()
        if not check:
            company_details=recruiters(company=company, location=location, hrcontact=hrcontact, website=website, companytype=companytype, ps=ps, email=email, password=password)
            db.session.add(company_details)
            db.session.commit()
            flash("Company registered successfully. Waiting for admin approval","success")
            return redirect(url_for("hero"))
        elif check_company:
            flash("Company name already exist. Enter unique company","info")
            return redirect(url_for("company_signup"))
        elif check_contact:
            flash("HR contact already exist. Enter unique HR Contact","info")
            return redirect(url_for("company_signup"))
        elif check_website:
            flash("Company website already exist. Enter unique website","info")
            return redirect(url_for("company_signup"))
        else:
            flash("Company already exist. Please login","info")
            return redirect(url_for("login"))
    return render_template("company_signup.html")



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        admin_email, admin_password="shikhar@admin", "admin@1234"
        if request.form.get("designation")=="admin":
            if admin_email==request.form.get("email") and admin_password==request.form.get("password"):
                session["admin_email"]=admin_email
                flash("Admin login successfull","success")
                return redirect(url_for("admindashboard"))
            else:
                flash("Invalid email or password","danger")           
        elif request.form.get("designation")=="student":
            email=request.form.get("email").strip()
            password=request.form.get("password").strip()
            student= students.query.filter_by(email=email).first()
            if student and student.password==password and student.status=="Approved":
                session["student_id"]=student.id
                session["student_email"]=student.email
                flash("Login successful","success")
                return redirect(url_for("studenthome"))
            elif student and student.password==password and student.status=="Blacklisted":
                flash("Your account has been blacklisted by the admin","danger")
                return redirect(url_for("hero"))
            elif student and student.password!=password:
                flash("Incorrect password","danger")
                return redirect(url_for("login"))
            else:
                flash("Student does not exist. Please register first","info")
                return redirect(url_for("student_signup"))
        else:
            email=request.form.get("email").strip()
            password=request.form.get("password") 
            company=recruiters.query.filter_by(email=email).first()
            if company and company.password==password and company.status=="Approved":
                session["company_id"]=company.id
                session["company_email"]=company.email
                flash("Login successful","success")
                return redirect(url_for("companyhome"))
            elif company and company.password==password and company.status=="Pending":
                session["company_id"]=company.id
                session["company_email"]=company.email
                flash("Waiting for admin approval","info")
                return redirect(url_for("hero")) 
            elif company and company.password==password and company.status=="Blacklisted":
                flash("Your account has been blocked by admin","danger")
                return redirect(url_for("hero"))
            elif company and company.password!=password:
                flash("Incorrect password","danger")
                return redirect(url_for("login"))
            else:
                flash("Company does not exist. Please register first","info")
                return redirect(url_for("company_signup"))     
    return render_template("login.html")









@app.route("/admindashboard")
def admindashboard():
    if "admin_email" in session:
        company= recruiters.query.filter(recruiters.status !="Pending").all()
        pending_company= recruiters.query.filter_by(status="Pending").all()
        pending_drive= drives.query.filter_by(status="Pending").all()
        student= students.query.count()
        drive= drives.query.filter(drives.status.in_(["Ongoing", "Closed", "Rejected"])).count()
        application=applications.query.count()
        return render_template("admin_dashboard.html", company=company, student=student, drive=drive, application=application, pending_company=pending_company, pending_drive=pending_drive)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))
    
@app.route("/admin/search", methods=["POST", "GET"])
def admin_search():
    if "admin_email" in session:
        if request.method=="POST":
            query=request.form.get("query").strip()
            if query !="":
                student=students.query.filter(students.name.ilike(f"%{query}%") | students.id.ilike(f"%{query}%") | students.email.ilike(f"%{query}%")).all()
                company=recruiters.query.filter(recruiters.company.ilike(f"%{query}%")).all()
            else:
                return redirect(url_for("admindashboard"))
        return render_template("admin_search.html", student=student, company=company)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))
    

@app.route("/application_list")
def application_list():
    if "admin_email" in session:
        application=applications.query.all()
        student_ids=[a.student_id for a in application]
        drive_ids=[a.drive_id for a in application]
        student=students.query.filter(students.id.in_(student_ids)).all()
        drive=drives.query.filter(drives.id.in_(drive_ids)).all()
        company_ids=[d.company_id for d in drive]
        company=recruiters.query.filter(recruiters.id.in_(company_ids)).all()
        applied_applications=applications.query.filter_by(status="Applied").count()
        shortlisted_applications=applications.query.filter_by(status="Shortlisted").count()
        accepted_applications=applications.query.filter_by(status="Accepted").count()
        rejected_applications=applications.query.filter_by(status="Rejected").count()
        return render_template("application_list.html", application=application, student=student, drive=drive, company=company, applied_applications=applied_applications, shortlisted_applications=shortlisted_applications, accepted_applications=accepted_applications, rejected_applications=rejected_applications)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/admin_view_aplication/<int:application_id>")
def admin_view_application(application_id):
    if "admin_email" in session:
        application=applications.query.filter_by(id=application_id).first()
        student=students.query.filter_by(id=application.student_id).first()
        drive=drives.query.filter_by(id=application.drive_id).first()
        return render_template("admin_view_application.html", application=application, student=student, drive=drive)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/drive_list")
def drive_list():
    if "admin_email" in session: 
        company=recruiters.query.filter(recruiters.status != "Pending").all()
        drive=drives.query.filter(drives.status != "Pending").all()
        ongoing_drives=drives.query.filter_by(status="Ongoing").count()
        closed_drives=drives.query.filter_by(status="Closed").count()
        rejected_drives=drives.query.filter_by(status="Rejected").count()
        return render_template("drive_list.html", company=company, drive=drive, ongoing_drives=ongoing_drives, closed_drives=closed_drives,rejected_drives=rejected_drives)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/drive_approval/<int:drive_id>", methods=["POST", "GET"])
def drive_approval(drive_id):
    if "admin_email" in session:
        drive=drives.query.filter_by(id=drive_id).first()
        company=recruiters.query.filter_by(id=drive.company_id).first()
        if request.method=="POST":
            data=request.form
            drive.status=data.get("status")
            db.session.commit()
            flash("Drive status updated","success")
            return redirect(url_for("admindashboard"))
        return render_template("drive_approval.html", drive=drive, company=company)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/admin/delete/drive/<int:drive_id>", methods=["POST","GET"])
def admin_delete_drive(drive_id):
    if "admin_email" in session:
        drive=drives.query.filter_by(id=drive_id).first()
        if request.method=="POST":
            db.session.delete(drive)
            db.session.commit()
            flash("Drive deleted successfully","success")
            return redirect(url_for("admindashboard"))
        return render_template("admin_confirmation.html", drive=drive, content="drive", back="/drive_list", link=f"/admin/delete/drive/{drive_id}", home="/admindashboard")
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))
    

@app.route("/company_list")
def company_list():
    if "admin_email" in session:
        company=recruiters.query.filter(recruiters.status != "Pending").all()
        approved_company=recruiters.query.filter_by(status="Approved").count()
        blacklist_company=recruiters.query.filter_by(status="Blacklisted").count()
        return render_template("company_list.html", company=company, approved_company=approved_company, blacklist_company=blacklist_company)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/company_approval/<int:company_id>", methods=["POST", "GET"])
def company_approval(company_id):
    if "admin_email" in session:
        company_details=recruiters.query.filter_by(id=company_id).first()
        if request.method=="POST":
            data=request.form
            company_details.status=data.get("status")
            db.session.commit()
            flash("Company status updated","success")
            return redirect(url_for("admindashboard"))
        return render_template("company_approval.html", company_details=company_details)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/admin/delete/company/<int:company_id>", methods=["POST","GET"])
def admin_delete_company(company_id):
    if "admin_email" in session:
        company=recruiters.query.filter_by(id=company_id).first()
        if request.method=="POST":
            db.session.delete(company)
            db.session.commit()
            flash("Recruiter deleted successfully","success")
            return redirect(url_for("admindashboard"))
        return render_template("admin_confirmation.html", company=company, content="recruiter", back="/company_list", link=f"/admin/delete/company/{company_id}", home="/admindashboard")
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/student_list")
def student_list():
    if "admin_email" in session:
        student=students.query.all()
        approved_student=students.query.filter_by(status="Approved").count()
        blacklisted_student=students.query.filter_by(status="Blacklisted").count()
        return render_template("student_list.html", approved_student=approved_student, blacklisted_student=blacklisted_student, student=student)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/student_approval/<int:student_id>", methods=["POST", "GET"])
def student_approval(student_id):
    if "admin_email" in session:
        student=students.query.filter_by(id=student_id).first()
        if request.method=="POST":
            data=request.form
            student.status=data.get("status")
            db.session.commit()
            flash("Student status updated","success")
            return redirect(url_for("student_list"))
        return render_template("student_approval.html", student=student)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/admin/delete/student/<int:student_id>", methods=["POST","GET"])
def admin_delete_student(student_id):
    if "admin_email" in session:
        student=students.query.filter_by(id=student_id).first()
        if request.method=="POST":
            db.session.delete(student)
            db.session.commit()
            flash("Student deleted successfully","success")
            return redirect(url_for("student_list"))
        return render_template("admin_confirmation.html", student=student, content="student", back="/student_list", link=f"/admin/delete/student/{student_id}", home="/admindashboard")
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))







@app.route("/companyhome")
def companyhome():
    if "company_id" in session:
        company=recruiters.query.filter_by(id=session.get("company_id")).first()
        ongoing_drive=drives.query.filter_by(company_id=session.get("company_id"), status="Ongoing").all()
        closed_drive=drives.query.filter_by(company_id=session.get("company_id"), status="Closed").all()
        pending_drive=drives.query.filter_by(company_id=session.get("company_id"), status="Pending").all()
        rejected_drive=drives.query.filter_by(company_id=session.get("company_id"), status="Rejected").all()
        return render_template("companyhome.html", company=company, ongoing_drive=ongoing_drive, closed_drive=closed_drive, pending_drive=pending_drive,rejected_drive=rejected_drive)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/company/search", methods=["POST", "GET"])
def company_search():
    if "company_id" in session:
        if request.method=="POST":
            query=request.form.get("query").strip()
            if query !="":
                drive=drives.query.filter(drives.company_id==session.get("company_id") ,drives.jobtitle.ilike(f"%{query}%") | drives.drivename.ilike(f"%{query}%")).all()
            else:
                return redirect(url_for("companyhome"))
        return render_template("company_search.html", drive=drive, company=recruiters.query.filter_by(id=session.get("company_id")).first())
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/createdrive", methods=["POST", "GET"])
def createdrive():
    if "company_id" in session:
        if request.method=="POST": 
            data=request.form    
            drivename=data.get("drivename").strip()
            jobtitle=data.get("jobtitle").strip()
            description= data.get("description").strip()
            eligibility= data.get("eligibility").strip()
            deadline= datetime.strptime(data.get("deadline"), "%Y-%m-%d").date()
            salary=data.get("salary").strip()
            if drivename=="" or jobtitle=="" or description=="" or eligibility=="" or deadline=="" or salary=="":
                flash("Kindly enter valid data.","warning")
                return redirect(url_for("createdrive"))
            companydrive=drives(drivename=drivename, jobtitle=jobtitle, description=description, eligibility=eligibility, deadline=deadline,salary=salary, company_id=session.get("company_id"))
            db.session.add(companydrive)
            db.session.commit()
            flash("Drive created successfully. Waiting for admin approval","success")
            return redirect(url_for("companyhome"))
        company=recruiters.query.filter_by(id=session.get("company_id")).first()
        return render_template("create_drive.html", company=company)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/drive_details/<int:drive_id>", methods=["POST","GET"])
def drive_details(drive_id):
    if "company_id" in session:
        drive=drives.query.filter_by(id=drive_id, company_id=session.get("company_id")).first()
        if drive:
            if drive.status =="Ongoing" or drive.status=="Closed":
                if request.method=="POST":
                    drive.status=request.form.get("status")
                    db.session.commit()
                    if drive.status=="Closed":
                        flash("Drive closed","success")
                        return redirect(url_for("companyhome"))
                    else:
                        return redirect(url_for("companyhome"))
            else:
                if request.method=="POST":
                    data=request.form
                    drive.status=data.get("status")
                    drive.drivename=data.get("drivename").strip()
                    drive.jobtitle=data.get("jobtitle").strip()
                    drive.description= data.get("description").strip()
                    drive.eligibility= data.get("eligibility").strip()
                    drive.deadline= datetime.strptime(data.get("deadline"), "%Y-%m-%d").date()
                    drive.salary=data.get("salary").strip()
                    if drive.drivename=="" or drive.jobtitle=="" or drive.description=="" or drive.eligibility=="" or drive.salary=="":
                        flash("Kindly enter valid data.","warning")
                        return redirect(url_for("drive_details",drive_id = drive.id))
                    db.session.commit()
                    flash("Drive updated successfully.","success")
                    return redirect(url_for("companyhome"))
            company=recruiters.query.filter_by(id=session.get("company_id")).first()
            application=applications.query.filter_by(drive_id=drive_id).all()
            student=students.query.all()
            return render_template("drive_details.html", drive=drive, company=company, application=application, student=student)
        else:
            flash("Drive does not exist","warning")
            return redirect(url_for("companyhome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/view_application/<int:application_id>", methods=["POST","GET"])
def view_application(application_id):
    if "company_id" in session:
        application_details=applications.query.filter_by(id=application_id).first()
        if application_details:
            companyID=(drives.query.filter_by(id=application_details.drive_id).first()).company_id
            if companyID==session.get("company_id"):
                student=students.query.filter_by(id=application_details.student_id).first()
                if request.method=="POST":
                    data=request.form
                    status=data.get("status")
                    application_details.status=status
                    db.session.commit()
                    return redirect(url_for("drive_details",drive_id=application_details.drive_id))
                company=recruiters.query.filter_by(id=session.get("company_id")).first()
                return render_template("company_view_application.html", company=company, student=student, application_details=application_details)
            else:
                flash("Access denied","warning")
                return redirect(url_for("companyhome"))
        else:
            flash("Action denied","warning")
            return redirect(url_for("companyhome"))

    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/delete/drive/<int:drive_id>", methods=["POST","GET"])
def delete_drive(drive_id):
    if "company_id" in session:
        company=recruiters.query.filter_by(id=session.get("company_id")).first()
        drive=drives.query.filter(drives.id==drive_id, drives.company_id==session.get("company_id"), drives.status.in_(["Pending","Rejected"])).first()
        if drive:
            if request.method=="POST":
                db.session.delete(drive)
                db.session.commit()
                flash("Drive deleted successfully.","success")
                return redirect(url_for("companyhome"))
            return render_template("confirmation.html", drive=drive, company=company)
        else:
            flash("Action denied","warning")
            return redirect(url_for("companyhome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/company_profile/<int:company_id>")
def company_profile(company_id):
    if "company_id" in session:
        if company_id==session.get("company_id"):
            company=recruiters.query.filter_by(id=company_id).first()
            return render_template("company_profile.html", company=company)
        else:
            flash("Access denied","warning")
            return redirect(url_for("companyhome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/edit_company_profile/<int:company_id>", methods=["POST","GET"])
def edit_company_profile(company_id):
    if "company_id" in session:
        if company_id==session.get("company_id"):
            company= recruiters.query.filter_by(id=company_id).first()
            if request.method=="POST":
                data=request.form
                company_company=data.get("company").strip()
                company_location=data.get("location").strip()
                company_hrcontact=data.get("hrcontact").strip()
                company_website=data.get("website").strip()
                company_companytype=data.get("companytype")
                company_ps=data.get("ps")
                company_email=data.get("email").strip()
                company_password=data.get("password").strip()
                check_company=recruiters.query.filter(((recruiters.company==company_company) | (recruiters.hrcontact==company_hrcontact) | (recruiters.website==company_website) | (recruiters.email==company_email)), recruiters.id != session.get("company_id")).first()
                if check_company:
                    flash("Duplicate entry not allowed","warning")
                    return redirect(url_for("edit_company_profile", company_id= session.get("company_id")))
                elif company_company=="" or company_location=="" or company_hrcontact=="" or company_website=="" or company_password=="":
                    flash("Kindly enter valid data.","warning")
                    return redirect(url_for("edit_company_profile", company_id= session.get("company_id")))
                company.company=company_company
                company.location=company_location
                company.hrcontact=company_hrcontact
                company.website=company_website
                company.companytype=company_companytype
                company.ps=company_ps
                company.email=company_email
                company.password=company_password
                db.session.commit()
                flash("Company details updated successfully","success")
                return redirect(url_for("companyhome"))
            return render_template("edit_company_profile.html",company=company)
        else:
            flash("Access denied","warning")
            return redirect(url_for("companyhome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))







@app.route("/studenthome")
def studenthome():
    if "student_id" in session:
        student=students.query.filter_by(id=session.get("student_id")).first()
        company=recruiters.query.all()
        application= applications.query.filter(applications.student_id==session.get("student_id"), applications.status.in_(['Applied','Shortlisted','Accepted','Rejected'])).all()
        drive=[f.drive_id for f in application]
        ongoing_drive=drives.query.filter(drives.status=="Ongoing", ~drives.id.in_(drive)).all()
        return render_template("studenthome.html", student=student, ongoing_drive=ongoing_drive, company=company)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/student/search", methods=["POST","GET"])
def student_search():
    if "student_id" in session:
        if request.method=="POST":
            query=request.form.get("query").strip()
            if query !="":
                company=recruiters.query.all()
                application=applications.query.filter_by(student_id=session.get("student_id")).all()
                drive_id=[a.drive_id for a in application]
                drive=drives.query.filter(~drives.id.in_(drive_id) ,drives.status=="Ongoing", drives.jobtitle.ilike(f"%{query}%")).all()
            else:
                return redirect(url_for("studenthome"))
        return render_template("student_search.html", drive=drive, company=company, student=students.query.filter_by(id=session.get("student_id")).first())
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/drive_apply/<int:drive_id>", methods=["POST","GET"])
def drive_apply(drive_id):
    if "student_id" in session:
        drive=drives.query.filter_by(id=drive_id).first()
        if drive.status=="Ongoing":
            application_check=applications.query.filter_by(drive_id=drive.id, student_id=session.get("student_id")).first()
            if not application_check:
                if request.method=="POST":
                    data=request.form
                    resume=data.get("resume").strip()
                    position=data.get("position").strip()
                    cgpa=data.get("cgpa").strip()
                    year=data.get("year").strip()
                    check= applications.query.filter_by(resume=resume).first()
                    if resume=="" or position=="" or cgpa=="" or year=="":
                        flash("Kindly enter valid data.","warning")
                        return redirect(url_for("drive_apply", drive_id=drive.id))
                    elif check:
                        flash("Resume already exists","warning")
                        return redirect(url_for("drive_apply", drive_id=drive.id))
                    application=applications(resume=resume, position=position, cgpa=cgpa, year=year, drive_id=drive.id, student_id=session.get("student_id"))
                    db.session.add(application)
                    db.session.commit()
                    flash("Application received. Kindly wait while we review it.","success")
                    return redirect(url_for("studenthome"))
            else:
                flash("You have already applied to this drive","warning")
                return redirect(url_for("studenthome"))
        else:
            flash("Action denied","warning")
            return redirect(url_for("studenthome"))
        student=students.query.filter_by(id=session.get("student_id")).first()
        company=recruiters.query.filter_by(id=drive.company_id).first()
        return render_template("drive_apply.html", drive=drive, student=student, company_name=company.company)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))
    

@app.route("/application_history")
def history():
    if "student_id" in session:
        application=applications.query.filter(applications.student_id==session.get("student_id")).all()
        drive_id=[ a.drive_id for a in application ]
        drive= drives.query.filter(drives.id.in_(drive_id))
        company_id= [ d.company_id for d in drive ]
        company= recruiters.query.filter(recruiters.id.in_(company_id))
        student= students.query.filter_by(id=session.get("student_id")).first()
        return render_template("history.html", drive=drive, application=application, company=company, student=student)
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/student_view_application/<int:application_id>", methods=["POST","GET"])
def student_view_application(application_id):
    if "student_id" in session:
        application=applications.query.filter_by(id=application_id).first()
        if application.student_id==session.get("student_id"):
            drive=drives.query.filter_by(id=application.drive_id).first()
            company=recruiters.query.filter_by(id=drive.company_id).first()
            return render_template("student_view_application.html", application=application, drive=drive, company=company, student=students.query.filter_by(id=session.get("student_id")).first())
        else:
            flash("Action denied","warning")
            return redirect(url_for("studenthome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))


@app.route("/student_profile/<int:student_id>")
def student_profile(student_id):
    if "student_id" in session:
        if student_id==session.get("student_id"):
            student=students.query.filter_by(id=student_id).first()
            return render_template("student_profile.html", student=student)
        else:
            flash("Action denied","warning")
            return redirect(url_for("studenthome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))

@app.route("/edit_student_profile/<int:student_id>", methods=["POST","GET"])
def edit_student_profile(student_id):
    if "student_id" in session:
        if student_id==session.get("student_id"):
            student=students.query.filter_by(id=student_id).first()
            if request.method=="POST":
                data=request.form
                student_name=data.get("name").strip()
                student_dob=datetime.strptime(data.get("dob"), "%Y-%m-%d").date()
                student_gender=data.get("gender")
                student_linkedin=data.get("linkedin").strip()
                student_department=data.get("department")
                student_degree=data.get("degree")
                student_email=data.get("email").strip()
                student_password=data.get("password").strip()
                check_student= students.query.filter(((students.linkedin==student_linkedin) | (students.email==student_email)), students.id != session.get("student_id")).first()
                if check_student:
                    flash("Duplicate entry not allowed","warning")
                    return redirect(url_for("edit_student_profile", student_id= session.get("student_id")))
                elif student_name=="" or student_dob=="" or student_linkedin=="" or student_email=="" or student_password=="":
                    flash("Kindly enter valid data.","warning")
                    return redirect(url_for("edit_student_profile", student_id= session.get("student_id")))
                student.name=student_name
                student.dob=student_dob
                student.gender=student_gender
                student.linkedin=student_linkedin
                student.department=student_department
                student.degree=student_degree
                student.email=student_email
                student.password=student_password
                db.session.commit()
                flash("Student details updated successfully","success")
                return redirect(url_for("studenthome"))
            return render_template("edit_student_profile.html", student=student)
        else:
            flash("Action denied","warning")
            return redirect(url_for("studenthome"))
    else:
        flash("Access denied","danger")
        return redirect(url_for("hero"))




@app.route("/logout")
def logout():
    if "student_id" in session:
        session.pop("student_id")
        session.pop("student_email")
        flash("You have been logged out","success")
        return redirect(url_for("hero"))
    elif "company_id" in session:
        session.pop("company_id")
        session.pop("company_email")
        flash("You have been logged out","success")
        return redirect(url_for("hero"))
    elif "admin_email" in session:
        session.pop("admin_email")
        flash("You have been logged out","success")
        return redirect(url_for("hero"))
    else:
        flash("Please login to continue","info")
        return redirect(url_for("hero"))




if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)