from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, session, Response
from markupsafe import Markup

from datetime import datetime
from static.converter import excel_to_json
import os
import math
import json
import logging
from werkzeug.utils import secure_filename
from pymongo import MongoClient

# configuring flask

app = Flask(__name__)
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploads")



# Connect to Local MongoDB
client = MongoClient("mongodb://localhost:27017/")
# client = pymongo.MongoClient(
#     "mongodb://localhost:27017")

db = client.Studetails
usercollections = db.users
stucollections = db.student
techercollections = db.teacher

# global variables
listy = []
filled = False
with open('static/dates.txt', 'r') as datefiles:
    dates = json.load(datefiles)

# routes
# homepage
@app.route('/')
def index():
    return render_template('home.html')

# signup page for admin
@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists in the database
        if usercollections.find_one({'username': username}):
            flash('Username already exists', 'registration-error')
            return redirect(url_for('register'))
        
        else:
            # If the username is unique, insert the new user into the database
            usercollections.insert_one(
                {'username': username, 'password': password})
            flash('Registration successful!', 'registration-success')
            return redirect(url_for('login'))
    else:
        return render_template('adminlogin.html')


# login page for admin
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    session['username'] = None
    if request.method == 'POST':
        # Retrieve the username and password from the form
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match a user in the database
        user = usercollections.find_one(
            {'username': username, 'password': password})
        
        if user:
            # If the user exists, store the username in the session
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'login-error')
            return redirect(url_for('login'))
    else:
        return render_template('adminlogin.html')


# main page of admin where he can choose the classes
@app.route('/admin')
def admin():
    # Check if user is logged in
    if session['username'] is None:
        flash('Please login first', 'login-error')
        return redirect(url_for('login'))
    
    return render_template('adminhome.html')


# main page of admin where he can choose the classes
@app.route('/logout')
def logout():
    # Check if user is logged in
    session['username'] = None
    flash('Logged out successfully', 'logout-success')
    
    return render_template('/adminlogin.html')

# Student Login Route
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        roll = request.form['roll_num']
        student_data = stucollections.find_one({'rollnum': int(roll)})
        
        if student_data is not None:
            seatnum = student_data.get('seatnum')
            # Get the first (earliest) exam date for the student
            earliest_date = None
            if isinstance(seatnum, list) and len(seatnum) > 0:
                dates_list = []
                for seat in seatnum:
                    if isinstance(seat, dict) and seat.get('date'):
                        dates_list.append(seat.get('date'))
                if dates_list:
                    earliest_date = sorted(dates_list)[0]
            
            return render_template('studentpage.html', roll_num=roll, seat_num=seatnum, exam_date=earliest_date)
        else:
            flash('Roll number not found', 'login-error')
            return redirect(url_for('student_login'))
    else:
        return render_template('studentlogin.html')
    
# When student enters their rollnumber
# their corresponding seating is displayed
@app.route('/student', methods=['GET', 'POST'])
def student():
    # Check if user is logged in
    if 'student_username' not in session or session['student_username'] is None:
        flash('Please login first', 'login-error')
        return redirect(url_for('student_login'))
    
    if request.method == 'POST':
        roll = request.form['roll_num']
        student_data = stucollections.find_one({'rollnum': int(roll)})
        
        # Retrieve the seat number for the student
        seatnum = None
        if student_data is not None:
            seatnum = student_data['seatnum']
        return render_template('studentpage.html', roll_num=roll, seat_num=seatnum)
    else:
        return render_template('studentpage.html')


# ============== TEACHER MODULE ==============

# Teacher Login Route
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if teacher exists in database
        teacher = techercollections.find_one({'username': username, 'password': password})
        
        if teacher:
            session['teacher_username'] = username
            session['teacher_id'] = str(teacher['_id'])
            flash('Login successful!', 'login-success')
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid username or password', 'login-error')
            return redirect(url_for('teacher_login'))
    else:
        return render_template('teacherlogin.html')


