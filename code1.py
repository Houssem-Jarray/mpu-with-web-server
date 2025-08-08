from flask import Flask, jsonify, send_from_directory
from mpu6050 import mpu6050
import time
import math

app = Flask(__name__)

# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)

# Initial orientation and complementary filter factor
last_pitch = 0
last_roll = 0
last_yaw = 0
alpha = 0.98  # Complementary filter coefficient
dt = 0.05     # Time delta between readings (in seconds)

def get_orientation():
    global last_pitch, last_roll, last_yaw

    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()

    # Compute pitch, roll from accelerometer
    accel_pitch = math.atan2(accel_data['y'], math.sqrt(accel_data['x']**2 + accel_data['z']**2)) * 180 / math.pi
    accel_roll = math.atan2(-accel_data['x'], accel_data['z']) * 180 / math.pi
    
    # Integrate gyroscope data to get yaw (drift-prone, so handled separately)
    gyro_yaw = last_yaw + gyro_data['z'] * dt

    # Complementary filter to combine accelerometer and gyroscope data
    pitch = alpha * (last_pitch + gyro_data['x'] * dt) + (1 - alpha) * accel_pitch
    roll = alpha * (last_roll + gyro_data['y'] * dt) + (1 - alpha) * accel_roll

    # Update last values for the next iteration
    last_pitch, last_roll, last_yaw = pitch, roll, gyro_yaw

    return {'pitch': pitch, 'roll': roll, 'yaw': gyro_yaw}

@app.route('/orientation')
def orientation():
    return jsonify(get_orientation())

@app.route('/')
def index():
    return send_from_directory('', 'index1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
