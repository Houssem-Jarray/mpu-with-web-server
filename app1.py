from flask import Flask, jsonify, send_from_directory
from mpu6050 import mpu6050

app = Flask(__name__)

# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)

# Capture initial offsets (assuming values at start are zero)
initial_accel_data = sensor.get_accel_data()
initial_gyro_data = sensor.get_gyro_data()

initial_offsets = {
    'pitch': initial_accel_data['x'] / 10,
    'roll': initial_accel_data['y'] / 10,
    'yaw': initial_accel_data['z'] / 10,
}

def get_orientation():
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()

    # Compute pitch, roll, and yaw based on accelerometer data
    pitch = accel_data['x'] / 10 - initial_offsets['pitch']
    roll = accel_data['y'] / 10 - initial_offsets['roll']
    yaw = accel_data['z'] / 10 - initial_offsets['yaw']

    return {'pitch': pitch, 'roll': roll, 'yaw': yaw}

@app.route('/orientation')
def orientation():
    return jsonify(get_orientation())

@app.route('/')
def index():
    return send_from_directory('', 'page1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