# Teacher Dashboard - Show Invigilation Hall and Students
@app.route('/teacher/dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'teacher_username' not in session:
        flash('Please login first', 'login-error')
        return redirect(url_for('teacher_login'))
    
    try:
        # Get teacher info
        teacher = techercollections.find_one({'username': session['teacher_username']})
        if not teacher:
            flash('Teacher not found', 'error')
            return redirect(url_for('teacher_login'))
        
        # Get invigilation hall and teacher display name
        invigilation_hall = str(teacher.get('invigilation_hall', 'Not Assigned'))
        teacher_name = str(teacher.get('name', session['teacher_username']))
        
        # Get students who have a seat entry for this hall (seatnum is an array of dicts)
        students_in_hall = []
        if invigilation_hall and invigilation_hall != 'Not Assigned':
            # Query student docs where any seat entry has classroom equal to invigilation_hall
            students_in_hall = list(stucollections.find({'seatnum.classroom': invigilation_hall}))
        
        # Extract unique dates for this hall
        available_dates = set()
        for student in students_in_hall:
            seatnums = student.get('seatnum', [])
            if isinstance(seatnums, list):
                for seat in seatnums:
                    if isinstance(seat, dict):
                        date = seat.get('date')
                        if date:
                            available_dates.add(date)
        
        available_dates = sorted(list(available_dates))
        
        # Get selected date from request or use first available date
        selected_date = request.args.get('date')
        if not selected_date and available_dates:
            selected_date = available_dates[0]
        
        # Process seating data for selected date only
        processed_students = []
        conflicts = []
        for student in students_in_hall:
            seatnums = student.get('seatnum', [])
            if isinstance(seatnums, list):
                for seat in seatnums:
                    if isinstance(seat, dict) and seat.get('date') == selected_date:
                        # Skip this student if the same roll number is assigned to a different hall for the same date
                        try:
                            other_conflict = stucollections.find_one({
                                '_id': {'$ne': student.get('_id')},
                                'rollnum': student.get('rollnum'),
                                'seatnum': {'$elemMatch': {'date': selected_date, 'classroom': {'$ne': invigilation_hall}}}
                            })
                        except Exception:
                            other_conflict = None
                        if other_conflict:
                            conflicts.append({'rollnum': student.get('rollnum'), 'other_classroom': other_conflict.get('seatnum')[0].get('classroom', '') if other_conflict.get('seatnum') else ''})
                            continue

                        student_data = {
                            'rollnum': student.get('rollnum'),
                            'name': student.get('name'),
                            'Year': student.get('Year'),
                                'seatnum': seat.get('seatnum', '-'),
                                'seat_label': seat.get('seat_label', (seat.get('column_letter','') + ( 'R' if seat.get('side')=='Right' else 'L'))),
                            'section': seat.get('section', '-'),
                            'bench_number': seat.get('bench_number', '-'),
                            'column_letter': seat.get('column_letter', '-'),
                            'side': seat.get('side', '-'),
                            'date': seat.get('date', '-'),
                                'branch': student.get('branch', ''),
                                'classroom': seat.get('classroom', invigilation_hall),
                            'subject': seat.get('subject', '-')
                        }
                        processed_students.append(student_data)
        
        # Get ONLY subjects that have students in THIS hall for selected date
        subjects_in_hall = set()
        for student in processed_students:
            subject = student.get('subject')
            if subject:
                subjects_in_hall.add(str(subject))
        subjects_in_hall = sorted(list(subjects_in_hall))
        
        # Build subject entries grouped by subject code with register numbers and counts
        subject_map = {}
        for s in processed_students:
            subj = s.get('subject') or 'Unknown'
            subj_key = str(subj)
            if subj_key not in subject_map:
                subject_map[subj_key] = {
                    'subject': subj_key,
                    'year': s.get('Year', ''),
                    'deg': 'UG',
                    'dept': s.get('branch', '') if s.get('branch') else '',
                    'registers': []
                }
            # add rollnum
            if s.get('rollnum') is not None:
                subject_map[subj_key]['registers'].append(str(s.get('rollnum')))

        # Helper function to format register numbers as range
        def format_register_range(rollnums):
            """Convert list of roll numbers to range format like '99990001-020'"""
            if not rollnums:
                return '-'
            try:
                nums = sorted([int(r) for r in rollnums])
                if len(nums) == 0:
                    return '-'
                if len(nums) == 1:
                    return str(nums[0])
                # Format as "first-last" where last shows only the suffix
                first = str(nums[0])
                last = str(nums[-1])
                # Show range as startnum-endnum (or just the tail if same prefix)
                return f"{first}-{last[-3:]}"  # shows last 3 digits of end
            except Exception:
                return ', '.join(str(r) for r in rollnums)
        
        # Convert map to list of entries
        subject_entries = []
        for subj_key, info in subject_map.items():
            registers = info.get('registers', [])
            entry = {
                'subject': info['subject'],
                'year': info.get('year', ''),
                'deg': info.get('deg', ''),
                'dept': info.get('dept', ''),
                'registers': registers,
                'registers_range': format_register_range(registers),
                'count': len(registers)
            }
            subject_entries.append(entry)
        # sort entries by subject name/code
        subject_entries = sorted(subject_entries, key=lambda x: x['subject'])

        # Build seating grid server-side for template rendering
        seating_grid = {}
        columns_set = set()
        max_row = 0
        for s in processed_students:
            try:
                row = int(s.get('bench_number') or 0)
            except Exception:
                row = 0
            col = s.get('column_letter') or ''
            side = 'R' if str(s.get('side')).lower().startswith('r') else 'L'
            columns_set.add(col)
            if row > max_row:
                max_row = row
            if row not in seating_grid:
                seating_grid[row] = {}
            if col not in seating_grid[row]:
                seating_grid[row][col] = {}
            seating_grid[row][col][side] = {
                'rollnum': s.get('rollnum'),
                'name': s.get('name'),
                'subject': s.get('subject'),
                'Year': s.get('Year'),
                'branch': s.get('branch',''),
                'seatnum': s.get('seatnum',''),
                'classroom': s.get('classroom','')
            }
        columns_set = sorted([c for c in columns_set if c])
        
        # Get next date index
        next_date = None
        prev_date = None
        if selected_date and available_dates:
            current_idx = available_dates.index(selected_date) if selected_date in available_dates else 0
            if current_idx < len(available_dates) - 1:
                next_date = available_dates[current_idx + 1]
            if current_idx > 0:
                prev_date = available_dates[current_idx - 1]
        
        total_students_in_hall = len(processed_students)
        total_subjects_in_hall = len(subjects_in_hall)
        if conflicts:
            flash(f"Excluded {len(conflicts)} duplicate roll no(s) assigned to other halls for {selected_date}.", 'error')
        
        return render_template('teacherdashboard.html', 
                             teacher_name=teacher_name,
                             invigilation_hall=invigilation_hall,
                             students_in_hall=processed_students,
                             total_students_in_hall=total_students_in_hall,
                             total_subjects=total_subjects_in_hall,
                             subjects_list=subjects_in_hall,
                             subject_entries=subject_entries,
                             seating_grid=seating_grid,
                             columns_set=columns_set,
                             max_row=max_row,
                             available_dates=available_dates,
                             selected_date=selected_date,
                             next_date=next_date,
                             prev_date=prev_date)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('teacher_login'))


