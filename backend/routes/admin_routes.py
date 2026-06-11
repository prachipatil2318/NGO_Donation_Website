from flask import Blueprint, request, jsonify
from db import get_connection
import random
admin_bp = Blueprint("admin_bp", __name__)
# ------------------ ADMIN REGISTER ------------------
@admin_bp.post("/admin/register")
def admin_register():
    try:
        data = request.json
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        conn = get_connection()
        cursor = conn.cursor()
        # Check if email already exists
        cursor.execute("SELECT * FROM admin WHERE admin_email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"})
        # Generate Admin ID: first 3 letters uppercase + random 5-digit number
        admin_id = f"{name[:3].upper()}-{random.randint(10000, 99999)}"
        # Insert into DB
        cursor.execute(
            "INSERT INTO admin (admin_id, admin_name, admin_email, admin_password, admin_phno) "
            "VALUES (%s, %s, %s, %s, %s)",
            (admin_id, name, email, password, phone)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Admin registered successfully", "adminId": admin_id})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
# ------------------ ADMIN LOGIN ------------------
@admin_bp.post("/admin/login")
def admin_login():
    try:
        data = request.json
        admin_id = data["adminId"]
        password = data["password"]
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Case-insensitive match for admin ID
        cursor.execute(
            "SELECT * FROM admin WHERE LOWER(admin_id)=LOWER(%s)",
            (admin_id,)
        )
        admin = cursor.fetchone()
        if not admin:
            return jsonify({"success": False, "message": "Admin ID not found"})
        if admin["admin_password"] != password:
            return jsonify({"success": False, "message": "Incorrect password"})
        return jsonify({"success": True, "admin": admin})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})