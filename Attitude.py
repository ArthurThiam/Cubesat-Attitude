from math import cos, acos, pi
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

    # determine incidence angles for three dominant sides
    def incidence_angles(self):
        max_range_values = self.max_values()

        incidence_angles = [
            (self.processed_data[0][0], acos(self.processed_data[0][1]/max_range_values[self.processed_data[0][0]])
             * 180 / pi),
            (self.processed_data[1][0], acos(self.processed_data[1][1]/max_range_values[self.processed_data[1][0]])
             * 180 / pi),
            (self.processed_data[2][0], acos(self.processed_data[2][1]/max_range_values[self.processed_data[2][0]])
             * 180 / pi)
        ]

        return incidence_angles

    # Method to derive unit vector from incidence angle data
    def unit_vector(self):
        incidence_data = self.incidence_angles()

        # Initialize unit vector components
        unit_component_1 = -1
        unit_component_2 = -1
        unit_component_3 = -1

        # Loop through incidence angles and associate with unit vector components.
        for i in incidence_data:
            if i[0] == 'x+':
                unit_component_1 = cos(i[1] * pi / 180)

            elif i[0] == 'x-':
                unit_component_1 = cos(i[1] * pi / 180 - pi)

            elif i[0] == 'y+':
                unit_component_2 = cos(i[1] * pi / 180)

            elif i[0] == 'y-':
                unit_component_2 = cos(i[1] * pi / 180 - pi)

            elif i[0] == 'z+':
                unit_component_3 = cos(i[1] * pi / 180)

            elif i[0] == 'z-':
                unit_component_3 = cos(i[1] * pi / 180 - pi)

        unit_vector = [unit_component_1, unit_component_2, unit_component_3]
        return unit_vector