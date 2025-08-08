from flask import Flask, jsonify, send_from_directory
from mpu6050 import mpu6050
import time
import math

app = Flask(__name__)

# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)

# Calibration and filter settings
GYRO_SENSITIVITY = 131.0  # Sensitivity for gyro (for 250dps)
ACCEL_SENSITIVITY = 16384.0  # Sensitivity for accel (for 2g)
alpha = 0.98  # Complementary filter constant
prev_time = time.time()

# Initialize pitch, roll, and yaw angles
pitch = 0
roll = 0
yaw = 0

def get_orientation():
    global pitch, roll, yaw, prev_time
    
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    
    # Time difference (dt) for integration
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    
    # Accelerometer angles (based on gravity)
    accel_pitch = math.atan2(accel_data['y'], accel_data['z']) * 180 / math.pi
    accel_roll = math.atan2(accel_data['x'], accel_data['z']) * 180 / math.pi

    # Gyroscope angular velocity in degrees/second
    gyro_pitch = gyro_data['x'] / GYRO_SENSITIVITY
    gyro_roll = gyro_data['y'] / GYRO_SENSITIVITY
    gyro_yaw = gyro_data['z'] / GYRO_SENSITIVITY

    # Integrate gyro angles
    pitch += gyro_pitch * dt
    roll += gyro_roll * dt
    yaw += gyro_yaw * dt

    # Complementary filter to combine gyro and accel data
    pitch = alpha * (pitch) + (1 - alpha) * accel_pitch
    roll = alpha * (roll) + (1 - alpha) * accel_roll

    return {'pitch': pitch, 'roll': roll, 'yaw': yaw}

@app.route('/orientation')
def orientation():
    return jsonify(get_orientation())

@app.route('/')
def index():
    return send_from_directory('', 'index1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
