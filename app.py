from flask import Flask, request, jsonify,render_template, abort
from flask_pymongo import PyMongo
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

app = Flask(__name__)


# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://vedant:nikhil@cluster0.2bsjy.mongodb.net/mydatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Email Configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "verdantrokade@gmail.com"
EMAIL_PASSWORD = "jeiglcxeviwaducq"


################################    pages ####################################

@app.route('/')
def home():
    return render_template("post-property.html")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard-com')
def dashboard_com():
    return render_template('dashboard-com.html')

@app.route('/next')
def next():
    return render_template('next.html')

@app.route('/register')
def register():
    return render_template("post-property.html")  # Ensure 'register.html' exists

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard-redev')
def dashboard_redev():
    return render_template('dashboard-redev.html')

@app.route('/dashboard-broker')
def dashboard_broker():
    return render_template('dashboard-broker.html') 
@app.route('/post-property', methods=['GET', 'POST'])
def post_property():
    if request.method == 'GET':
        return render_template("post-property.html")

##########################################################################


# Helper function to send email
def send_email(to_email, otp):
    try:
        msg = MIMEText(f"Your OTP is: {otp}")
        msg["Subject"] = "Your OTP Code"
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# Route to request an OTP
@app.route("/request-otp", methods=["POST"])
def request_otp():
    data = request.json
    email = data.get("email_or_mobile")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check if the "users" collection exists and if the user already exists
    if "users" in mongo.db.list_collection_names():
        if mongo.db.users.find_one({"email": email}):
            return jsonify({'tp': True}), 200  # User already exists

    # Generate a 6-digit OTP
    otp = random.randint(1000, 9999)
    expiry_time = datetime.utcnow() + timedelta(minutes=5)  # OTP expires in 5 minutes

    # Store OTP in MongoDB
    mongo.db.otp_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "expiry": expiry_time}},
        upsert=True
    )

    # Send OTP via email
    if send_email(email, otp):
        return jsonify({'tp2': True}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500
# Route to verify OTP
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email_or_mobile")
    mobile = data.get("cont")
    password = data.get("password")
    entered_otp = data.get("otp")
    propertytype = data.get("propertyt")
    role = data.get("userr")

    # Ensure all fields are provided
    if not all([email, mobile, password, entered_otp, propertytype, role]):
        return jsonify({"error": "All fields are required"}), 400

    # Fetch OTP from MongoDB
    record = mongo.db.otp_collection.find_one({"email": email})

    if not record:
        return jsonify({"error": "No OTP found for this email"}), 404

    # Check OTP validity
    if record["otp"] == int(entered_otp):
        if datetime.utcnow() > record["expiry"]:
            return jsonify({"error": "OTP expired"}), 400

        # Add user to the "users" collection with all specified fields
        mongo.db.users.insert_one({
            "email": email,
            "mobile": mobile,
            "password": password,
            "propertytype": propertytype,
            "role": role
        })

        return jsonify({"message": "OTP verified successfully, user created"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400




@app.route('/login1', methods=['POST'])
def login1():
    data = request.get_json()
    email1 = data.get('username')
    password = data.get('password')

    # Fetch user details from MongoDB
    record = mongo.db.users.find_one({"email": email1})

    if record and record.get("password") == password:
        propertyt = record.get("propertytype")
        role33 = record.get("role")

        if propertyt == 'residential' and role33 == 'owner':
            return jsonify({'success': True, 'ty': 1}), 200
        elif propertyt == 'commercial' and role33 == 'owner':
            return jsonify({'success': True, 'ty': 2}), 200
        elif role33 == 'broker':
            return jsonify({'success': True, 'ty': 4}), 200
        elif role33 == 'redev':
            return jsonify({'success': True, 'ty': 3}), 200

    return abort(401, description="Invalid credentials")



def save_property_to_user(email, property_data):
    """Function to append a property to the user's document"""
    user = mongo.db.users.find_one({"email": email})

    if user:
        # Append new property to the existing array
        mongo.db.users.update_one(
            {"email": email},
            {"$push": {"properties": property_data}}
        )
    else:
        # If user does not exist, create a new user with properties array
        mongo.db.users.insert_one({
            "email": email,
            "properties": [property_data]
        })


@app.route('/save-property', methods=['POST'])
def save_property():
    email = request.form.get('email')
    property_data = {
        "username": request.form.get('username'),
        "city": request.form.get('city'),
        "locality": request.form.get('locality'),
        "propertyname": request.form.get('propertyname'),
        "possession_status": request.form.get('possession_status'),
        "possession_date": request.form.get('possession_date'),
        "property_type": request.form.get('property_type'),
        "property_price": request.form.get('property_price'),
        "security_deposit": request.form.get('security_deposit'),
        "comments": request.form.get('comments'),
        "photos": []
    }

    # Save property photos
    property_photos = request.files.getlist('property_photos')
    i = 1
    for photo in property_photos:
        if photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{email}{property_data['propertyname']}{i}.jpg")
            photo.save(photo_path)
            property_data["photos"].append(photo_path)
            i += 1

    try:
        save_property_to_user(email, property_data)
        return jsonify({'message': 'Property saved successfully'}), 201
    except Exception as e:
        return abort(500, description=str(e))


@app.route('/save-property1', methods=['POST'])
def save_property1():
    email = request.form.get('email')
    property_data = {
        "user_type": request.form.get('user_type'),
        "city": request.form.get('city'),
        "name": request.form.get('name'),
        "mobile": request.form.get('mobile'),
        "firm_name": request.form.get('firm_name'),
        "business_since": request.form.get('business_since')
    }

    try:
        save_property_to_user(email, property_data)
        return jsonify({'message': 'Property saved successfully'}), 201
    except Exception as e:
        return abort(500, description=str(e))


@app.route('/save-property2', methods=['POST'])
def save_property2():
    email = request.form.get('email')
    property_data = {
        "propertyName": request.form.get('propertyName'),
        "location": request.form.get('location'),
        "propertyType": request.form.get('propertyType'),
        "address": request.form.get('address'),
        "builtUpArea": request.form.get('builtUpArea'),
        "carpetArea": request.form.get('carpetArea'),
        "ownership": request.form.get('ownership'),
        "totalFloors": request.form.get('totalFloors'),
        "totalFlats": request.form.get('totalFlats'),
        "totalOwners": request.form.get('totalOwners'),
        "comments": request.form.get('comments'),
        "photos": []
    }

    # Save property photos
    property_photos = request.files.getlist('property_photos')
    i = 1
    for photo in property_photos:
        if photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{email}{property_data['propertyName']}{i}.jpg")
            photo.save(photo_path)
            property_data["photos"].append(photo_path)
            i += 1

    try:
        save_property_to_user(email, property_data)
        return jsonify({'message': 'Property saved successfully'}), 201
    except Exception as e:
        return abort(500, description=str(e))


@app.route('/save-property3', methods=['POST'])
def save_property3():
    email = request.form.get('email')
    property_data = request.form.to_dict()

    try:
        save_property_to_user(email, property_data)
        return jsonify({'message': 'Property saved successfully'}), 201
    except Exception as e:
        return abort(500, description=str(e))



if __name__ == "__main__":
    app.run(debug=True)