# View Student Performance
@app.route('/teacher/student/<int:roll_num>', methods=['GET'])
def teacher_view_student(roll_num):
    if 'teacher_username' not in session:
        flash('Please login first', 'login-error')
        return redirect(url_for('teacher_login'))
    
    student = stucollections.find_one({'rollnum': roll_num})
    
    if student:
        return render_template('teacher_student_details.html', student=student)
    else:
        flash('Student not found', 'error')
        return redirect(url_for('teacher_dashboard'))


@app.route('/teacher/hall_debug', methods=['GET'])
def teacher_hall_debug():
    # Debug route: returns processed_students JSON for the logged-in teacher and optional date
    if 'teacher_username' not in session:
        return jsonify({'error': 'login required'}), 401
    teacher = techercollections.find_one({'username': session['teacher_username']})
    if not teacher:
        return jsonify({'error': 'teacher not found'}), 404
    invigilation_hall = str(teacher.get('invigilation_hall', 'Not Assigned'))
    if invigilation_hall == 'Not Assigned':
        return jsonify({'error': 'no hall assigned'}), 400
    selected_date = request.args.get('date')
    students_in_hall = list(stucollections.find({'seatnum.classroom': invigilation_hall}))
    # collect available dates
    available_dates = set()
    for student in students_in_hall:
        for seat in student.get('seatnum', []) or []:
            if isinstance(seat, dict) and seat.get('date'):
                available_dates.add(seat.get('date'))
    available_dates = sorted(list(available_dates))
    if not selected_date and available_dates:
        selected_date = available_dates[0]
    processed_students = []
    for student in students_in_hall:
        for seat in student.get('seatnum', []) or []:
            if isinstance(seat, dict) and seat.get('date') == selected_date:
                # ensure this roll isn't assigned to some other hall for the same date
                try:
                    other_conflict = stucollections.find_one({
                        '_id': {'$ne': student.get('_id')},
                        'rollnum': student.get('rollnum'),
                        'seatnum': {'$elemMatch': {'date': selected_date, 'classroom': {'$ne': invigilation_hall}}}
                    })
                except Exception:
                    other_conflict = None
                if other_conflict:
                    # skip duplicate roll assigned elsewhere
                    continue
                processed_students.append({
                    'rollnum': student.get('rollnum'),
                    'name': student.get('name'),
                    'Year': student.get('Year'),
                    'seat': seat
                })
    return jsonify({'hall': invigilation_hall, 'selected_date': selected_date, 'available_dates': available_dates, 'students': processed_students})


@app.route('/teacher/export_csv', methods=['GET'])
def teacher_export_csv():
    if 'teacher_username' not in session:
        flash('Please login first', 'login-error')
        return redirect(url_for('teacher_login'))
    teacher = techercollections.find_one({'username': session['teacher_username']})
    if not teacher:
        flash('Teacher not found', 'error')
        return redirect(url_for('teacher_login'))
    invigilation_hall = str(teacher.get('invigilation_hall', 'Not Assigned'))
    if invigilation_hall == 'Not Assigned':
        flash('No hall assigned', 'error')
        return redirect(url_for('teacher_dashboard'))

    selected_date = request.args.get('date')
    students_in_hall = list(stucollections.find({'seatnum.classroom': invigilation_hall}))
    # determine available dates
    available_dates = set()
    for student in students_in_hall:
        for seat in student.get('seatnum', []) or []:
            if isinstance(seat, dict) and seat.get('date'):
                available_dates.add(seat.get('date'))
    available_dates = sorted(list(available_dates))
    if not selected_date and available_dates:
        selected_date = available_dates[0]

    # build CSV
    import csv
    from io import StringIO

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['SeatID','RollNo','Name','Year','Subject','Column','Bench','Side','Classroom','Date'])
    for student in students_in_hall:
        for seat in student.get('seatnum', []) or []:
            if isinstance(seat, dict) and seat.get('date') == selected_date:
                # Skip if this roll is assigned in another hall for same date
                try:
                    other_conflict = stucollections.find_one({
                        '_id': {'$ne': student.get('_id')},
                        'rollnum': student.get('rollnum'),
                        'seatnum': {'$elemMatch': {'date': selected_date, 'classroom': {'$ne': invigilation_hall}}}
                    })
                except Exception:
                    other_conflict = None
                if other_conflict:
                    continue

                seatid = seat.get('seatnum') or (seat.get('column_letter','') + ( 'R' if seat.get('side')=='Right' else 'L') + str(seat.get('bench_number','')))
                cw.writerow([seatid, student.get('rollnum'), student.get('name'), student.get('Year'), seat.get('subject'), seat.get('column_letter'), seat.get('bench_number'), seat.get('side'), seat.get('classroom'), seat.get('date')])

    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={"Content-disposition": f"attachment; filename={invigilation_hall.replace(' ','_')}_{selected_date}.csv"})


