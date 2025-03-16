import numpy as np
import matplotlib.pyplot as plt

from ADCS_estimations_task import time,dt,x_coordinate_list,y_coordinate_list,variance_coordinates_noise

def radius(at_time):
    x_position = x_coordinate_list[at_time]
    y_position = y_coordinate_list[at_time]
    rad = np.sqrt(x_position**2 + y_position**2)
    return rad      #function to define radius at specific time

mistake_theta_list = np.arctan2(y_coordinate_list,x_coordinate_list)
print(mistake_theta_list)
theta_list = []
count = 0

for i in range(101):
    if i != 0:
        # print(i)
        if mistake_theta_list[i-1] - mistake_theta_list[i] > np.pi:
            count += 1
            print(i)
    temp = mistake_theta_list[i] + 2*count*np.pi
    theta_list.append(temp)

angular_velocity_list = []

# print(range(len(time)))
for i in range(len(time)):
    # print(i)
    if i < 100:
        angular_velocity = (theta_list[i+1] - theta_list[i])/dt
        angular_velocity_list.append(angular_velocity)
    else :
        angular_velocity = 1
        angular_velocity_list.append(angular_velocity)

print("output w     ",angular_velocity_list)
print("output angle ",theta_list)


x_kalman_estimates = []
y_kalman_estimates = []
angle_est = 0
P = 1
R = variance_coordinates_noise

angle_est_list = []

for i in range(len(time)):
    # print(i)
    angle_pred = angle_est + angular_velocity_list[i]*dt

    K = P / (P + R)

    angle_est = angle_pred + K*(theta_list[i] - angle_pred)
    P = (1 - K)*P

    x_kalman_estimates.append(radius(i)*np.cos(angle_est))
    y_kalman_estimates.append(radius(i)*np.sin(angle_est))
    angle_est_list.append(angle_est)

print(x_kalman_estimates)
print(y_kalman_estimates)
print(angle_est_list)

plt.figure(figsize=(8,8))

plt.plot(x_kalman_estimates, y_kalman_estimates, label='1D Kalman Filter')
plt.scatter(x_coordinate_list, y_coordinate_list, label='Noisy GPS Coordinates', color='red',s = 10)

plt.title('Pranav\'s Circular Motion with Filters')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()