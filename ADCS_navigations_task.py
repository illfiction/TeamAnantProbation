import numpy as np
from datetime import datetime

#constants
DAYS_IN_YEAR = 365
RADIUS_EARTH = 6371
EARTH_ORBIT_RADIUS = 149598000
EARTH_AXIS_ANGLE = np.radians(23.5)
EARTH_ROTATION_PERIOD = 23*3600 + 56*60 + 4
EARTH_REVOLUTION_PERIOD = DAYS_IN_YEAR * 24 *3600 #seconds

def convert_time(date_str):

    date_format = "%b %d, %I%p, %Y"
    parsed_date = datetime.strptime(date_str, date_format)

    # Create a datetime object for March 20 of the same year
    march_20 = datetime(parsed_date.year, 3, 20,12)

    # Calculate the difference in days
    delta = parsed_date - march_20

    return delta.days*24*3600 + delta.seconds #seconds

def x_rotation_matrix(angle):
    return np.array([[1, 0, 0],
                     [0, np.cos(angle), -np.sin(angle)],
                     [0, np.sin(angle), np.cos(angle)]
                     ])

def y_rotation_matrix(angle):
    return np.array([[np.cos(angle), 0, np.sin(angle)],
                     [0, 1, 0],
                     [-np.sin(angle), 0, np.cos(angle)]
                     ])

def z_rotation_matrix(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle), np.cos(angle), 0],
                     [0, 0, 1]
                     ])

def ecef_to_eci(ecef_initial, converted_time):
    rotation_angle = 2*np.pi *converted_time/EARTH_REVOLUTION_PERIOD

    eci = np.dot(z_rotation_matrix(rotation_angle), ecef_initial)

    return eci

def axis_tilt(eci):
    rotation_angle = EARTH_AXIS_ANGLE

    coords = np.dot(x_rotation_matrix(rotation_angle), eci)

    return coords

def radial_vector_sun_earth(time):
    rotation_angle = 2*np.pi*time/EARTH_REVOLUTION_PERIOD
    vector = np.dot(z_rotation_matrix(rotation_angle),[-EARTH_ORBIT_RADIUS ,0 ,0])
    return vector

while True:
    user_input = input("Enter (1-3) for examples(1-3),4 for custom,0 for exit:")
    if user_input == "1" or user_input == "2" or user_input == "3" or user_input == "4":
        ECEF_input = "(6400, 1220, 1800)"
        if user_input == "1":
            time1 = "Dec 21, 10am, 2024"
            time2 = "Jun 21, 8pm, 2021"
        elif user_input == "2":
            time1 = "Jun 10, 10am, 2025"
            time2 = "Mar 21, 8pm, 2025"
        elif user_input == "3":
            time1 = "Dec 25, 5pm, 2025"
            time2 = "Jun 21, 10am, 2001"
        else:
            time1 = input("Time1:")
            ECEF_input = input("ECEF coordinates at Time 1:")
            time2 = input("Time2:")
    else:
        print("Bye bye......")
        break
    print(time1)
    print(ECEF_input)
    print(time2)

    converted_time1 = convert_time(time1)
    converted_time2 = convert_time(time2)

    initial_x, initial_y, initial_z = map(int, ECEF_input.strip("()").replace(" ", "").split(","))  # change
    ECEF_initial = np.array([initial_x, initial_y, initial_z])
    print("Initial  ",ECEF_initial)

    eci1 = ecef_to_eci(ECEF_initial, converted_time1)
    print("ECI1:    ", eci1)

    coords1 = axis_tilt(eci1)
    print("ECLIPTIC1:", coords1)

    radial_vector_earth_pos1 = radial_vector_sun_earth(converted_time1)
    radial_vector_earth_pos2 = radial_vector_sun_earth(converted_time2)

    print("R1:      ", radial_vector_earth_pos1)
    print("R2:      ", radial_vector_earth_pos2)

    coords2 = radial_vector_earth_pos2 + coords1 - radial_vector_earth_pos1
    print("ECLIPTIC2", coords2)

    eci2 = np.dot(x_rotation_matrix(-EARTH_AXIS_ANGLE), coords2)
    print("ECI2:    ", eci2)