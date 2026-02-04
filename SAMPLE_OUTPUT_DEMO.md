# Exam Seating Arrangement System - Sample Output

## Application Status
✅ **Flask Server Running**: http://127.0.0.1:5000
✅ **Debug Mode**: ON
✅ **Debugger PIN**: 405-468-285

---

## System Overview

### User Roles & Login

**ADMIN Dashboard**: `http://127.0.0.1:5000/admin/login`
- Username: `admin` (or your configured admin user)
- Access: Upload students, upload timetable, select classes, generate seating

**TEACHER Dashboard**: `http://127.0.0.1:5000/teacher/login`
- Username: `teacher_eab415` (example)
- Access: View seating arrangements for assigned hall, export CSV, navigate exam dates

**STUDENT Login**: `http://127.0.0.1:5000/student/login`
- Roll Number: `11913001` (example)
- Access: View seat assignment, classroom, subject for exams

---

## 1. Teacher Dashboard - Main Display

### Page Header
```
                    EXAM SEATING ARRANGEMENT
                         Teacher Dashboard

Assigned Hall: EAB 415          [Logout]
```

### Date Navigation Section
```
┌─────────────────────────────────────────────────────┐
│ Select Date: [25-02-2023 ▼] [← Prev]  [Next →]     │
│ [Export CSV] ↓                                       │
│                                                       │
│ Subjects for this date:                             │
│ • Electromagnetic Theory (11:00 AM - 1:00 PM)      │
│ • Renewable Energy Sources (2:00 PM - 4:00 PM)     │
└─────────────────────────────────────────────────────┘
```

### Classroom Seating Table (Professional Layout)

#### Example Date: 24-04-2023
```
╔═══════╦════════╦════════╦════════╦════════╦════════╗
║ ROW   ║   A    ║   B    ║   C    ║   D    ║   E    ║
║       ║ L │ R  ║ L │ R  ║ L │ R  ║ L │ R  ║ L │ R  ║
╠═══════╬═════════╬═════════╬═════════╬═════════╬═════════╣
║  1    ║AL1│AR1 ║BL1│BR1 ║ -- │ -- ║ -- │ -- ║ -- │ -- ║
║       ║001│002 ║003│004 ║    │    ║    │    ║    │    ║
╠═══════╬═════════╬═════════╬═════════╬═════════╬═════════╣
║  2    ║AL2│AR2 ║BL2│BR2 ║ -- │ -- ║ -- │ -- ║ -- │ -- ║
║       ║005│006 ║007│008 ║    │    ║    │    ║    │    ║
╠═══════╬═════════╬═════════╬═════════╬═════════╬═════════╣
║  3    ║ -- │ -- ║ -- │ -- ║ -- │ -- ║ -- │ -- ║ -- │ -- ║
║       ║    │    ║    │    ║    │    ║    │    ║    │    ║
╚═══════╩═════════╩═════════╩═════════╩═════════╩═════════╝

Legend:
  🔵 Blue cells = Left seats (L)
  🟡 Yellow cells = Right seats (R)
  -- = Empty seat
```

**Seat Format**: `COLUMN + SIDE + BENCH_NUMBER`
- Example: `AL1` = Column A, Left side, Bench 1
- Example: `BR2` = Column B, Right side, Bench 2

---

## 2. Detailed Student List (Below Seating Table)

```
╔═══════════╦═════════════╦═════════════════════════╦════════════════════════════╗
║ Seat ID   ║  Roll No    ║ Name                    ║ Subject                    ║
╠═══════════╬═════════════╬═════════════════════════╬════════════════════════════╣
║ AL1       ║ 11913001    ║ ASWIN VM                ║ Electromagnetic Theory     ║
║ AR1       ║ 11913002    ║ AVARNYA SABU            ║ Electromagnetic Theory     ║
║ BL1       ║ 12118001    ║ ADEEB BABU              ║ Robot Programming          ║
║ BR1       ║ 12118002    ║ ADITHYA DINESH RAO      ║ Robot Programming          ║
║ BL2       ║ 12118003    ║ ALAN GEORGE SHIBU       ║ Robot Programming          ║
║ BR2       ║ 12118004    ║ ANN MARY SHAJI          ║ Robot Programming          ║
╚═══════════╩═════════════╩═════════════════════════╩════════════════════════════╝
```

---

## 3. Sample Seating Data Structure (MongoDB)

### Student Document After Seating Generation

