import os
from flask import Flask, render_template, request, jsonify, Response
from RoverOOP import Rover, Joint
import cv2
from picamera2 import Picamera2
# from motion import Motion

# Initialize the camera
try:
    camera = Picamera2()
    camera.preview_configuration.main.format = "RGB888"
    camera.start()
    camera_available = True
except Exception as e:
    print("Error initializing camera:", e)
    camera_available = False

FLJ = Joint(0, 6)  # Front Left Joint
FRJ = Joint(1, 7)  # Front Right Joint
MLJ = Joint(2, 8)  # Middle Left Joint
MRJ = Joint(3, 9)  # Middle Right Joint
RLJ = Joint(4, 10)  # Rear Left Joint
RRJ = Joint(5, 11)  # Rear Right Joint

# Create the Rover object, having as arguments the 6 Joint objects
Rover_obj = Rover(FLJ, FRJ, MLJ, MRJ, RLJ, RRJ)

app = Flask(__name__)

"""
Part of the code from Antonia S.,
its script being motion.py

# Constants for calibrating the camera 
KNOWN_WIDTH = 100
FOCAL_LENGTH = 60

motion = Motion(camera, KNOWN_WIDTH, FOCAL_LENGTH, Rover_obj)
"""

def generate_frames():
    while True:
        try:
            frame = camera.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Error capturing frame:", e)
            
def shutdown_raspberry():
    os.system("sudo shutdown -h now")
    return jsonify({'status': 'Raspberry Pi shutting down...'})

@app.route('/video_feed')
def video_feed():
    if camera_available:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return app.send_static_file('no_image.png')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    if direction == 'forward':
        Rover_obj.Move_forward(90)
        return jsonify({'status': 'Moved forward'})
    elif direction == 'backward':
        Rover_obj.Move_backward(90)
        return jsonify({'status': 'Moved backward'})
    elif direction == 'left':
        Rover_obj.Move_forward(45)
        return jsonify({'status': 'Moved left'})
    elif direction == 'right':
        Rover_obj.Move_forward(135)
        return jsonify({'status': 'Moved right'})
    elif direction == 'stop':
        Rover_obj.Stop_rover()
        return jsonify({'status': 'Stopped rover'})
    else:
        return jsonify({'status': 'Invalid direction'})
        
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_raspberry()
    return jsonify({'status': 'Shutting down Raspberry Pi'})

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=False, use_reloader=False)
