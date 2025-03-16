import numpy as np
import matplotlib.pyplot as plt

angular_velocity = 1 #rad/s
radius = 15 # m
theta = 0
dt = 0.2

mean_angular_velocity_noise = 0
variance_angular_velocity_noise = 0.25

mean_coordinates_noise = 0
variance_coordinates_noise = 1

time = np.arange(0,20+dt,dt)

x_coordinate = 15
y_coordinate = 0

angular_velocity_list = []
x_coordinate_list = []
y_coordinate_list = []
x_true_list = []
y_true_list = []
theta_list = []

for t in time:
    x_coordinate_list.append(x_coordinate)
    y_coordinate_list.append(y_coordinate)
    noise_angular_velocity = angular_velocity + np.random.normal(mean_angular_velocity_noise,variance_angular_velocity_noise**0.5)
    theta = theta + noise_angular_velocity*dt
    x_true = radius*np.cos(theta)
    y_true = radius*np.sin(theta)
    x_coordinate = x_true + np.random.normal(mean_coordinates_noise,variance_coordinates_noise**0.5)
    y_coordinate = y_true + np.random.normal(mean_coordinates_noise,variance_coordinates_noise**0.5)
    angular_velocity_list.append(noise_angular_velocity)
    theta_list.append(theta)
    x_true_list.append(x_true)
    y_true_list.append(y_true)

plt.figure(figsize=(10, 5))
plt.subplot(3, 1, 1)
plt.plot(time, x_coordinate_list, label='x_coordinate')
plt.xlabel('Time (s)')
plt.ylabel('x')
plt.legend()
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(time, angular_velocity_list, label='Angle')
plt.axhline(y=angular_velocity, color='r', linestyle='--', label='angular velocity')
plt.xlabel('Time (s)')
plt.ylabel('radians per sec')
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(time, y_coordinate_list, label='y_coordinate')
plt.xlabel('Time (s)')
plt.ylabel('y')
plt.grid()


plt.figure(figsize=(10, 10))
plt.plot(x_coordinate_list, y_coordinate_list,color='red',label='Noisy GPS Coordinates')
plt.plot(x_true_list, y_true_list, label='True values',color = 'green')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.grid()


plt.tight_layout()
plt.show()