```json
{
  "_id": ObjectId("..."),
  "rollnum": 11913001,
  "name": "ASWIN VM",
  "Year": "FourthYear",
  "branch": "Electrical and Electronics Engineering",
  "seatnum": [
    {
      "date": "24-04-2023",
      "seatnum": "AL1",
      "seat_label": "AL",
      "bench_number": 1,
      "column_letter": "A",
      "side": "Left",
      "classroom": "EAB 415",
      "subject": "Electromagnetic Theory"
    },
    {
      "date": "25-02-2023",
      "seatnum": "AR2",
      "seat_label": "AR",
      "bench_number": 2,
      "column_letter": "A",
      "side": "Right",
      "classroom": "EAB 415",
      "subject": "Renewable Energy Sources"
    }
  ]
}
```

### Teacher Document

```json
{
  "_id": ObjectId("..."),
  "username": "teacher_eab415",
  "password": "demo123",
  "name": "Dr. John Smith",
  "invigilation_hall": "EAB 415"
}
```

---

## 4. CSV Export Format

**Filename**: `EAB_415_seating_24-04-2023.csv`

```csv
SeatID,RollNo,Name,Year,Subject,Column,Bench,Side,Classroom,Date
AL1,11913001,ASWIN VM,FourthYear,Electromagnetic Theory,A,1,Left,EAB 415,24-04-2023
AR1,11913002,AVARNYA SABU,FourthYear,Electromagnetic Theory,A,1,Right,EAB 415,24-04-2023
BL1,12118001,ADEEB BABU,SecondYear,Robot Programming,B,1,Left,EAB 415,24-04-2023
BR1,12118002,ADITHYA DINESH RAO,SecondYear,Robot Programming,B,1,Right,EAB 415,24-04-2023
BL2,12118003,ALAN GEORGE SHIBU,SecondYear,Robot Programming,B,2,Left,EAB 415,24-04-2023
BR2,12118004,ANN MARY SHAJI,SecondYear,Robot Programming,B,2,Right,EAB 415,24-04-2023
```

---

## 5. Student Login - Single Date View

### Page Display

```
                    EXAM SEATING DETAILS
                      Student Dashboard

╔════════════════════════════════════════╗
║  Your Exam Seat Assignment             ║
╠════════════════════════════════════════╣
║ Name:           ASWIN VM               ║
║ Roll Number:    11913001               ║
║ Year:           FourthYear             ║
║                                        ║
║ Date:           24-04-2023             ║
║ Subject:        Electromagnetic Theory ║
║ Classroom:      EAB 415                ║
║ Seat ID:        AL1                    ║
║ Position:       Column A, Bench 1      ║
║ Side:           Left                   ║
║                                        ║
║ Other Dates:    [25-02-2023 ▼]         ║
╚════════════════════════════════════════╝
```

### Seating Map (Showing Current Seat)

```
        CLASSROOM LAYOUT - EAB 415
    (Student's seat highlighted)

╔════════════════════════════════════╗
║  ENTRANCE                          ║
╠════════════════════════════════════╣
║  [✓ AL1] [AR1]  [BL1] [BR1]       ║
║   001    002     003    004        ║
║  [AL2] [AR2]  [BL2] [BR2]         ║
║   005    006     007    008        ║
╚════════════════════════════════════╝

✓ = Your seat (AL1)
```

---

## 6. API Endpoints

### 1. Teacher Dashboard
**URL**: `http://127.0.0.1:5000/teacher/dashboard`
**Method**: GET/POST (with date selection)
**Response**: HTML with seating table

### 2. Debug JSON Endpoint
**URL**: `http://127.0.0.1:5000/teacher/hall_debug?date=24-04-2023`
**Method**: GET
**Response**: JSON of processed students with seat details

**Sample Response**:
```json
{
  "hall": "EAB 415",
  "date": "24-04-2023",
  "students": [
    {
      "rollnum": 11913001,
      "name": "ASWIN VM",
      "year": "FourthYear",
      "seatnum": "AL1",
      "bench_number": 1,
      "column_letter": "A",
      "side": "Left",
      "subject": "Electromagnetic Theory"
    }
  ],
  "total_students": 6,
  "available_dates": ["24-04-2023", "25-02-2023"]
}
```

### 3. CSV Export Endpoint
**URL**: `http://127.0.0.1:5000/teacher/export_csv?date=24-04-2023`
**Method**: GET
**Response**: CSV file download (application/csv)

---

## 7. Admin Workflow

### Step 1: Upload Student Data
```
Form: Admin Dashboard → Upload Students
Input: CSV file with columns:
  - Roll Number
  - Name
  - Year
  - Branch/Department
Result: Students stored in MongoDB
```

### Step 2: Upload Timetable
```
Form: Admin Dashboard → Upload Timetable
Input: CSV/Excel with:
  - Date (DD-MM-YYYY)
  - Time
  - Subject
  - Branch/Year
Result: Exam schedule stored in MongoDB
```

