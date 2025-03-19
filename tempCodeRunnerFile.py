
def request_otp():
    email1 = request.json.get('email_or_mobile')
    try:
        otp2 = send_email(email1)
        if otp2 == 0:
            return jsonify({'tp': True}), 200
        else:
            store_email_otp(email1, otp2)
            return jsonify({'tp2': True}), 200
    except Exception as e:
        return abort(500, description=f"Failed to send email: {str(e)}")

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.json.get('email_or_mobile')
    password = request.json.get('password')
    entered_otp = request.json.get('otp')
    propertytype = request.json.get('propertyt')
    role = request.json.get('userr')
    print(role)
    if verify_otp1(email, entered_otp):
        store_password(email, password, propertytype, role)
        return jsonify({"message": "OTP verified successfully!"}), 200
    return abort(400, description="Invalid or expired OTP")

# ============================== Property Routes =======================