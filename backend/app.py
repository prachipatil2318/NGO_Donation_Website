from flask import Flask
from flask_cors import CORS
from routes.donor_routes import donor_bp
from routes.admin_routes import admin_bp
from routes.donation_routes import donation_bp
from routes.report_routes import report_bp
app = Flask(__name__)
CORS(app)
app.register_blueprint(donor_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(donation_bp)
app.register_blueprint(report_bp)
@app.route("/")
def home():
    return "Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
