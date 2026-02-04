"""
Sample output demonstration for the Exam Seating Arrangement System
Shows what the teacher dashboard will display with sample data
"""

# Sample student records after seating generation
sample_students = [
    {
        "rollnum": 11913001,
        "name": "ASWIN VM",
        "Year": "FourthYear",
        "seatnum": [
            {
                "date": "24-04-2023",
                "seatnum": "AL1",
                "seat_label": "AL",
                "section": "a",
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
                "section": "a",
                "bench_number": 2,
                "column_letter": "A",
                "side": "Right",
                "classroom": "EAB 415",
                "subject": "Renewable Energy Sources"
            }
        ]
    },
    {
        "rollnum": 11913002,
        "name": "AVARNYA SABU",
        "Year": "FourthYear",
        "seatnum": [
            {
                "date": "24-04-2023",
                "seatnum": "AR1",
                "seat_label": "AR",
                "section": "a",
                "bench_number": 1,
                "column_letter": "A",
                "side": "Right",
                "classroom": "EAB 415",
                "subject": "Electromagnetic Theory"
            }
        ]
    },
    {
        "rollnum": 12118001,
        "name": "ADEEB BABU",
        "Year": "SecondYear",
        "seatnum": [
            {
                "date": "24-04-2023",
                "seatnum": "BL1",
                "seat_label": "BL",
                "section": "b",
                "bench_number": 1,
                "column_letter": "B",
                "side": "Left",
                "classroom": "EAB 415",
                "subject": "Robot Programming"
            }
        ]
    },
    {
        "rollnum": 12118002,
        "name": "ADITHYA DINESH RAO",
        "Year": "SecondYear",
        "seatnum": [
            {
                "date": "24-04-2023",
                "seatnum": "BR1",
                "seat_label": "BR",
                "section": "b",
                "bench_number": 1,
                "column_letter": "B",
                "side": "Right",
                "classroom": "EAB 415",
                "subject": "Robot Programming"
            }
        ]
    },
    {
        "rollnum": 12118003,
        "name": "ALAN GEORGE SHIBU",
        "Year": "SecondYear",
        "seatnum": [
            {
                "date": "24-04-2023",
                "seatnum": "BL2",
                "seat_label": "BL",
                "section": "b",
                "bench_number": 2,
                "column_letter": "B",
                "side": "Left",
                "classroom": "EAB 415",
                "subject": "Robot Programming"
            }
        ]
    },
    {
        "rollnum": 12118004,
        "name": "ANN MARY SHAJI",
        "Year": "SecondYear",
        "seatnum": [
            {
                "date": "24-04-2023",
                "seatnum": "BR2",
                "seat_label": "BR",
                "section": "b",
                "bench_number": 2,
                "column_letter": "B",
                "side": "Right",
                "classroom": "EAB 415",
                "subject": "Robot Programming"
            }
        ]
    }
]

# Sample teacher record
sample_teacher = {
    "username": "teacher_eab415",
    "password": "demo123",
    "name": "Dr. John Smith",
    "invigilation_hall": "EAB 415"
}

print("=" * 80)
print("EXAM SEATING ARRANGEMENT SYSTEM - SAMPLE DATA DEMONSTRATION")
print("=" * 80)
print()

print("TEACHER LOGIN DATA:")
print("-" * 80)
print(f"Username: {sample_teacher['username']}")
print(f"Password: {sample_teacher['password']}")
print(f"Hall Assigned: {sample_teacher['invigilation_hall']}")
print()

print("CLASSROOM LAYOUT TABLE FOR DATE: 24-04-2023")
print("HALL: EAB 415")
print("-" * 80)
print()

# Build seating grid for the specific date
date_filter = "24-04-2023"
seating_grid = {}

for student in sample_students:
    for seat in student.get('seatnum', []):
        if seat.get('date') == date_filter:
            row = seat.get('bench_number')
            col = seat.get('column_letter')
            side = seat.get('side')[0]  # 'L' or 'R'
            
            if row not in seating_grid:
                seating_grid[row] = {}
            if col not in seating_grid[row]:
                seating_grid[row][col] = {}
            
            seating_grid[row][col][side] = {
                'rollnum': student.get('rollnum'),
                'name': student.get('name'),
                'subject': seat.get('subject')
            }

# Get columns and max row
columns = sorted(set([col for row_dict in seating_grid.values() for col in row_dict.keys()]))
max_row = max(seating_grid.keys()) if seating_grid else 0

# Print table header
print("┌─────┬" + "─" * 20 + "┬" + "─" * 20 + "┬" + "─" * 20 + "┬" + "─" * 20 + "┐")
print("│ ROW │ A (Left)         │ A (Right)        │ B (Left)         │ B (Right)        │")
print("├─────┼─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤")

# Print rows
for row_num in range(1, max_row + 1):
    row_data = seating_grid.get(row_num, {})
    
    row_str = f"│  {row_num}  │"
    for col in columns:
        col_data = row_data.get(col, {})
        
        # Left seat
        left = col_data.get('L')
        if left:
            seat_info = f"{col}L{row_num}: {left['rollnum']}"
            row_str += f" {seat_info:<17} │"
        else:
            row_str += f" {'':<17} │"
    
    print(row_str)
    print("├─────┼─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤")

print("└─────┴─────────────────────┴─────────────────────┴─────────────────────┴─────────────────────┘")
print()

print("DETAILED STUDENT LIST FOR DATE: 24-04-2023")
print("-" * 80)
print(f"{'Seat ID':<12} {'Roll No':<12} {'Name':<25} {'Subject':<30} {'Side':<8}")
print("-" * 80)

for student in sample_students:
    for seat in student.get('seatnum', []):
        if seat.get('date') == date_filter:
            seatid = seat.get('seatnum')
            rollno = student.get('rollnum')
            name = student.get('name')[:25]
            subject = seat.get('subject')[:30]
            side = seat.get('side')
            
            print(f"{seatid:<12} {rollno:<12} {name:<25} {subject:<30} {side:<8}")

print()
print("=" * 80)
print("FEATURES AVAILABLE IN TEACHER DASHBOARD:")
print("=" * 80)
print("""
1. SEATING ARRANGEMENT TABLE
   - Displays rows (benches) and columns (A, B, C, etc.)
   - Shows seat IDs (e.g., AL1, AR1) with roll numbers
   - Color-coded: Left seats (blue), Right seats (yellow)

2. DATE NAVIGATION
   - Dropdown selector to choose exam date
   - Previous/Next buttons to navigate between dates
   - Only shows students for selected date

3. EXPORT FUNCTIONALITY
   - CSV download button for current hall & date
   - Includes all student details and seating info

4. DETAILED LIST
   - Table with full student information
   - Columns: Seat ID, Roll No, Name, Subject, Year, etc.

5. DEBUG & VERIFICATION
   - /teacher/hall_debug - JSON view of seating data
   - /teacher/export_csv - CSV export endpoint
""")

print("=" * 80)
print("APP URLs:")
print("=" * 80)
print("""
Home:                 http://localhost:5000/
Admin Login:          http://localhost:5000/admin/login
Teacher Login:        http://localhost:5000/teacher/login
Student Login:        http://localhost:5000/student/login

After Teacher Login:
Dashboard:            http://localhost:5000/teacher/dashboard
Debug JSON:           http://localhost:5000/teacher/hall_debug
Export CSV:           http://localhost:5000/teacher/export_csv?date=24-04-2023
""")
print("=" * 80)
