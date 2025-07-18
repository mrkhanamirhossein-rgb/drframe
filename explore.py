# explore.py

import os  # For file and directory operations
import sqlite3  # For interacting with SQLite databases
from users import DB_NAME, get_user_profile  # Import database name and user profile function
from webulits import render  # Import render function for HTML templates

def list_users():
    """بازگرداندن لیست کاربران همراه با اطلاعات ضروری برای اکسپلور"""
    with sqlite3.connect(DB_NAME) as conn:  # Connect to the SQLite database
        cur = conn.cursor()  # Create a cursor object for executing SQL queries
        cur.execute("SELECT username, fullname, skills, avatar FROM users")  # Query user info
        rows = cur.fetchall()  # Fetch all results from the query
    users = []  # Initialize an empty list to store user dictionaries
    for row in rows:  # Iterate over each row from the query result
        users.append({
            "username": row[0],  # Username from the database
            "fullname": row[1] or row[0],  # Full name or fallback to username
            "skills": row[2] or '',  # Skills or empty string if None
            "avatar": row[3] or '/static/avatar.png',  # Avatar or default image
        })
    return users  # Return the list of user dictionaries

def get_explore_html(context=None):
    """صفحه اکسپلور کاربران"""
    users = list_users()  # Get the list of users
    return render("explore_users.html", {"users": users, **(context or {})})  # Render the explore page

def get_user_html(username, context=None):
    """نمایش کامل پروفایل یک کاربر"""
    profile = get_user_profile(username)  # Get the user's profile data
    if not profile:  # If the user was not found
        return render("404.html", {"title": "کاربر پیدا نشد"})  # Render a 404 page
    return render("user_profile.html", {**profile, **(context or {})})  # Render the user's profile page

def get_resume_path(username):
    return f"resumes/{username}.pdf"  # Generate the path for the user's PDF resume

def user_has_resume(username):
    return os.path.isfile(get_resume_path(username))  # Check if the resume file exists

def save_resume(username, file_content):
    os.makedirs("resumes", exist_ok=True)  # Ensure the resumes directory exists
    with open(get_resume_path(username), "wb") as f:  # Open the resume file for writing in binary mode
        f.write(file_content)  # Write the file content to disk
    return True  # Indicate success

def get_resume_download_link(username):
    if user_has_resume(username):  # If the user has a resume file
        return f"/static/resumes/{username}.pdf"  # Return the static URL for download
    return ""  # Return an empty string if no resume

