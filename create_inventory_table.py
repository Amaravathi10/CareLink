import sqlite3
import csv

# Create a connection to SQLite database (pharmacy.db)
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Create Inventory table with all columns as TEXT
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    StoreName TEXT NOT NULL,
    Location TEXT NOT NULL,
    PinCode TEXT NOT NULL,
    ContactName TEXT NOT NULL,
    ContactNo TEXT NOT NULL,
    SupplyID TEXT PRIMARY KEY,
    SupplyName TEXT NOT NULL,
    Quantity TEXT NOT NULL,
    ExpiryDate TEXT NOT NULL,
    Status TEXT NOT NULL DEFAULT 'Active'
)
''')

# Load data from CSV into Inventory table
inventory_file = 'inventory.csv'
with open(inventory_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            # Insert data into the inventory table
            cursor.execute('''
                INSERT INTO inventory (StoreName, Location, PinCode, ContactName, ContactNo, SupplyID, SupplyName, Quantity, ExpiryDate, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Store Name'],
                row['Location'],
                row['Pin Code'],
                row['Contact Name'],
                row['Contact No'],
                row['Supply ID'],  # Store SupplyID as TEXT
                row['Supply Name'],
                row['Quantity'],   # Store Quantity as TEXT
                row['Expiry Date'],
                row.get('Status', 'Active')  # Default to 'Pending' if 'Status' is missing
            ))
        except KeyError as e:
            print(f"Missing field in row {row}: {e}")

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Inventory table created and populated successfully with TEXT columns.")
