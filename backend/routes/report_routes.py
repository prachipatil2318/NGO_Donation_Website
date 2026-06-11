from flask import Blueprint, request, jsonify
from db import get_connection
report_bp = Blueprint("report_bp", __name__)
@report_bp.get("/report/history")
def report_history():
    donor_id = request.args.get("donor_id")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.report_id,
            r.total_amt,
            r.report_date,
            d.d_name
        FROM report r
        JOIN donors d ON r.donor_id = d.D_id
        WHERE r.donor_id = %s
        ORDER BY r.report_date DESC
    """, (donor_id,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "reports": records})