### Step 3: Select Classes & Generate Seating
```
Form: Admin Dashboard → Select Class/Hall
Input: Choose:
  - Hall/Classroom
  - Date
  - Year/Branch
Result: Seating arrangement generated with:
  - Bench numbers (1, 2, 3, ...)
  - Seat sides (Left, Right)
  - Seat positions (AL1, AR1, BL1, BR1, etc.)
  - Written to student.seatnum array in MongoDB
```

---

## 8. Seating Algorithm

### Bench & Side Calculation

For each student in a section, the system calculates:

```
Position in section: 1, 2, 3, 4, 5, 6, ...

Bench Number = ((Position - 1) ÷ 2) + 1
- Position 1 → Bench 1
- Position 2 → Bench 1
- Position 3 → Bench 2
- Position 4 → Bench 2
- Position 5 → Bench 3
- Position 6 → Bench 3

Side = "Left" if Position is ODD else "Right"
- Position 1 → Left (AL)
- Position 2 → Right (AR)
- Position 3 → Left (BL)
- Position 4 → Right (BR)

Seat ID = Column + Side + Bench
- Example: AL1, AR1, BL2, BR2
```

### Hall Layout Columns

```
Standard 5-Column Layout:
Column A (2 seats per bench) | Column B | Column C | Column D | Column E

Each column has:
- Left side (L)
- Right side (R)

Example: AL1 = Column A, Left, Bench 1
         AR1 = Column A, Right, Bench 1
         BL1 = Column B, Left, Bench 1
         BR1 = Column B, Right, Bench 1
```

---

## 9. Key Features Implemented

✅ **Professional Table Layout**
- Rows (benches) numbered 1 to max
- Columns A to E with Left/Right seat pairs
- Color-coded cells (blue for left, yellow for right)
- Matches real-world classroom seating

✅ **Single Date Display**
- Shows only ONE exam date at a time
- Dropdown selector to switch dates
- Prev/Next navigation buttons

✅ **Date Management**
- Extracts available exam dates from student data
- Calculates next/previous dates
- Handles invalid date navigation

✅ **CSV Export**
- Exports current hall's seating for selected date
- Columns: SeatID, RollNo, Name, Year, Subject, Column, Bench, Side, Classroom, Date
- Filename includes hall name and date

✅ **Debug JSON Endpoint**
- Returns structured data for verification
- Shows calculated seat positions, benches, sides
- Useful for troubleshooting seating algorithm

✅ **Student Single-Date View**
- Student login shows earliest exam date
- Can select other dates from dropdown
- Displays seat position in readable format

---

## 10. Testing the System

### Test Admin Flow
```
1. Open http://127.0.0.1:5000/admin/login
2. Login with admin credentials
3. Upload test students (Student Data/ folder has sample files)
4. Upload test timetable (Student Timetable/ folder)
5. Go to /class and /seating to generate arrangement
6. Check MongoDB for student.seatnum entries
```

### Test Teacher Flow
```
1. Open http://127.0.0.1:5000/teacher/login
2. Login with teacher_eab415 / password
3. View seating table for assigned hall
4. Switch dates using dropdown/navigation
5. Click "Export CSV" to download arrangement
6. Test /teacher/hall_debug endpoint
```

### Test Student Flow
```
1. Open http://127.0.0.1:5000/student/login
2. Enter roll number (e.g., 11913001)
3. View earliest exam date by default
4. Use date selector to switch exam dates
5. Verify seat information displays correctly
```

---

## 11. Database Structure

### Collections

**students**
```
- rollnum (number)
- name (string)
- Year (string)
- branch (string)
- seatnum (array)
  - date (string, DD-MM-YYYY)
  - seatnum (string, e.g., "AL1")
  - seat_label (string, e.g., "AL")
  - bench_number (number)
  - column_letter (string, A-E)
  - side (string, "Left" or "Right")
  - classroom (string)
  - subject (string)
```

**teachers**
```
- username (string, unique)
- password (string)
- name (string)
- invigilation_hall (string)
```

**timetables**
```
- date (string, DD-MM-YYYY)
- time (string)
- subject (string)
- year (string)
- classroom (string)
```

---

## Summary

The Exam Seating Arrangement System now displays:

✅ Professional classroom seating tables (rows × columns)
✅ Seat IDs matching physical classroom positions (AL1, AR1, BL1, BR1, etc.)
✅ Single date display with navigation
✅ Detailed student information tables
✅ CSV export functionality
✅ Debug JSON endpoints for troubleshooting
✅ Works for admin, teacher, and student users

**Application is live and ready for testing!**
- **URL**: http://127.0.0.1:5000
- **Status**: Running
- **Debug Mode**: ON (PIN: 405-468-285)
