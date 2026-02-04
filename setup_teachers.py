#!/usr/bin/env python3
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.Studetails
teacher_collection = db.teacher

teachers = [
    {
        "username": "teacher1",
        "password": "pass123",
        "name": "Mr. John Doe",
        "invigilation_hall": "ADM 303",
        "assigned_class": "Class A",
        "assigned_subject": "Mathematics",
        "email": "john@email.com",
        "phone": "9876543210"
    },
    {
        "username": "teacher2",
        "password": "pass456",
        "name": "Ms. Sarah Smith",
        "invigilation_hall": "EAB 206",
        "assigned_class": "Class B",
        "assigned_subject": "English",
        "email": "sarah@email.com",
        "phone": "9876543211"
    },
    {
        "username": "teacher3",
        "password": "pass789",
        "name": "Dr. Raj Kumar",
        "invigilation_hall": "WAB 207",
        "assigned_class": "Class C",
        "assigned_subject": "Science",
        "email": "raj@email.com",
        "phone": "9876543212"
    }
]

try:
    teacher_collection.delete_many({})
    result = teacher_collection.insert_many(teachers)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} teachers!")
    print("\nTeacher Invigilation Allocations:")
    for teacher in teachers:
        print(f"  {teacher['name']}: Hall {teacher['invigilation_hall']} | Login: {teacher['username']}")
except Exception as e:
    print(f"❌ Error: {e}")
