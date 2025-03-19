import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import random
import json
def generate_otp():
    return str(random.randint(1000, 9999))  # Ensures a 4-digit number

def send_email(rec):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users WHERE email = ?", (rec,))
    record = cursor.fetchone()

    conn.close()
    print(record)
    record = 3 
    if record == 2: 
        return 0
    else :
        sender_email = "verdantrokade@gmail.com"  # Replace with your email
        app_password = "jeiglcxeviwaducq"  # Replace with your generated app password
        receiver_email = rec  # Replace with the recipient's email
    
        subject = "OTP for verfication"
        otp = generate_otp()
        body = f'Hello, your otp for propertybharat.com is {otp}.'
    
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
    
        try:
            # Connect to the SMTP server (Gmail)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Secure the connection
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
            return otp
        except Exception as e:
            print("Failed to send email:", e)


def store_email_otp(email, otp1):
    otp = otp1  # Generate OTP
    print(email)

    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            otp TEXT, 
            password TEXT
        )
    ''')

    # Insert or update OTP for the email
    cursor.execute("INSERT INTO otp_data (email, otp) VALUES (?, ?) ON CONFLICT(email) DO UPDATE SET otp = ?", (email, otp, otp))

    # Commit and close
    conn.commit()
    conn.close()

    print(f"OTP for {email} stored successfully: {otp}")


def verify_otp1(email, user_otp):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT otp FROM otp_data WHERE email = ?", (email,))
    record = cursor.fetchone()

    conn.close()

    if record and record[0] == user_otp:
        print("OTP Verified Successfully!")
        return True
    else:
        print("Invalid OTP!")
        return False
    
def resend_otp(email):
    otp3 = send_email(email)
    store_email_otp(email,otp3)

def store_password(email, password, propertyt, role, mobile):
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    # Check if 'mobile' column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]  # Get column names

    if 'mobile' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN mobile TEXT")
        conn.commit()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            propertyt TEXT,
            role TEXT,
            mobile TEXT
        )
    ''')

    # Insert or update password, propertyt, role, and mobile
    cursor.execute('''
        INSERT INTO users (email, password, propertyt, role, mobile) 
        VALUES (?, ?, ?, ?, ?) 
        ON CONFLICT(email) DO UPDATE SET password = ?, propertyt = ?, role = ?, mobile = ?
    ''', (email, password, propertyt, role, mobile, password, propertyt, role, mobile))

    conn.commit()
    conn.close()
    print(f"Password for {email} stored successfully.")

    
def login3(email1, password):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    # Fetch password and propertyt from database for the given email
    cursor.execute("SELECT password, propertyt, role FROM users WHERE email = ?", (email1,))
    record = cursor.fetchone()
    conn.close()
    print(record)
    print(email1)

    # Check if a record exists and compare passwords
    if record and record[0] == password:
        print("User Verified Successfully!")
        propertyt = record[1]
        role33=record[2]
        if propertyt == 'residential' and role33 == 'owner':
            return 1
        elif propertyt == 'commercial' and role33 == 'owner':
            return 2
        elif role33 == 'broker':
            return 4
        elif role33 == 'redev':
            return 3
    else:
        print("Invalid user!")
        return 0
    

def save_prop(email, name, city, loc, prop, pi, date, proptype, loc_hub, owner, deposit, comments, photos,price):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    # Check if 'properties' column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]  # Get column names

    if 'properties' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN properties TEXT DEFAULT '[]'")
        conn.commit()

    # Fetch existing properties for the user
    cursor.execute("SELECT properties FROM users WHERE email = ?", (email,))
    record = cursor.fetchone()

    if record and record[0]:
        properties = json.loads(record[0])
    else:
        properties = []

    # Add new property to the list
    new_property = {
        'name': name,
        'city': city,
        'locality': loc,
        'propertyname': prop,
        'possession_status': pi,
        'possession_date': date,
        'property_type': proptype,
        'location_hub': loc_hub,
        'ownership': owner,
        'deposit': deposit,
        'comments': comments,
        'photos': photos,
        'price': price
    }
    properties.append(new_property)

    # Update the properties column in the database
    cursor.execute("UPDATE users SET properties = ? WHERE email = ?", (json.dumps(properties), email))

    conn.commit()
    conn.close()

    print(f"Property for {email} stored successfully.")


