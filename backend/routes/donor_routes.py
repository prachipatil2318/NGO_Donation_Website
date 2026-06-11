from flask import Blueprint, request, jsonify
from db import get_connection
donor_bp = Blueprint("donor_bp", __name__)
# Register Donor
@donor_bp.post("/donor/register")
def donor_register():
    try:
        data = request.json
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        conn = get_connection()
        cursor = conn.cursor()
        # Check duplicate email
        cursor.execute("SELECT * FROM donors WHERE D_email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"})
        # Insert donor
        cursor.execute(
            "INSERT INTO donors (D_name, D_email, D_phno, D_password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Donor registered successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
# Donor Login
@donor_bp.post("/donor/login")
def donor_login():
    try:
        data = request.json
        email = data["email"]
        password = data["password"]
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors WHERE D_email=%s AND D_password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify({"success": True, "message": "Login successful", "user": user})
        else:
            return jsonify({"success": False, "message": "Invalid email or password"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})