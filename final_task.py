import sqlite3  # Import SQLite library for database operations
import math     # Import math library for calculations
import re       # Import regular expressions for validation
import sys      # Import sys for exiting the program

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    phi1 = math.radians(lat1)  # Convert latitude 1 to radians
    phi2 = math.radians(lat2)  # Convert latitude 2 to radians
    d_phi = math.radians(lat2 - lat1)  # Difference in latitude in radians
    d_lambda = math.radians(lon2 - lon1)  # Difference in longitude in radians
    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2  # Haversine formula part
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))  # Haversine formula part
    distance = R * c  # Calculate distance
    return distance

def validate_city_name(name):
    # Only English letters, spaces, hyphens, minimum 2 characters
    return bool(re.fullmatch(r"[A-Za-z \-]{2,}", name))

def validate_latitude(lat):
    try:
        lat = float(lat)  # Try to convert latitude to float
        return -90 <= lat <= 90  # Check if latitude is in valid range
    except ValueError:
        return False  # Return False if conversion fails

def validate_longitude(lon):
    try:
        lon = float(lon)  # Try to convert longitude to float
        return -180 <= lon <= 180  # Check if longitude is in valid range
    except ValueError:
        return False  # Return False if conversion fails

class Save_to_db:
    def __init__(self, db_path='city.db'):
        self.conn = sqlite3.connect(db_path)  # Connect to SQLite database
        self.cursor = self.conn.cursor()      # Create a cursor object
        self.create_tables()                  # Create tables if not exist

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CITY (
                CITY_ID integer PRIMARY KEY AUTOINCREMENT,
                CITY text UNIQUE,
                LAT real,
                LON real
            );
        ''')  # Create CITY table
        self.conn.commit()  # Commit changes

    def add_coordinates_to_db(self, city, lat, lon):
        self.cursor.execute('SELECT * FROM CITY WHERE UPPER(CITY)=UPPER(?)', (city,))  # Check if city exists
        result = self.cursor.fetchone()
        if not result:  # If city not found, add to database
            self.cursor.execute('INSERT INTO CITY (CITY, LAT, LON) VALUES (?, ?, ?)', (city, lat, lon))
            self.conn.commit()

    def fetch_coordinates(self, city):
        self.cursor.execute('SELECT LAT, LON FROM CITY WHERE UPPER(CITY)=UPPER(?)', (city,))  # Get coordinates for city
        result = self.cursor.fetchone()
        return result  # Return coordinates or None

    def close(self):
        self.conn.close()  # Close database connection

db = Save_to_db()  # Initialize database object

# Greetings
print('Hello, welcome in tool which will calculate straight-line distance between different cities based on coordinates.')
# Get and validate city A name
while True:
    city_A = input('Provide name of city A (ex. London or q to quit): ').strip()  # Ask for city A name
    if city_A.lower() == 'q':  # If user wants to quit
        print("Exiting program.")
        db.close()
        sys.exit()
    if validate_city_name(city_A):  # Validate city name
        break
    print("Invalid city name! Only letters, spaces and hyphens allowed.")

# Get and validate city B name
while True:
    city_B = input('Provide name of city B (ex. Paris or q to quit): ').strip()  # Ask for city B name
    if city_B.lower() == 'q':  # If user wants to quit
        print("Exiting program.")
        db.close()
        sys.exit()
    if validate_city_name(city_B):  # Validate city name
        break
    print("Invalid city name! Only letters, spaces and hyphens allowed.")

# Get and validate coordinates for city A
coords_A = db.fetch_coordinates(city_A)  # Try to fetch city A coordinates from database
if not coords_A:
    print(f"Coordinates for {city_A} not found.")
    while True:
        lat_A = input(f"Provide latitude for {city_A} (-90 to 90, or q to quit) in format 0.0000: ").strip()  # Ask for latitude
        if lat_A.lower() == 'q':
            print("Exiting program.")
            db.close()
            sys.exit()
        if validate_latitude(lat_A):  # Validate latitude
            lat_A = float(lat_A)
            break
        print("Invalid latitude! Must be a number between -90 and 90.")
    while True:
        lon_A = input(f"Provide longitude for {city_A} (-180 to 180, or q to quit) in format 0.0000: ").strip()  # Ask for longitude
        if lon_A.lower() == 'q':
            print("Exiting program.")
            db.close()
            sys.exit()
        if validate_longitude(lon_A):  # Validate longitude
            lon_A = float(lon_A)
            break
        print("Invalid longitude! Must be a number between -180 and 180.")
    db.add_coordinates_to_db(city_A, lat_A, lon_A)  # Save coordinates to database
    coords_A = (lat_A, lon_A)
else:
    lat_A, lon_A = coords_A  # Unpack coordinates

# Get and validate coordinates for city B
coords_B = db.fetch_coordinates(city_B)  # Try to fetch city B coordinates from database
if not coords_B:
    print(f"Coordinates for {city_B} not found.")
    while True:
        lat_B = input(f"Provide latitude for {city_B} (-90 to 90, or q to quit) in format 0.0000: ").strip()  # Ask for latitude
        if lat_B.lower() == 'q':
            print("Exiting program.")
            db.close()
            sys.exit()
        if validate_latitude(lat_B):  # Validate latitude
            lat_B = float(lat_B)
            break
        print("Invalid latitude! Must be a number between -90 and 90.")
    while True:
        lon_B = input(f"Provide longitude for {city_B} (-180 to 180, or q to quit) in format 0.0000: ").strip()  # Ask for longitude
        if lon_B.lower() == 'q':
            print("Exiting program.")
            db.close()
            sys.exit()
        if validate_longitude(lon_B):  # Validate longitude
            lon_B = float(lon_B)
            break
        print("Invalid longitude! Must be a number between -180 and 180.")
    db.add_coordinates_to_db(city_B, lat_B, lon_B)  # Save coordinates to database
    coords_B = (lat_B, lon_B)
else:
    lat_B, lon_B = coords_B  # Unpack coordinates

# Calculate and print distance
distance = calculate_distance(lat_A, lon_A, lat_B, lon_B)  # Calculate distance between cities
print(f"Distance between {city_A} and {city_B}: {distance:.2f} km")  # Print result

db.close()  # Close database connection