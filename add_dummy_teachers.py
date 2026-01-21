#!/usr/bin/env python3
"""
Script to insert dummy teacher data into MongoDB
Run this once to populate the teacher collection with test data
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.Studetails
teacher_collection = db.teacher

# Dummy teacher data
teachers = [
    {
        "username": "teacher1",
        "password": "pass123",
        "name": "Mr. John Doe",
        "assigned_class": "Class A",
        "assigned_subject": "Mathematics",
        "email": "john@email.com",
        "phone": "9876543210"
    },
    {
        "username": "teacher2",
        "password": "pass456",
        "name": "Ms. Sarah Smith",
        "assigned_class": "Class B",
        "assigned_subject": "English",
        "email": "sarah@email.com",
        "phone": "9876543211"
    },
    {
        "username": "teacher3",
        "password": "pass789",
        "name": "Dr. Raj Kumar",
        "assigned_class": "Class C",
        "assigned_subject": "Science",
        "email": "raj@email.com",
        "phone": "9876543212"
    }
]

# Insert teachers
try:
    result = teacher_collection.insert_many(teachers)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} teachers!")
    print("\nTeacher credentials:")
    for teacher in teachers:
        print(f"  Username: {teacher['username']}, Password: {teacher['password']}, Class: {teacher['assigned_class']}")
except Exception as e:
    print(f"❌ Error: {e}")
