import sqlite3
import csv

# Create a connection to SQLite database (pharmacy.db)
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Create MedicalStores table
cursor.execute('''
CREATE TABLE IF NOT EXISTS MedicalStores (
    MedicalStoreID INTEGER PRIMARY KEY,
    Name TEXT,
    Location TEXT,
    PinCode TEXT,
    ContactName TEXT,
    ContactNo TEXT
)
''')

# Create Supplies table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Supplies (
    SupplyID INTEGER PRIMARY KEY,
    SupplyName TEXT,
    Quantity INTEGER,
    ExpiryDate TEXT,
    MedicalStoreID INTEGER,
    FOREIGN KEY(MedicalStoreID) REFERENCES MedicalStores(MedicalStoreID)
)
''')

# Load data from CSV into MedicalStores table
medical_stores_file = 'MedicalStoresdata.csv'
with open(medical_stores_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
            INSERT INTO MedicalStores (MedicalStoreID, Name, Location, PinCode, ContactName, ContactNo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['MedicalStoreID'], row['Name'], row['Location'], row['PinCode'], row['ContactName'], row['ContactNo']))

# Load data from CSV into Supplies table
supplies_file = 'Suppliesdata.csv'
with open(supplies_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
            INSERT INTO Supplies (SupplyID, SupplyName, Quantity, ExpiryDate, MedicalStoreID)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['SupplyID'], row['SupplyName'], row['Quantity'], row['ExpiryDate'], row['MedicalStoreID']))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("pharmacy.db created and populated successfully.")