# Teacher Logout
@app.route('/teacher/logout')
def teacher_logout():
    session['teacher_username'] = None
    session['teacher_id'] = None
    flash('Logged out successfully!', 'logout-success')
    return redirect(url_for('index'))


@app.route('/admin/load_sample', methods=['GET'])
def admin_load_sample():
    """Convenience route to insert sample teacher and student seating data for testing/viewing.
    Inserts a teacher assigned to 'ADM 303' and several students with seat assignments for a sample date.
    """
    # Sample date and hall
    sample_date = '18.11.2025'
    hall = 'ADM 303'

    # Create or update teacher
    techercollections.update_one({'username': 'teacher_adm303'}, {'$set': {
        'username': 'teacher_adm303',
        'password': 'demo123',
        'name': 'Demo Teacher',
        'invigilation_hall': hall
    }}, upsert=True)

    # Clear any existing sample students with rollnums starting with 999
    stucollections.delete_many({'rollnum': {'$gte': 99990000}})

    # Build sample students with seat assignments matching AL/AR/BL/BR pattern
    sample_students = [
        (99990001, 'STUDENT A', 'FourthYear', 'A', 1, 'Left', 'EC19702'),
        (99990002, 'STUDENT B', 'FourthYear', 'A', 1, 'Right', 'EC19702'),
        (99990003, 'STUDENT C', 'FourthYear', 'B', 1, 'Left', 'IT19741'),
        (99990004, 'STUDENT D', 'FourthYear', 'B', 1, 'Right', 'IT19741'),
        (99990005, 'STUDENT E', 'FourthYear', 'A', 2, 'Left', 'EC19702'),
        (99990006, 'STUDENT F', 'FourthYear', 'A', 2, 'Right', 'EC19702'),
    ]

    for roll, name, year, col, bench, side, subj in sample_students:
        seat_label = f"{col}{'L' if side=='Left' else 'R'}{bench}"
        doc = {
            'rollnum': int(roll),
            'name': name,
            'Year': year,
            'branch': 'ECE',
            'seatnum': [
                {
                    'date': sample_date,
                    'seatnum': seat_label,
                    'seat_label': seat_label[:2],
                    'bench_number': bench,
                    'column_letter': col,
                    'side': side,
                    'classroom': hall,
                    'subject': subj
                }
            ]
        }
        stucollections.replace_one({'rollnum': int(roll)}, doc, upsert=True)

    return f"Inserted sample teacher and {len(sample_students)} students for hall {hall} on {sample_date}.\n\nTeacher login: teacher_adm303 / demo123\nVisit /teacher/login to sign in."


@app.route('/class', methods=['GET'])
def classchoose():
    return render_template('classavailable.html')


# page for uploading student details
@app.route('/uploaddata', methods=['GET'])
def uploadpage():
    return render_template('studentdataupload.html')

# when the data is submitted from /uploaddata or studentdataupload.html the data is processed here
# Here the data is checked and uploaded to the database
    # with sheetname as classname,year,classroom:which is the class they are going to be seated
# the data is also passed to "listy" for later usage in /seating
# finally the uploaded data is displayed in uploadeddata.html


@app.route('/upload', methods=['POST'])
def upload_file():
    file2 = request.files['file2']
    file3 = request.files['file3']
    file4 = request.files['file4']

    if file2.filename == '' and file3.filename == '' and file4.filename == '':
        flash('No files uploaded', 'error')
        return render_template('studentdataupload.html')

    if file2.filename:
        filename2 = secure_filename(file2.filename)
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        global data2
        data2 = excel_to_json(os.path.join(
            app.config['UPLOAD_FOLDER'], filename2))
    else:
        data2 = None

    if file3.filename:
        filename3 = secure_filename(file3.filename)
        file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
        global data3
        data3 = excel_to_json(os.path.join(
            app.config['UPLOAD_FOLDER'], filename3))
    else:
        data3 = None

    if file4.filename:
        filename4 = secure_filename(file4.filename)
        file4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))
        global data4
        data4 = excel_to_json(os.path.join(
            app.config['UPLOAD_FOLDER'], filename4))
    else:
        data4 = None

    if data2 is not None:
        for sheet_name, sheet_data in data2.items():
            stucollections.insert_many([
                {**item, "sheet_name": sheet_name, "Year": "SecondYear", "classroom": None} for item in sheet_data
            ])

    if data3 is not None:
        for sheet_name, sheet_data in data3.items():
            stucollections.insert_many([
                {**item, "sheet_name": sheet_name, "Year": "ThirdYear", "classroom": None} for item in sheet_data
            ])

    if data4 is not None:
        for sheet_name, sheet_data in data4.items():
            stucollections.insert_many([
                {**item, "sheet_name": sheet_name, "Year": "FourthYear", "classroom": None} for item in sheet_data
            ])

    global listy
    listy = []
    details = []
    details = stucollections.aggregate(
        [{"$group": {"_id": "$subject", "ro": {"$push": "$rollnum"}}}])
    for i in details:
        listy.append(i)

    return render_template('uploadeddata.html', data2=data2, data3=data3, data4=data4)

