from config import db

class Shortage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(100), nullable=False)
    supply_type = db.Column(db.String(100), nullable=False)
    quantity_needed = db.Column(db.Integer, nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Shortage {self.hospital_name} - {self.supply_type}>'
