# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:01:25 2025

@author: MALACHI COMPUTERS
"""

import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    EMAIL_ADDRESS = "focusintech1@gmail.com"
    APP_PASSWORD = "yujn skmo qdtm hprv"  # 16 characters

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully ✅")
    

send_email(
    to_email="ekehboss1@gmail.com",
    subject="Task Reminder ⏰",
    body="This is a reminder for your task."
)