# page for displaying the data via "GET" method
@app.route('/displaydata', methods=['GET'])
def display_data():
    return render_template('displaydata.html', data2=data2, data3=data3, data4=data4)

# here the timetable is uploaded via timetableupload.html
# the filename is checked
@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    if request.method == 'POST':
        # Retrieve uploaded files
        file2 = request.files['file2']
        file3 = request.files['file3']
        file4 = request.files['file4']

        if not file2 and not file3 and not file4:
            flash('No files uploaded', 'error')
            return render_template('timetableupload.html')

        # Check if file2 is uploaded
        if file2.filename:
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            global timetable2
            timetable2 = excel_to_json(os.path.join(
                app.config['UPLOAD_FOLDER'], filename2))
        else:
            timetable2 = None

        # Check if file3 is uploaded
        if file3.filename:
            filename3 = secure_filename(file3.filename)
            file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
            global timetable3
            timetable3 = excel_to_json(os.path.join(
                app.config['UPLOAD_FOLDER'], filename3))
        else:
            timetable3 = None

        # Check if file4 is uploaded
        if file4.filename:
            filename4 = secure_filename(file4.filename)
            file4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))
            global timetable4
            timetable4 = excel_to_json(os.path.join(
                app.config['UPLOAD_FOLDER'], filename4))
        else:
            timetable4 = None

        # "Year" field is set to "SecondYear"
        # creates a list of the "_id" field values for those documents.
        # It then repeats this process for students in their third and fourth year of study,
        # Fetch student IDs for each year level

        second_year_students = stucollections.find({"Year": "SecondYear"})
        second_year_student_ids = [student["_id"]
                                   for student in second_year_students]
        third_year_students = stucollections.find({"Year": "ThirdYear"})
        third_year_student_ids = [student["_id"]
                                  for student in third_year_students]
        fourth_year_students = stucollections.find({"Year": "FourthYear"})
        fourth_year_student_ids = [student["_id"]
                                   for student in fourth_year_students]

        # The code first checks if the timetable exists by checking if "timetable2" is not None.
        # If it does exist, the code iterates over the sheets in the timetable ("timetable2.items()"),
        # and for each subject in each sheet, it converts the "date" field to a string in the format '%d-%m-%Y'
        # using the "datetime.fromtimestamp()" and "strftime()" functions.
        # It then checks if the subject date is already in the "dates" list, and if not , adds it to the list.
        # The code then updates the "subject" field for each sheet in the "stucollections"
        # collection based on the sheet name, year level, and student IDs.
        # For each sheet, it uses the "update_many()" method to update the "subject" field of all documents in the collection
        # where the "sheet_name" field is equal to the current sheet, the "Year" field is equal to "SecondYear",
        # and the "_id" field is in the list of second-year student IDs retrieved earlier.

        # The updated "subject" field is set to the contents of the corresponding sheet in the "timetable2" dictionary,
        # which is accessed using the sheet name as the key(e.g., "timetable2["csa"]").
        # Update subjects in the "stucollections" collection based on the uploaded timetables

        if timetable2 is not None:
            for sheet_name, subjects in timetable2.items():
                for subject in subjects:
                    subject_date = datetime.fromtimestamp(
                        subject['date'] / 1000.0).strftime('%d-%m-%Y')
                    subject['date'] = subject_date
                    if subject_date not in dates:
                        dates.append(subject_date)
            stucollections.update_many(
                {"sheet_name": "csa", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["cs"]}}
            )
            stucollections.update_many(
                {"sheet_name": "csb", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["cs"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ec", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["ec"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ee", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["ee"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ad", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["ad"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ce", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["ce"]}}
            )
            # stucollections.update_many(
            #     {"sheet_name": "mea", "Year": "SecondYear",
            #         "_id": {"$in": second_year_student_ids}},
            #     {"$set": {"subject": timetable2["me"]}}
            # )
            # stucollections.update_many(
            #     {"sheet_name": "meb", "Year": "SecondYear",
            #         "_id": {"$in": second_year_student_ids}},
            #     {"$set": {"subject": timetable2["me"]}}
            # )
            stucollections.update_many(
                {"sheet_name": "me", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "mr", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["mr"]}}
            )
            stucollections.update_many(
                {"sheet_name": "rb", "Year": "SecondYear",
                    "_id": {"$in": second_year_student_ids}},
                {"$set": {"subject": timetable2["rb"]}}
            )

        if timetable3 is not None:
            for sheet_name, subjects in timetable3.items():
                for subject in subjects:
                    subject_date = datetime.fromtimestamp(
                        subject['date'] / 1000.0).strftime('%d-%m-%Y')
                    subject['date'] = subject_date
                    if subject_date not in dates:
                        dates.append(subject_date)
            stucollections.update_many(
                {"sheet_name": "csa", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["cs"]}}
            )
            stucollections.update_many(
                {"sheet_name": "csb", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["cs"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ee", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["ee"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ec", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["ec"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ce", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["ce"]}}
            )
            stucollections.update_many(
                {"sheet_name": "mea", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "meb", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "me", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "mr", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["mr"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ad", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["ad"]}}
            )
            stucollections.update_many(
                {"sheet_name": "rb", "Year": "ThirdYear",
                    "_id": {"$in": third_year_student_ids}},
                {"$set": {"subject": timetable3["rb"]}}
            )

        if timetable4 is not None:
            for sheet_name, subjects in timetable4.items():
                for subject in subjects:
                    subject_date = datetime.fromtimestamp(
                        subject['date'] / 1000.0).strftime('%d-%m-%Y')
                    subject['date'] = subject_date
                    if subject_date not in dates:
                        dates.append(subject_date)
            stucollections.update_many(
                {"sheet_name": "csa", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["cs"]}}
            )
            stucollections.update_many(
                {"sheet_name": "csb", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["cs"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ec", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["ec"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ce", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["ce"]}}
            )
            stucollections.update_many(
                {"sheet_name": "ee", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["ee"]}}
            )
            stucollections.update_many(
                {"sheet_name": "me", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "mea", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "meb", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["me"]}}
            )
            stucollections.update_many(
                {"sheet_name": "mr", "Year": "FourthYear",
                    "_id": {"$in": fourth_year_student_ids}},
                {"$set": {"subject": timetable4["mr"]}}
            )

        with open('static/dates.txt', 'w') as f:
            json.dump(dates, f, indent=4)
            flash('Upload successful', 'success')
        return render_template('timetableupload.html')
    else:
        flash('Upload failed', 'danger')
    return render_template('timetableupload.html')

# the timetable is fetched and displayed here
@app.route('/viewtimetable', methods=['GET'])
def view_timetable():
    # Fetch the documents from the MongoDB collection
    documents = stucollections.find(
        {}, {'sheet_name': 1, 'subject': 1, 'Year': 1})
    
    # Dictionary to store the timetable data
    timetables = {}
    for doc in documents:
        year = doc.get('Year')
        sheet_name = doc.get('sheet_name')
        subject = doc.get('subject')

        if year and sheet_name and subject:
            if year not in timetables:
                timetables[year] = {}

            if sheet_name not in timetables[year]:
                timetables[year][sheet_name] = subject
        
    # Render the timetable in HTML template
    return render_template('viewtimetable.html', timetables=timetables)


# unlike the /displaydata which displays the uploaded data
# this route fetches the uploaded data from the mongodb
@app.route('/viewdata', methods=['GET'])
def view_data():
    # Fetch the documents from the MongoDB collection
    documents = stucollections.find(
        {}, {'name': 1, 'rollnum': 1, 'sheet_name': 1, 'Year': 1})
    
    # List to store the retrieved data
    data = []
    
    for doc in documents:
        # Extract the relevant fields from each document and append them to the data list
        data.append({
            'name': doc['name'],
            'rollnum': doc['rollnum'],
            'sheet_name': doc['sheet_name'],
            'Year': doc['Year']
        })
        
    # Render the data in HTML template
    return render_template('viewdata.html', data=data)


# here we are assigning the classname and seat num for each class
@app.route('/details', methods=['POST'])
def details():
    if request.method == 'POST':
        # Get the list of selected items from the form
        items = request.form.getlist('item[]')

        # List to store the details of selected classes
        class_data = []

        # Dictionary mapping class items to their details
        class_details = {
            'ADM 303': {'class_name': 'ADM 303', 'column': 6, 'rows': 7},
            'ADM 304': {'class_name': 'ADM 304', 'column': 8, 'rows': 3},
            'ADM 305': {'class_name': 'ADM 305', 'column': 7, 'rows': 3},
            'ADM 306': {'class_name': 'ADM 306', 'column': 7, 'rows': 3},
            'ADM 307': {'class_name': 'ADM 307', 'column': 7, 'rows': 3},
            'ADM 308': {'class_name': 'ADM 308', 'column': 7, 'rows': 3},
            'ADM 309': {'class_name': 'ADM 309', 'column': 7, 'rows': 3},
            'ADM 310': {'class_name': 'ADM 310', 'column': 7, 'rows': 3},
            'ADM 311': {'class_name': 'ADM 311', 'column': 7, 'rows': 3},
            'EAB 206': {'class_name': 'EAB 206', 'column': 7, 'rows': 3},
            'EAB 306': {'class_name': 'EAB 306', 'column': 7, 'rows': 3},
            'EAB 401': {'class_name': 'EAB 401', 'column': 8, 'rows': 3},
            'EAB 304': {'class_name': 'EAB 304', 'column': 7, 'rows': 3},
            'EAB 303': {'class_name': 'EAB 303', 'column': 7, 'rows': 3},
            'EAB 104': {'class_name': 'EAB 104', 'column': 7, 'rows': 3},
            'EAB 103': {'class_name': 'EAB 103', 'column': 7, 'rows': 3},
            'EAB 203': {'class_name': 'EAB 203', 'column': 7, 'rows': 3},
            'EAB 204': {'class_name': 'EAB 204', 'column': 7, 'rows': 3},
            'WAB 206': {'class_name': 'WAB 206', 'column': 7, 'rows': 3},
            'WAB 105': {'class_name': 'WAB 105', 'column': 7, 'rows': 3},
            'WAB 107': {'class_name': 'WAB 107', 'column': 7, 'rows': 3},
            'WAB 207': {'class_name': 'WAB 207', 'column': 8, 'rows': 3},
            'WAB 212': {'class_name': 'WAB 212', 'column': 7, 'rows': 3},
            'WAB 210': {'class_name': 'WAB 210', 'column': 7, 'rows': 3},
            'WAB 211': {'class_name': 'WAB 211', 'column': 7, 'rows': 3},
            'WAB 205': {'class_name': 'WAB 205', 'column': 7, 'rows': 3},
            'WAB 305': {'class_name': 'WAB 305', 'column': 7, 'rows': 3},
            'WAB 303': {'class_name': 'WAB 303', 'column': 7, 'rows': 3},
            'WAB 403': {'class_name': 'WAB 403', 'column': 7, 'rows': 3},
            'WAB 405': {'class_name': 'WAB 405', 'column': 7, 'rows': 3},
            'EAB 415': {'class_name': 'EAB 415', 'column': 8, 'rows': 15},
            'EAB 416': {'class_name': 'EAB 416', 'column': 8, 'rows': 14},
            'WAB 412': {'class_name': 'WAB 412', 'column': 7, 'rows': 3},
            'EAB 310': {'class_name': 'EAB 310', 'column': 7, 'rows': 3},
        }

        for item in items:
            if item in class_details:
                class_data.append(class_details[item])

        # Write the class_data list to 'static/stuarrange.txt' file as JSON
        with open('static/stuarrange.txt', 'w') as f:
            json.dump(class_data, f, indent=4)

        global filled
        filled = False
        return render_template('classdetails.html', class_data=class_data)


# here the seating is done
# only two students can sit one bench but with different subjects as exam
# -issue-:this issue may arise when there is limited class and students with same subject maybe seated nearby
# using the skeleton file stuarrange.txt the students are seated into the classroom
# the timetable/date is noted . stuarrange.txt files which is the seating arrangement is generated for each day in the timetable

@app.route('/seating', methods=['GET'])
def seating():
    global filled
    
    if not os.path.exists('static/stuarrange.txt'):
        flash('Choose Class', 'error')
        return redirect(url_for('admin'))
    
    if filled:
        with open('static/stuarrange.txt', 'r') as stufiles:
            stulist = json.load(stufiles)
        flash('Already generated', 'error')
        return redirect(url_for('admin'))
    
    else:
        stucollections.update_many({}, {"$unset": {"seatnum": ""}})
        
        for date in dates:
            global listyy
            
            listyy = []
            details = stucollections.aggregate(
                [{"$group": {"_id": "$subject", "ro": {"$push": "$rollnum"}}}])
            for i in details:
                listyy.append(i)
            
            listy = []
            for item in listyy:
                for item1 in item["_id"]:
                    if item1.get("date") == date:
                        tempdict = dict(item)
                        tempdict["_id"] = item1
                        listy.append(tempdict)
                        
            with open('static/stuarrange.txt', 'r') as stufiles:
                stulist = json.load(stufiles)
            
            for i in stulist:
                i["a"] = []
                i["b"] = []
                i["c"] = []
                i["d"] = []
                class_name = i.get("class_name")
                
                if len(listy) == 0:
                    break
                
                total_seats = int(i["column"]) * int(i["rows"])
                seats_per_section = total_seats // 4
                remaining_seats = total_seats % 4
                
                seat_counts = [seats_per_section] * 4
                for j in range(remaining_seats):
                    seat_counts[j] += 1
                
                sections = ["a", "b", "c", "d"]
                idlist = []
                
                if len(listy) == 0:
                    continue
                    
                firstitem = listy[0]
                idlist.append(firstitem["_id"])
                listy.pop(0)
                
                # Calculate classroom layout parameters
                num_columns = int(i["column"])
                num_rows = int(i["rows"])
                benches_per_column = num_rows
                columns_list = ["A", "B", "C", "D", "E"][:num_columns]
                
                for section_idx, section_name in enumerate(sections):
                    section_seat_count = seat_counts[section_idx]
                    
                    for seat_num in range(section_seat_count):
                        if not firstitem or len(firstitem["ro"]) == 0:
                            if len(listy) == 0:
                                break
                            
                            firstitem = listy[0]
                            idlist.append(firstitem["_id"])
                            listy.pop(0)
                        
                        if not firstitem or len(firstitem["ro"]) == 0:
                            break
                        
                        i[section_name].append(firstitem["ro"][0])
                        
                        # Calculate classroom grid position based on index in section
                        idx_in_section = len(i[section_name])
                        # bench_number: each bench holds two seats (Left then Right)
                        bench_num = ((idx_in_section - 1) // 2) + 1
                        # side alternates: odd index -> Left, even index -> Right
                        seat_side = "Left" if (idx_in_section % 2 == 1) else "Right"
                        
                        # Map section (a,b,c,d) to column positions
                        section_map = {"a": 0, "b": 1, "c": 2, "d": 3}
                        col_idx = section_map.get(section_name, 0)
                        col_letter = columns_list[col_idx] if col_idx < len(columns_list) else "A"
                        
                        seatinfo = [{
                            "date": date,
                            # seat label like AR/AL/BR/BL depending on column and side
                            "seat_label": col_letter + ("R" if seat_side == "Right" else "L"),
                            "seatnum": col_letter + ("R" if seat_side == "Right" else "L") + str(bench_num),
                            "section": section_name,
                            "bench_number": bench_num,
                            "column_letter": col_letter,
                            "side": seat_side,
                            "classroom": class_name,
                            "subject": firstitem["_id"]["subject"]
                        }]
                        
                        stucollections.update_one(
                            {"rollnum": firstitem["ro"][0]},
                            {"$addToSet": {"seatnum": seatinfo}}
                        )
                        
                        firstitem["ro"].pop(0)
                    
                    if firstitem and len(firstitem["ro"]) != 0:
                        listy.append(firstitem)
                    
                    if len(listy) == 0:
                        break
                    
                    if listy:
                        firstitem = listy[0]
                        listy.pop(0)
                    else:
                        firstitem = None
            
            newlist = list(stulist)
            
            stunum = 0
            for listitem in listy:
                stunum += len(listitem["ro"])
            
            if stunum > 0:
                flash('Warning: Number of items exceeds total capacity.', 'danger')
                return render_template('classavailable.html', stunum=stunum)
            
            with open('static/stuarrange' + date + '.txt', 'w') as f:
                json.dump(newlist, f, indent=4)
            
            filled = True
        
        flash('Generated', 'success')
        return render_template("adminhome.html")
    
@app.route('/viewseating', methods=['GET'])
def viewseating():
    global filled
    if not filled:
        flash('Firstly generate seating', 'error')
        return render_template("adminhome.html")
    with open('static/dates.txt', 'r') as file:
        content = file.read()
    return render_template('viewseating.html', dates=Markup(content))
# Render the 'viewseating.html' template, passing the content of 'dates.txt' as the 'dates' variable
# Markup is used to mark the content as safe to render HTML tags, assuming the content contains HTML


@app.route('/viewseating/<path:name>', methods=['GET'])
def viewseating1(name):
    global filled
    if filled:
        file_loc = 'static/stuarrange'+name+'.txt'
        # Assumes static folder is defined in your Flask app
        with open(file_loc, 'r') as file:  # Open the file in read mode
            content = file.read()  # Read the content of the file

    else:
        flash('Firstly generate seating', 'error')
        return render_template("adminhome.html")
    return content


# Resetting everything out
@app.route('/reset', methods=['GET'])
def reset():
    return render_template('reset.html')


@app.route('/reset/collections', methods=['GET'])
def reset_collections():
    global filled
    filled = False
    stucollections.drop()  # Drop the 'student' collection
    message = "Student data has been deleted."
    return render_template('reset.html', message=message)


@app.route('/reset/users', methods=['GET'])
def reset_users():
    usercollections.drop()  # Drop the 'users' collection
    message = "Users has been deleted."
    return render_template('reset.html', message=message)


@app.route('/reset/static', methods=['GET'])
def reset_static():
    folder_path = 'static'
    files = os.listdir(folder_path)  # Get a list of all files in the folder
    for file in files:
        if file.startswith("stuarrange"):
            # Get the full path of the file
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)  # Remove the file from the folder
    message = "Static files have been reset."
    global filled
    filled = False
    return render_template('reset.html', message=message)


@app.route('/reset/uploads', methods=['GET'])
def reset_uploads():
    folder_path = 'uploads'
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)
    message = "Uploads have been reset."
    return render_template('reset.html', message=message)


@app.route('/reset/dates', methods=['GET'])
def reset_dates():
    folder_path = 'static'
    file_path = os.path.join(folder_path, 'dates.txt')
    with open(file_path, 'w') as file:
        file.write('[]')
    message = "Dates have been reset."
    return render_template('reset.html', message=message)

# main function
if __name__ == '__main__':
    # Disable the reloader to avoid Windows Watchdog socket errors during development
    app.run(debug=True, use_reloader=False)
    


