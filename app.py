
from flask import Flask, jsonify, send_from_directory
from mpu6050 import mpu6050

app = Flask(__name__)

# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)

def get_orientation():
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()

    # Compute pitch, roll, and yaw based on accelerometer data
    pitch = accel_data['x'] / 10
    roll = accel_data['y'] / 10
    yaw = accel_data['z'] / 10

    return {'pitch': pitch, 'roll': roll, 'yaw': yaw}

@app.route('/orientation')
def orientation():
    return jsonify(get_orientation())

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
