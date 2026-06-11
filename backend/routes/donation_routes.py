from flask import Blueprint, request, jsonify
from db import get_connection
donation_bp = Blueprint("donation_bp", __name__)
@donation_bp.post("/donation/save")
def save_donation():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        #  Insert into donation table
        donation_sql = """
            INSERT INTO donation 
            (D_id, Cause_name, amount, country, D_address, state, city, pincode, Donation_date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())
        """
        donation_values = (
            data["D_id"],
            data["Cause_name"],
            data["amount"],
            data["country"],
            data["address"],
            data["state"],
            data["city"],
            data["pincode"]
        )
        cursor.execute(donation_sql, donation_values)
        donation_id = cursor.lastrowid 
        #  Insert into report table
        report_sql = """
            INSERT INTO report (donor_id, total_amt, report_date)
            SELECT D_id, amount, Donation_date
            FROM donation
            WHERE donation_id = %s
        """
        cursor.execute(report_sql, (donation_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
@donation_bp.get("/donation/history")
def donation_history():
    D_id = request.args.get("D_id")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            d.amount,
            d.Cause_name,
            d.country,
            d.state,
            d.city,
            d.D_address,
            d.pincode,
            d.Donation_date,
            dr.d_name
        FROM donation d
        JOIN donors dr ON d.D_id = dr.D_id
        WHERE d.D_id = %s
        ORDER BY d.Donation_date DESC
    """, (D_id,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "history": records})