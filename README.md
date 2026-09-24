# Placement Portal Application - V1

## 1. Project Overview

**Placement Portal Application (PPA) V1** is a web-based placement management system designed to simplify the campus recruitment process for an institute.

The application provides a common platform for:

* **Admin (Institute Placement Cell)**

* **Companies / Recruiters**

* **Students**

The system manages company registrations, placement drives, student applications, application status, and placement history.

It replaces manual processes such as spreadsheets, emails, and offline coordination with a centralized digital platform.

---

## 2. Objectives

The main objectives of the application are:

* Provide role-based access to Admin, Companies, and Students.

* Allow companies to register and create placement drives.

* Allow Admin to approve/reject companies and placement drives.

* Allow students to search and apply for placement drives.

* Track applications and recruitment status.

* Maintain complete placement history.

* Prevent duplicate applications for the same placement drive.

---

## 3. Technology Stack

| Technology                | Purpose                               |
| ------------------------- | ------------------------------------- |
| **Flask**                 | Backend web framework                 |
| **Jinja2**                | Server-side HTML templating           |
| **HTML**                  | Frontend structure                    |
| **CSS**                   | Styling                               |
| **Bootstrap**             | User interface                        |
| **SQLite**                | Database                              |
| **Flask-SQLAlchemy**      | ORM and database operations           |
| **Flask Session**         | Authentication and session management |
| **Lexend (Google Fonts)** | UI typography / font                  |

The database is created programmatically using SQLAlchemy model definitions. No manual database creation is required.

---

# 4. User Roles

The application has three main roles.

## 4.1 Admin

The Admin represents the institute placement cell.

There is only **one Admin**, and Admin registration is not allowed.

Admin can:

* View dashboard statistics.

* Approve or reject company registrations.

* Approve or reject placement drives.

* View all students.

* View all companies.

* View all placement drives.

* View student applications.

* Search students and companies.

* Blacklist students and companies.

* Delete students, companies, and placement drives.

### Admin Dashboard

The dashboard displays:

* Total Students

* Total Companies

* Total Placement Drives

* Total Applications

* Pending Company Registrations

* Pending Placement Drives

---

# 5. Company / Recruiter Functionalities

Companies can register themselves on the platform.

After registration, the company profile remains **Pending** until it is approved by the Admin.

### Company Features

* Register company profile.

* Login after approval.

* View company profile.

* Edit company profile.

* Create placement drives.

* View created placement drives.

* Edit placement drives.

* Delete eligible placement drives.

* Close ongoing placement drives.

* View student applications.

* Update application status.

### Company Approval Flow

```text
Company Registration

        ↓

Pending Approval

        ↓

Admin Review

      ↙   ↘

Approved   Rejected

    ↓

Create Placement Drives
```

---

# 6. Student Functionalities

Students can register themselves and create their profiles.

### Student Features

* Register and login.

* Create/update student profile.

* Add academic details.

* Add LinkedIn profile.

* View available placement drives.

* Search placement drives.

* Apply for placement drives.

* View application status.

* View application history.

### Student Application Flow

```text
View Available Drive

        ↓

      Apply

        ↓

      Applied

        ↓

Shortlisted / Rejected

        ↓

Accepted / Rejected
```

---

# 7. Placement Drive

A **Placement Drive** represents a recruitment opportunity created by a company.

A placement drive contains information such as:

* Drive ID

* Company ID

* Drive Name

* Job Title

* Job Description

* Eligibility Criteria

* Application Deadline

* Salary / CTC

* Status

### Drive Status

```text
Pending

   ↓

Ongoing

   ↓

Closed
```

A drive can also be rejected by the Admin.

---

# 8. Application Management

An **Application** represents a student's application to a placement drive.

Each application contains information such as:

* Application ID

* Student ID

* Drive ID

* Resume

* Application Date

* Position

* CGPA

* Passing Year

* Application Status

### Application Status

```text
Applied

   ↓

Shortlisted

   ↓

Accepted
```

An application can also be marked as **Rejected** during the recruitment process.

### Duplicate Application Prevention

A student cannot apply multiple times to the same placement drive.

This is enforced using a unique combination of:

```text
Student ID + Drive ID
```

---

# 9. Authentication and Authorization

The application uses **Flask Session** for authentication and maintaining login sessions.

After successful login:

```text
Login

  ↓

Credentials Verification

  ↓

Session Created

  ↓

Role-Based Access

  ↓

User Dashboard
```

Separate sessions are maintained for Admin, Company, and Student users.

Role-based access ensures that users can access only the functionality permitted for their role.

---

# 10. Database Design

The application uses **SQLite** as the database.

The database is created programmatically using SQLAlchemy models.

The main entities are:

```text
Student
   │
   └── Application
             │
             └── Placement Drive
                       │
                       └── Company
```

### Main Tables

#### Student

Stores student profile and academic information.

#### Recruiter

Stores company profile and approval status.

#### Drive

Stores placement drive information.

#### Application

Stores student applications and recruitment status.

---

# 11. Project Structure

```text
PlacementPortalV1/
│
├── app.py
├── models.py
├── requirements.txt
│
├── static/
│   └── ...
│
├── templates/
│   ├── hero.html
│   ├── login.html
│   ├── student_signup.html
│   ├── company_signup.html
│   ├── admin_dashboard.html
│   ├── studenthome.html
│   ├── companyhome.html
│   └── ...
│
└── instance/
    └── users.db
     
```

---

# 12. Installation and Setup

## Prerequisites

Install the following:

* Python 3.x

* Git

## Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 13. Run the Application

Run the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:8000
```

> Make sure the virtual environment is activated before installing dependencies and running the application.

---

# 14. Admin Account

Admin registration is not available through the application.

The application contains a pre-existing Admin account.

```text
Email: shikhar@admin
Password: admin@1234
```

The Admin can manage companies, students, placement drives, and applications.

---

# 15. Key Features Summary

### Admin

* Dashboard

* Company approval/rejection

* Placement drive approval/rejection

* Student management

* Company management

* Application management

* Search

* Blacklist/deactivation

### Company

* Registration

* Company profile

* Placement drive creation

* Placement drive management

* Applicant management

* Application status updates

* Drive closure

* Search

### Student

* Registration/login

* Profile management

* Placement drive search

* Drive application

* Duplicate application prevention

* Application tracking

* Placement history

* Search

### System

* Role-based authentication

* SQLite database

* Programmatic database creation

* Server-side rendering using Jinja2

* Session-based access control

---

# 16. Conclusion

The **Placement Portal Application  V2** provides a centralized platform for managing the complete campus placement process.

It connects the institute, recruiters, and students through role-based workflows while reducing manual coordination and improving placement application tracking.

The application uses **Flask, Jinja2, HTML, CSS, Bootstrap, SQLite, and Flask-SQLAlchemy** to provide a lightweight web-based placement management system.