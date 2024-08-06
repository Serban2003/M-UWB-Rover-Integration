# Import necessary libraries
from adafruit_servokit import ServoKit

# Pulse width range global parameters
servo180_1 = 535
servo180_2 = 2590

# Speed global parameters
stopSpeed = 0.03
maxSpeed = 1

# Angle global parameters
maxAngle = 180
minAngle = 0
neutralAngle = 90

# Direction global parameters
forwardDirection = 1
backwardDirection = -1
noDirection = 0

# Create the kit object of the ServoKit class from the Adafruit library
kit = ServoKit(channels=16)

# Set PWM range for each 180 motor
for i in range(6, 12):
    kit.servo[i].set_pulse_width_range(servo180_1, servo180_2)


# Create the Joint class. It will be used to control
# each 2 motors(one 180 and one 360) of the 6 joints of the rover
class Joint:

    # Constructor
    def __init__(self, id360, id180, angle=None, speed=None, direction=None):

        if id360 < 0 or id360 > 5:
            raise Exception("id360 must be between 0-5")
        else:
            self._id360 = id360  # private argument

        if id180 < 6 or id180 > 11:
            raise Exception("id180 must be between 6-11")
        else:
            self._id180 = id180  # private argument

        if angle is None:
            angle = []
        elif angle < minAngle or angle > maxAngle:
            raise Exception("Angle must be between 0-180")
        self.angle = neutralAngle  # public argument, default is neutralAngle(globally defined as 90)

        if speed is None:
            speed = []
        elif speed < stopSpeed or speed > maxSpeed:
            raise Exception("Speed must be between 0.03 and 1")
        self.speed = stopSpeed  # public argument, default is stopSpeed (globally defined as 0.03)

        if direction is None:
            direction = []
        elif direction != backwardDirection and direction != forwardDirection and direction != noDirection:
            raise Exception("Direction must be 0, -1 or 1")
        self.direction = noDirection  # public argument, default is noDirection (globally defined as 0)

    # Function for printing the objects
    def __str__(self):
        return f"{self.angle}, {self.speed}, {self.direction}"

    # Move function, with angle, speed and direction as parameters
    def Move(self, angle, speed, direction):

        if angle < minAngle or angle > maxAngle:
            raise Exception("Angle must be between 0-180")
        else:
            self.angle = angle

        if speed < stopSpeed or speed > maxSpeed:
            raise Exception("Speed must be between 0.03 and 1")
        else:
            self.speed = speed

        if direction != backwardDirection and direction != forwardDirection and direction != noDirection:
            raise Exception("Direction must be 0, -1 or 1")
        elif self._id360 in [0, 2, 4]:  # correction for the left-side 360 motors
            direction = direction * (-1)
        else:
            self.direction = direction

        kit.servo[self._id180].angle = angle

        if speed == stopSpeed:
            kit.continuous_servo[self._id360].throttle = stopSpeed
        else:
            kit.continuous_servo[self._id360].throttle = speed * direction

    # Stop function sets the throttle speed to stopSpeed(globally declared as 0.03)
    def Stop(self):
        kit.continuous_servo[self._id360].throttle = stopSpeed


class Rover:
    def __init__(self, FLJ_obj, FRJ_obj, MLJ_obj, MRJ_obj, RLJ_obj, RRJ_obj):
        self.FLJ_obj = FLJ_obj
        self.FRJ_obj = FRJ_obj
        self.MLJ_obj = MLJ_obj
        self.MRJ_obj = MRJ_obj
        self.RLJ_obj = RLJ_obj
        self.RRJ_obj = RRJ_obj

    def Move_forward(self, angle):
        self.FLJ_obj.Move(int(angle), maxSpeed, forwardDirection)
        self.FRJ_obj.Move(int(angle), maxSpeed, forwardDirection)
        self.MLJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
        self.MRJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
        self.RLJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
        self.RRJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
        return "Moving forward"

    def Move_backward(self, angle):
        self.FLJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
        self.FRJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
        self.MLJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
        self.MRJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
        self.RLJ_obj.Move(int(180 - angle), maxSpeed, backwardDirection)
        self.RRJ_obj.Move(int(180 - angle), maxSpeed, backwardDirection)
        return "Moving backward"


    def Stop_rover(self):
        self.FLJ_obj.Move(neutralAngle, stopSpeed, noDirection)
        self.FRJ_obj.Move(neutralAngle, stopSpeed, noDirection)
        self.MLJ_obj.Move(neutralAngle, stopSpeed, noDirection)
        self.MRJ_obj.Move(neutralAngle, stopSpeed, noDirection)
        self.RLJ_obj.Move(neutralAngle, stopSpeed, noDirection)
        self.RRJ_obj.Move(neutralAngle, stopSpeed, noDirection)
        return "Stopped"


    def Crab_walk(self, direction):
        self.FLJ_obj.Move(maxAngle, maxSpeed, direction)
        self.FRJ_obj.Move(maxAngle, maxSpeed, direction)
        self.MLJ_obj.Move(maxAngle, maxSpeed, direction)
        self.MRJ_obj.Move(maxAngle, maxSpeed, direction)
        self.RLJ_obj.Move(maxAngle, maxSpeed, direction)
        self.RRJ_obj.Move(maxAngle, maxSpeed, direction)



