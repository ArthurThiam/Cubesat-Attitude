from math import cos, acos, pi
import configparser


class Data:

    def __init__(self, data):
        self.data = data

    # Read range calibration data
    @staticmethod
    def calibration():
        config = configparser.ConfigParser()
        config.read('calibration.ini')

        ranges = {
            "A0": config.getint('settings', 'A0_max') - config.getint('settings', 'A0_min'),
            "A1": config.getint('settings', 'A1_max') - config.getint('settings', 'A1_min'),
            "A2": config.getint('settings', 'A2_max') - config.getint('settings', 'A2_min'),
            "A3": config.getint('settings', 'A3_max') - config.getint('settings', 'A3_min'),
            "A4": config.getint('settings', 'A4_max') - config.getint('settings', 'A4_min'),
            "A5": config.getint('settings', 'A5_max') - config.getint('settings', 'A5_min'),
            "A6": config.getint('settings', 'A6_max') - config.getint('settings', 'A6_min'),
            "A7": config.getint('settings', 'A7_max') - config.getint('settings', 'A7_min'),
            "A8": config.getint('settings', 'A8_max') - config.getint('settings', 'A8_min'),
            "A9": config.getint('settings', 'A9_max') - config.getint('settings', 'A9_min'),
            "A10": config.getint('settings', 'A10_max') - config.getint('settings', 'A10_min'),
            "A11": config.getint('settings', 'A11_max') - config.getint('settings', 'A11_min')
        }
        
        range_minima = {
            "A0": config.getint('settings', 'A0_min'),
            "A1": config.getint('settings', 'A0_min'),
            "A2": config.getint('settings', 'A0_min'),
            "A3": config.getint('settings', 'A0_min'),
            "A4": config.getint('settings', 'A0_min'),
            "A5": config.getint('settings', 'A0_min'),
            "A6": config.getint('settings', 'A0_min'),
            "A7": config.getint('settings', 'A0_min'),
            "A8": config.getint('settings', 'A0_min'),
            "A9": config.getint('settings', 'A0_min'),
            "A10": config.getint('settings', 'A0_min'),
            "A11": config.getint('settings', 'A0_min')
        }
        
        calibration_data = [ranges, range_minima]
        return calibration_data
    
    # Apply range calibration for each sensor
    def calibrated(self):
        calibration_ranges = self.calibration()[0]
        calibration_minima = self.calibration()[1]

        calibrated_data = {
            "A0": (self.data[0] - calibration_minima["A0"]) / calibration_ranges["A0"] * 1023,
            "A1": (self.data[1] - calibration_minima["A1"]) / calibration_ranges["A1"] * 1023,
            "A2": (self.data[2] - calibration_minima["A2"]) / calibration_ranges["A2"] * 1023,
            "A3": (self.data[3] - calibration_minima["A3"]) / calibration_ranges["A3"] * 1023,
            "A4": (self.data[4] - calibration_minima["A4"]) / calibration_ranges["A4"] * 1023,
            "A5": (self.data[5] - calibration_minima["A5"]) / calibration_ranges["A5"] * 1023,
            "A6": (self.data[6] - calibration_minima["A6"]) / calibration_ranges["A6"] * 1023,
            "A7": (self.data[7] - calibration_minima["A7"]) / calibration_ranges["A7"] * 1023,
            "A8": (self.data[8] - calibration_minima["A8"]) / calibration_ranges["A8"] * 1023,
            "A9": (self.data[9] - calibration_minima["A9"]) / calibration_ranges["A9"] * 1023,
            "A10": (self.data[10] - calibration_minima["A10"]) / calibration_ranges["A10"] * 1023,
            "A11": (self.data[11] - calibration_minima["A11"]) / calibration_ranges["A11"] * 1023
        }

        return calibrated_data

    # average sensor values and associate to correct face
    def averaged(self):

        avg_data = {
            "x+": 0.5 * (self.calibrated()["A10"] + self.calibrated()["A11"]),
            "x-": 0.5 * (self.calibrated()["A6"] + self.calibrated()["A7"]),
            "y+": 0.5 * (self.calibrated()["A2"] + self.calibrated()["A3"]),
            "y-": 0.5 * (self.calibrated()["A4"] + self.calibrated()["A5"]),
            "z+": 0.5 * (self.calibrated()["A8"] + self.calibrated()["A9"]),
            "z-": 0.5 * (self.calibrated()["A0"] + self.calibrated()["A1"])
        }

        return avg_data

    # Sort the data to return the three largest values and their corresponding face
    def sorted(self):
        data_items = list(self.averaged().items())
        ordered_data = []

        # iterate through all data_items, add the maximum to ordered_data, and remove it from the data_items list
        for i in range(0, 3):
            max = -1
            max_idx = 0

            for j in range(len(data_items)):
                if data_items[j][1] > max:
                    max = data_items[j][1]
                    max_idx = j

            ordered_data.append((data_items[max_idx][0], data_items[max_idx][1]))
            data_items.pop(max_idx)

        return ordered_data


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
            (self.processed_data[0][0], 90 - acos(self.processed_data[0][1]/max_range_values[self.processed_data[0][0]])
             * 180 / pi),
            (self.processed_data[1][0], 90 - acos(self.processed_data[1][1]/max_range_values[self.processed_data[1][0]])
             * 180 / pi),
            (self.processed_data[2][0], 90 - acos(self.processed_data[2][1]/max_range_values[self.processed_data[2][0]])
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
                unit_component_1 = pi - cos(i[1] * pi / 180)

            elif i[0] == 'y+':
                unit_component_2 = cos(i[1] * pi / 180)

            elif i[0] == 'y-':
                unit_component_2 = pi - cos(i[1] * pi / 180)

            elif i[0] == 'z+':
                unit_component_3 = cos(i[1] * pi / 180)

            elif i[0] == 'z-':
                unit_component_3 = pi - cos(i[1] * pi / 180)

        unit_vector = [unit_component_1, unit_component_2, unit_component_3]
        return unit_vector