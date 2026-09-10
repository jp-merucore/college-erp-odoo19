# College ERP for Odoo 19

A complete College ERP management system developed for Odoo 19.

The module provides college administration functionality including student
management, admissions, departments, courses, subjects, teachers,
attendance, examinations, fees, timetable, notices, dashboards, reports,
and student portal functionality.

---

## 📚 Features

### 🎓 Student Management

- Student registration
- Student profile
- Student personal information
- Student contact information
- Department assignment
- Course assignment
- Student status management
- Student ID card
- Student reports

### 📝 Admission Management

- College admission management
- Admission application tracking
- Student admission workflow
- Admission sequence generation
- Admission status management

### 🏫 Department Management

- Create and manage departments
- Department head management
- Department information
- Department-wise student management
- Department-wise course management

### 📖 Course Management

- Course creation
- Course information
- Department-based courses
- Course duration
- Course management from backend

### 📕 Subject Management

- Subject creation
- Subject code
- Course assignment
- Subject management

### 👨‍🏫 Teacher Management

- Teacher registration
- Teacher profile
- Teacher contact information
- Department assignment
- Teacher management

### 🕐 Timetable Management

- College timetable
- Course-wise timetable
- Subject-wise timetable
- Teacher assignment
- Schedule management

### ✅ Attendance Management

- Student attendance
- Attendance date
- Student-wise attendance
- Attendance status
- Attendance management from backend
- Attendance information available through the student portal

### 📝 Examination Management

- Exam management
- Course-wise examinations
- Subject-wise examinations
- Exam scheduling
- Exam results
- Student result management

### 💰 Fee Management

- Student fee management
- Fee records
- Fee amount
- Payment status
- Student fee information through portal

### 📢 Notice Management

- College notices
- Notice title
- Notice content
- Notice publishing
- Notices available through student portal

### 📊 Dashboard

- College dashboard
- College statistics
- Student information
- Admission information
- Attendance information
- Examination information
- Fee information

### 🌐 Student Portal

Students can access:

- Student dashboard
- Student profile
- Courses
- Attendance
- Fees
- Examination results
- Timetable
- College notices
- Student ID card

### 📄 Reports

- Student report
- Student ID card report

---

# 🧩 Module Structure

```text
college_erp_ready/
│
├── __init__.py
├── __manifest__.py
│
├── controllers/
│   ├── __init__.py
│   ├── college_dashboard.py
│   └── student_portal.py
│
├── data/
│   └── ir_sequence.xml
│
├── models/
│   ├── __init__.py
│   ├── college_admission.py
│   ├── college_attendance.py
│   ├── college_course.py
│   ├── college_department.py
│   ├── college_exam.py
│   ├── college_exam_result.py
│   ├── college_fee.py
│   ├── college_notice.py
│   ├── college_student.py
│   ├── college_subject.py
│   ├── college_teacher.py
│   └── college_timetable.py
│
├── report/
│   ├── report_actions.xml
│   ├── student_id_card.xml
│   └── student_report.xml
│
├── security/
│   └── ir.model.access.csv
│
├── static/
│   ├── description/
│   │   └── icon.png
│   └── src/
│       ├── css/
│       ├── dashboard/
│       └── img/
│
├── tests/
│
├── views/
│   ├── backend/
│   └── portal/
│
└── wizard/
