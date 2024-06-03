from models.blogModel import Blog
from models.childModel import Child
from models.notificationModel import Notification
from sqlalchemy import and_
from services.db import db
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getFilteredBlogs(age_from, age_to, gender):
    filters = []

    if age_from is not None:
        filters.append(Blog.age_from >= age_from)
        filters.append(Blog.age_to <= age_from)
    if age_to is not None:
        filters.append(Blog.age_from <= age_to)
        filters.append(Blog.age_to >= age_to)
    if gender is not None:
        filters.append(Blog.gender == gender)

    blogs = Blog.query.filter(and_(*filters)).all()
    return blogs

def send_email(notification):
    sender_email = "kartikjoshiuk@gmail.com"
    # password is removed for security reasons
    sender_password = ""

    # Email content
    subject = notification.subject
    body = notification.description

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = sender_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain", "utf-8"))
    context = ssl.create_default_context()

    try:
        # Connect to the Gmail server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, sender_email, message.as_string())
        print("Email sent successfully\n")
    except Exception as e:
        print(f"Error: {e}")


def send_notification(blogs, blogs_id, age_from, age_to, gender):
    print("Inside send notification")
    filters = []

    if age_from is not None:
        filters.append(Child.age >= age_from)
    if age_to is not None:
        filters.append(Child.age <= age_to)
    if gender is not None:
        filters.append(Child.gender == gender)
    
    parents = []
    children = Child.query.filter(and_(*filters)).all()
    parents = set(child.parent_id for child in children)
    print(parents)
    for parent_id in parents:
        new_notification = Notification(subject="New blog recommendation for you", description=f'{blogs.title}', blog_id=blogs_id, to=parent_id)
        db.session.add(new_notification)
        db.session.commit()
        send_email(new_notification)

