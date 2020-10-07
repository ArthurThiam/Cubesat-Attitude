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

while running:
    while listening:
        output = ser.readline()
        if output == b',\r\n':
            listening = False

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

    raw_data = [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11]
    measurement = Data(raw_data)
    sorted_data = measurement.sorted()
    incidence_data = Attitude(sorted_data).incidence_angles()
    print('Dominant incidence angles: ', incidence_data)
    print('')

    listening = True
    time.sleep(1)

