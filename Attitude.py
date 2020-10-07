from Classes import Data, Attitude
import configparser
import serial
import time


# Unit test
def unit_test():
    measurement = Data([900, 902, 0, 5, 880, 890, 950, 952, 1000, 1012, 20, 25])

    # Return the averaged, calibrated and sorted dominant values
    sorted_data = measurement.sorted()
    print('Dominant Side Proccessed Data: ', sorted_data)

    # Return incidence angles for the three dominant sides
    incidence_data = Attitude(sorted_data).incidence_angles()
    print('Dominant Side Incidence Angles: ', incidence_data)


# Communicate with serial port
config = configparser.ConfigParser()
config.read('calibration.ini')
ser = serial.Serial(config.get('settings', 'com_port'), 9600)

running = True
listening = True
counter = 0
moving_average_period = 10
stored_data = []

# While attitude determination is required
while running:

    # Listen to serial port until dataset delimiter ',' is detected
    while listening:
        output = ser.readline()
        if output == b',\r\n':

            # Dataset delimiter detected, run interrupt to determine attitude
            listening = False

    # Read all sensor values from the serial port
    A0 = int(ser.readline())
    A1 = int(ser.readline())
    A2 = int(ser.readline())
    A3 = int(ser.readline())
    A4 = int(ser.readline())
    A5 = int(ser.readline())
    A6 = int(ser.readline())
    A7 = int(ser.readline())
    A8 = int(ser.readline())
    A9 = int(ser.readline())
    A10 = int(ser.readline())
    A11 = int(ser.readline())

    # Save data into required format and instantiate Data class
    raw_data = [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11]
    measurement = Data(raw_data)

    # calibrate, average and sort data
    sorted_data = measurement.sorted()

    # Request incidence angle by instantiating Attitude class
    sun_vector = Attitude(sorted_data).unit_vector()

    # Add data to temporary storage and move counter
    counter += 1

    if len(stored_data) < moving_average_period:
        stored_data.append(sun_vector)

    elif len(stored_data) >= moving_average_period:
        stored_data.pop(0)                  # remove oldest value
        stored_data.append(sun_vector)      # add newest value

    # if counter is not yet above threshold, use singular value
    if counter < moving_average_period:
        averaged_sun_vector = stored_data[-1]

    # if counter is above threshold, apply moving average
    elif counter >= moving_average_period:
        summed_data = [0, 0, 0]

        # Sum all of the parameters and store them in summed_data
        for i in stored_data:
            summed_data[0] += i[0]
            summed_data[1] += i[1]
            summed_data[2] += i[2]

        # Add averages to the averaged sun vector
        averaged_sun_vector = [(summed_data[0] / 10),
                               (summed_data[1] / 10),
                               (summed_data[2] / 10)
                               ]

    print('Dominant incidence angles: ', averaged_sun_vector)
    print('')

    listening = True
    time.sleep(0.5)

