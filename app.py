from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shortages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Shortage Model
class Shortage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(150), nullable=False)
    supply_type = db.Column(db.String(100), nullable=False)
    quantity_needed = db.Column(db.Integer, nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(250), nullable=True)

# Inventory Model
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    supply_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')

@app.route('/distrubation')
def distrubation():
    highest_shortage = Shortage.query.order_by(Shortage.quantity_needed.desc()).first()
    return render_template('distrubation.html', highest_shortage=highest_shortage)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        hospital_name = request.form['hospital_name']
        supply_type = request.form['supply_type']
        quantity_needed = request.form['quantity_needed']
        contact_person = request.form['contact_person']
        contact_email = request.form['contact_email']
        contact_phone = request.form['contact_phone']
        address = request.form['address']
        new_shortage = Shortage(
            hospital_name=hospital_name,
            supply_type=supply_type,
            quantity_needed=quantity_needed,
            contact_person=contact_person,
            contact_email=contact_email,
            contact_phone=contact_phone,
            address=address
        )
        db.session.add(new_shortage)
        db.session.commit()
        return redirect(url_for('display'))
    return render_template('report.html')

@app.route('/display')
def display():
    shortages = Shortage.query.all()
    return render_template('display.html', shortages=shortages)

@app.route('/shortage/<string:hospital_name>')
def shortage_detail(hospital_name):
    shortage = Shortage.query.filter_by(hospital_name=hospital_name).first_or_404()
    return render_template('shortage_detail.html', shortage=shortage)

@app.route('/report_address', methods=['POST'])
def report_address():
    data = request.get_json()
    user_address = data.get('address', '').strip().lower()
    
    if not user_address:
        return jsonify({"status": "failure", "message": "Address not provided."})

    hospitals = Shortage.query.filter(Shortage.address.ilike(f'%{user_address}%')).all()
    sorted_hospitals = sorted(hospitals, key=lambda h: h.quantity_needed, reverse=True)
    
    return jsonify({
        "status": "success",
        "address": user_address,
        "nearest_hospitals": [
            {"hospital_name": h.hospital_name, "quantity_needed": h.quantity_needed}
            for h in sorted_hospitals
        ]
    })

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
# Connect to SQLite Database
def get_db_connection():
    conn = sqlite3.connect('pharmacy.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory', methods=['GET'])
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT StoreName, Location, PinCode, ContactName, ContactNo, SupplyID, SupplyName, Quantity, ExpiryDate, Status
    FROM inventory
    '''
    cursor.execute(query)
    inventory = cursor.fetchall()

    conn.close()

    return render_template('inventory.html', inventory=inventory)

@app.route('/request_management', methods=['GET'])
def request_management():
    return render_template('request_management.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    store_name = request.form['storeName']
    location = request.form['location']
    pin_code = request.form['pinCode']
    contact_name = request.form['contactName']
    contact_no = request.form['contactNo']
    supply_name = request.form['supplyName']
    quantity = request.form['quantity']
    expiry_date = request.form['expiryDate']

    # Validate that all fields are filled
    if not (store_name and location and pin_code and contact_name and contact_no and supply_name and quantity and expiry_date):
        flash("All fields must be filled.")
        return redirect(url_for('inventory'))

    # Validate that the expiry date is not before the current date
    if datetime.strptime(expiry_date, '%Y-%m-%d') < datetime.now():
        flash("Expiry date cannot be in the past.")
        return redirect(url_for('inventory'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO inventory (StoreName, Location, PinCode, ContactName, ContactNo, SupplyName, Quantity, ExpiryDate, Status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    ''', (store_name, location, pin_code, contact_name, contact_no, supply_name, quantity, expiry_date))

    conn.commit()
    conn.close()

    return redirect(url_for('inventory'))
    
@app.route('/search', methods=['POST'])
def search():
    location = request.form.get('location', '')
    supply_name = request.form.get('supplyName', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT ms.*, s.SupplyName, s.Quantity, s.ExpiryDate
    FROM MedicalStores ms
    JOIN Supplies s ON ms.MedicalStoreID = s.MedicalStoreID
    WHERE 1=1
    '''
    
    params = []

    if location:
        query += ' AND ms.Location LIKE ?'
        params.append(f'%{location}%')
    
    if supply_name:
        query += ' AND s.SupplyName LIKE ?'
        params.append(f'%{supply_name}%')
    
    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()

    return render_template('request_management.html', results=results)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)