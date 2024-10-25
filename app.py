from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure the SQLAlchemy database (you can change the connection string as needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the sensor readings model
class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aqi = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    tvoc_mg_m3 = db.Column(db.Float, nullable=False)
    eco2 = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    location = db.Column(db.Text , nullable=False)

# Create the database (only needs to be done once)
with app.app_context():
    if not os.path.exists('sensor_data.db'):
        db.create_all()

@app.route('/get_data_api', methods=['POST'])
def get_data():
    if request.is_json:
        data = request.get_json()  # Parse JSON data
        # Access the sensor data sent by Arduino
        id = data.get('id')
        aqi = data.get('aqi')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        tvoc_mg_m3 = data.get('tvoc_mg_m3')
        eco2 = data.get('eco2')
        location = data.get('location')
        timestamp = datetime.now()

        # Print the data to check if it was received correctly
        print(f"Received AQI: {aqi}")
        print(f"Received Temperature: {temperature}")
        print(f"Received Humidity: {humidity}")
        print(f"Received TVOC (mg/m³): {tvoc_mg_m3}")
        print(f"Received eCO2: {eco2}")
        print(f"Received Location: {location}")

        # Store the sensor reading in the database

        new_reading = SensorReading(
            id=id,
            aqi=aqi,
            temperature=temperature,
            humidity=humidity,
            tvoc_mg_m3=tvoc_mg_m3,
            eco2=eco2,
            location=location,
            timestamp=timestamp
        )
        db.session.add(new_reading)
        db.session.commit()

        # Respond with a success message
        return jsonify({"message": "Data received and saved successfully"}), 200
    else:
        return jsonify({"error": "Invalid data format. Expected JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