def save_prop1(email, name, city, user_type, mobile, firm_name, business_since):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    print(email, name, city, user_type, mobile, firm_name, business_since)

    # Check if 'properties' column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]  # Get column names

    if 'properties' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN properties TEXT DEFAULT '[]'")
        conn.commit()

    # Fetch existing properties for the user
    cursor.execute("SELECT properties FROM users WHERE email = ?", (email,))
    record = cursor.fetchone()

    if record and record[0]:
        properties = json.loads(record[0])
    else:
        properties = []

    # Add new property to the list
    new_property = {
        'email': email,
        'name': name,
        'city': city,
        'user_type': user_type,
        'mobile': mobile,
        'firm_name': firm_name,
        'business_since': business_since
    }
    properties.append(new_property)

    # Update the properties column in the database
    cursor.execute("UPDATE users SET properties = ? WHERE email = ?", (json.dumps(properties), email))

    conn.commit()
    conn.close()

    print(f"Property for {email} stored successfully.")


def save_prop2(email, propertyName, location, propertyType, address, builtUpArea, carpetArea, ownership, totalFloors, totalFlats, totalOwners, comments):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    # Check if 'properties' column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]  # Get column names

    if 'properties' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN properties TEXT DEFAULT '[]'")
        conn.commit()

    # Fetch existing properties for the user
    cursor.execute("SELECT properties FROM users WHERE email = ?", (email,))
    record = cursor.fetchone()

    if record and record[0]:
        properties = json.loads(record[0])
    else:
        properties = []

    # Add new property to the list
    new_property = {
        'propertyName': propertyName,
        'location': location,
        'propertyType': propertyType,
        'address': address,
        'builtUpArea': builtUpArea,
        'carpetArea': carpetArea,
        'ownership': ownership,
        'totalFloors': totalFloors,
        'totalFlats': totalFlats,
        'totalOwners': totalOwners,
        'comments': comments,
    }
    properties.append(new_property)

    # Update the properties column in the database
    cursor.execute("UPDATE users SET properties = ? WHERE email = ?", (json.dumps(properties), email))

    conn.commit()
    conn.close()

    print(f"Property for {email} stored successfully.")



def save_prop3(email, name, location, propertyType, possession, buildupArea, carpetArea, ownership, totalFloors, yourFloor, seats, rooms, cabins, price, locationHub, condition, comments):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    # Check if 'properties' column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]  # Get column names

    if 'properties' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN properties TEXT DEFAULT '[]'")
        conn.commit()

    # Fetch existing properties for the user
    cursor.execute("SELECT properties FROM users WHERE email = ?", (email,))
    record = cursor.fetchone()

    if record and record[0]:
        properties = json.loads(record[0])
    else:
        properties = []

    # Add new property to the list
    new_property = {
        'email': email,
        'name': name,
        'location': location,
        'propertyType': propertyType,
        'possession': possession,
        'buildupArea': buildupArea,
        'carpetArea': carpetArea,
        'ownership': ownership,
        'totalFloors': totalFloors,
        'yourFloor': yourFloor,
        'seats': seats,
        'rooms': rooms,
        'cabins': cabins,
        'price': price,
        'locationHub': locationHub,
        'condition': condition,
        'comments': comments,
    }
    properties.append(new_property)

    # Update the properties column in the database
    cursor.execute("UPDATE users SET properties = ? WHERE email = ?", (json.dumps(properties), email))

    conn.commit()
    conn.close()

    print(f"Property for {email} stored successfully.")
