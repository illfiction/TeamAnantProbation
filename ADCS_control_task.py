import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.integral = 0
        self.previous_error = 0

    def compute (self, target_angle, current_angle):
        error = target_angle - current_angle
        self.integral += error * self.dt
        derivative = (error - self.previous_error)/self.dt
        self.previous_error = error

        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative


wheel_mass = 1 #kg
wheel_radius = 0.5 #m
plate_mass = 1 #kg
plate_length = np.sqrt(6) #m

I_wheel = 0.5 * wheel_mass * (wheel_radius ** 2)
I_plate = (plate_mass * (plate_length ** 2))/6
I_net = I_wheel + I_plate

k = 0 #torsional spring const
b = 0 # frictional torque
dt = 0.1 #interval


##CHANGE THESE VALUES FOR TUNING
Kp = 21.2897251220628
Ki = 15.3897712451248
Kd = 6.99148336114352
target_angle = input("Please enter the target angle: ")
target_angle = float(target_angle)

time = np.arange(0,20,dt) #setting intervals of time
angular_velocity = 0 #initially
angle = 0 #initially
controller = PIDController(Kp, Ki, Kd, dt)

angular_velocity_list = []
angles_list = []
print("something worked")

for t in time:
    input_toque = controller.compute(target_angle,angle)
    angle = (angle + 180) % 360 - 180 # sets domain of angle [-180,180]
    frictional_torque = - b * angular_velocity 
    spring_torque = - k * angle
    net_torque = frictional_torque + spring_torque + input_toque
    angular_acceleration = net_torque/I_net
    angular_velocity += angular_acceleration*dt
    angle += angular_velocity*dt
    angle = (angle + 180) % 360 - 180 # sets domain of angle [-180,180]
    angular_velocity_list.append(angular_velocity)
    angles_list.append(angle)
    print("working")

print(angles_list)

plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(time, angles_list)
plt.axhline(y=target_angle, color='r', linestyle='--', label='Target Angle')
plt.xlabel('Time (s)')
plt.ylabel('radians')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(time, angular_velocity_list, label='Angle')
plt.xlabel('Time (s)')
plt.ylabel('radians per sec')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()