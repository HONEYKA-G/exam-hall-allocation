#!/usr/bin/env python3
"""
Script to add dummy seating arrangement for testing teacher module
Run this to assign students to halls for testing
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.Studetails
stucollections = db.student

# Sample students to assign to ADM 303 hall
# This simulates what happens when admin generates seating arrangement
seating_assignments = [
    {"rollnum": 11913001, "seatnum": "A1", "classroom": "ADM 303"},
    {"rollnum": 11913002, "seatnum": "A2", "classroom": "ADM 303"},
    {"rollnum": 11913003, "seatnum": "A3", "classroom": "ADM 303"},
    {"rollnum": 11913004, "seatnum": "A4", "classroom": "ADM 303"},
    {"rollnum": 11913005, "seatnum": "A5", "classroom": "ADM 303"},
    {"rollnum": 11913006, "seatnum": "A6", "classroom": "ADM 303"},
    {"rollnum": 12118001, "seatnum": "B1", "classroom": "ADM 303"},
    {"rollnum": 12118002, "seatnum": "B2", "classroom": "ADM 303"},
    {"rollnum": 12118003, "seatnum": "B3", "classroom": "ADM 303"},
    {"rollnum": 12118004, "seatnum": "B4", "classroom": "ADM 303"},
    {"rollnum": 12118005, "seatnum": "B5", "classroom": "ADM 303"},
    {"rollnum": 12118006, "seatnum": "B6", "classroom": "ADM 303"},
]

try:
    # Update each student with classroom and seat number
    updated_count = 0
    for assignment in seating_assignments:
        result = stucollections.update_one(
            {'rollnum': assignment['rollnum']},
            {'$set': {'classroom': assignment['classroom'], 'seatnum': assignment['seatnum']}}
        )
        if result.modified_count > 0:
            updated_count += 1
    
    print(f"✅ Successfully updated {updated_count} students with seating assignments!")
    print(f"\nStudents assigned to ADM 303:")
    students = stucollections.find({'classroom': 'ADM 303'})
    for student in students:
        print(f"  Roll: {student['rollnum']}, Seat: {student.get('seatnum', 'N/A')}, Subject: {student.get('subject', 'N/A')}")
except Exception as e:
    print(f"❌ Error: {e}")
