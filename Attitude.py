from math import sin, asin, pi
import configparser


class Attitude:

    def __init__(self, processed_data):
        self.processed_data = processed_data

    # Read max calibration values
    @staticmethod
    def max_values():
        config = configparser.ConfigParser()
        config.read('calibration.ini')

        # average of the max values of sensor pairs
        max_values = {
            "x+": (config.getint('settings', 'A10_max') + config.getint('settings', 'A11_max')) / 2,
            "x-": (config.getint('settings', 'A6_max') + config.getint('settings', 'A7_max')) / 2,

            "y+": (config.getint('settings', 'A2_max') + config.getint('settings', 'A3_max')) / 2,
            "y-": (config.getint('settings', 'A4_max') + config.getint('settings', 'A5_max')) / 2,

            "z+": (config.getint('settings', 'A8_max') + config.getint('settings', 'A9_max')) / 2,
            "z-": (config.getint('settings', 'A0_max') + config.getint('settings', 'A1_max')) / 2
        }

        return max_values

    def remove_low_ldr(self):
        config = configparser.ConfigParser()
        config.read('calibration.ini')
        data = self.processed_data
        iterator = 0

        # if readout value is too low, set value to 0
        for i in data:
            if i[1] < config.getint('settings', 'detection_threshold'):
                data[iterator] = (i[0], 0)

            iterator += 1

        print('remove low ldr return: ', data)
        return data

    # determine incidence angles for three dominant sides
    def incidence_angles(self):
        low_ldr_data = self.remove_low_ldr()

        # Check how many 0 vectors there are:
        counter = 0
        for i in low_ldr_data:
            if i[1] == 0:
                counter += 1


        if counter == 0:
            incidence_angles = [
                (low_ldr_data[0][0], asin(low_ldr_data[0][1]/1023)
                 * 180 / pi),
                (low_ldr_data[1][0], asin(low_ldr_data[1][1]/1023)
                 * 180 / pi),
                (low_ldr_data[2][0], asin(low_ldr_data[2][1]/1023)
                 * 180 / pi)
            ]

        elif counter == 1:
            incidence_angles = [
                (low_ldr_data[0][0], asin(low_ldr_data[0][1] / 1023)
                 * 180 / pi),
                (low_ldr_data[1][0], asin(low_ldr_data[1][1] / 1023)
                 * 180 / pi),
                ('', 0)
            ]

        elif counter == 2:
            incidence_angles = [
                (low_ldr_data[0][0], asin(low_ldr_data[0][1] / 1023)
                 * 180 / pi),
                ('', 0),
                ('', 0)
            ]

        else:
            incidence_angles = [
                ('', 0),
                ('', 0),
                ('', 0)
            ]

        return incidence_angles

    # Method to derive unit vector from incidence angle data
    def vector(self):
        incidence_data = self.incidence_angles()
        print('incidence_data: ', incidence_data)

        # Initialize unit vector components
        unit_component_1 = 0
        unit_component_2 = 0
        unit_component_3 = 0

        for i in incidence_data:
            if i[0] == 'x+':
                unit_component_1 = sin(i[1] * pi / 180)

            elif i[0] == 'x-':
                unit_component_1 = sin(i[1] * pi / 180 - pi)

            elif i[0] == 'y+':
                unit_component_2 = sin(i[1] * pi / 180)

            elif i[0] == 'y-':
                unit_component_2 = sin(i[1] * pi / 180 - pi)

            elif i[0] == 'z+':
                unit_component_3 = sin(i[1] * pi / 180)

            elif i[0] == 'z-':
                unit_component_3 = sin(i[1] * pi / 180 - pi)

        vector = [unit_component_1, unit_component_2, unit_component_3]
        print('vector return: ', vector)
        return vector
