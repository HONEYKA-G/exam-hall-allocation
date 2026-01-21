# Teacher Module Setup Instructions

## What Was Added:

✅ **3 Teacher Routes** in app.py:
- `/teacher/login` - Login page
- `/teacher/dashboard` - Dashboard with student list
- `/teacher/student/<roll_num>` - View individual student details
- `/teacher/logout` - Logout functionality

✅ **3 HTML Templates**:
- `teacherlogin.html` - Login form
- `teacherdashboard.html` - Dashboard with statistics and student list
- `teacher_student_details.html` - Individual student details page

✅ **Database Integration**:
- Added `techercollections` to MongoDB connection
- Stores teacher credentials and assigned class/subject

✅ **Home Page Updated**:
- Added "Teachers" button on home page

---

## Setup Steps:

### Step 1: Run Dummy Data Script

```bash
python add_dummy_teachers.py
```

This will insert 3 test teachers:
- **teacher1** / pass123 (Class A - Mathematics)
- **teacher2** / pass456 (Class B - English)
- **teacher3** / pass789 (Class C - Science)

### Step 2: Start Your Flask App

```bash
python app.py
```

### Step 3: Test Teacher Module

1. Go to `http://localhost:5000/`
2. Click **"Go to Teacher Page"** button
3. Login with credentials from Step 1
4. View dashboard with assigned class and students
5. Click "View Details" on any student

---

## Teacher Dashboard Features:

✅ **Statistics Cards**:
- Total Students count
- Assigned Subject
- Assigned Class

✅ **Student List Table**:
- Roll Number
- Student Name
- Class
- Year
- View Details button

✅ **Student Details Page**:
- Roll Number
- Name
- Class
- Year
- Subject (if available)
- Seat Number (if assigned)
- Classroom (if assigned)

---

## Database Schema:

```json
{
  "username": "teacher1",
  "password": "pass123",
  "name": "Mr. John Doe",
  "assigned_class": "Class A",
  "assigned_subject": "Mathematics",
  "email": "john@email.com",
  "phone": "9876543210"
}
```

---

## Session Management:

- `session['teacher_username']` - Stores logged-in teacher username
- `session['teacher_id']` - Stores MongoDB teacher ID

---

## Notes:

- Teachers can only see students from their assigned class
- Teacher passwords are stored in MongoDB (for demo purposes)
- To add more teachers, run the script again with updated data
- Teachers are automatically filtered by `assigned_class` field

---

## Troubleshooting:

**Error: "typo: techercollections not found"**
- Make sure line 36 in app.py has: `techercollections = db.teacher`

**Error: "Template not found"**
- Check that all 3 files are in `templates/` folder:
  - teacherlogin.html
  - teacherdashboard.html
  - teacher_student_details.html

**No students showing in dashboard**
- Make sure students have `sheet_name` field matching teacher's `assigned_class`
- Check MongoDB that student collection has data

---

Done! ✅ Teacher module is ready to use!
