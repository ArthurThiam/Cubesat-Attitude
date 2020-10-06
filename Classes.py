from math import acos, pi
import configparser


class Data:

    def __init__(self, data):
        self.data = data

    # Read range calibration data
    def ranges(self):
        config = configparser.ConfigParser()
        config.read('calibration.ini')

        ranges = {
            "x+": config.getint('settings', 'x_p_max') - config.getint('settings', 'x_p_min'),
            "x-": config.getint('settings', 'x_n_max') - config.getint('settings', 'x_n_min'),

            "y+": config.getint('settings', 'y_p_max') - config.getint('settings', 'y_p_min'),
            "y-": config.getint('settings', 'y_n_max') - config.getint('settings', 'y_n_min'),

            "z+": config.getint('settings', 'z_p_max') - config.getint('settings', 'z_p_min'),
            "z-": config.getint('settings', 'z_n_max') - config.getint('settings', 'z_n_min')
        }

        return ranges

    # average sensor values and associate to correct face
    def averaged(self):
        x_pos_avg = 0.5 * (self.data[10] + self.data[11])
        x_neg_avg = 0.5 * (self.data[6] + self.data[7])
        y_pos_avg = 0.5 * (self.data[2] + self.data[3])
        y_neg_avg = 0.5 * (self.data[4] + self.data[5])
        z_pos_avg = 0.5 * (self.data[8] + self.data[9])
        z_neg_avg = 0.5 * (self.data[0] + self.data[1])

        avg_data = {
            "x+": x_pos_avg,
            "x-": x_neg_avg,
            "y+": y_pos_avg,
            "y-": y_neg_avg,
            "z+": z_pos_avg,
            "z-": z_neg_avg
        }

        return avg_data

    # Apply range calibration
    def calibrated(self):
        calibration_ranges = self.ranges()

        calibrated_data = {
            "x+": self.averaged()["x+"]*(1023/calibration_ranges["x+"]),
            "x-": self.averaged()["x-"]*(1023/calibration_ranges["x-"]),
            "y+": self.averaged()["y+"]*(1023/calibration_ranges["y+"]),
            "y-": self.averaged()["y-"]*(1023/calibration_ranges["y-"]),
            "z+": self.averaged()["z+"]*(1023/calibration_ranges["z+"]),
            "z-": self.averaged()["z-"]*(1023/calibration_ranges["z-"])
        }

        return calibrated_data

    # Sort the data to return the three largest values and their corresponding face
    def sorted(self):
        data_items = list(self.calibrated().items())
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
    def max_values(self):
        config = configparser.ConfigParser()
        config.read('calibration.ini')

        max_values = {
            "x+": config.getint('settings', 'x_p_max'),
            "x-": config.getint('settings', 'x_n_max'),

            "y+": config.getint('settings', 'y_p_max'),
            "y-": config.getint('settings', 'y_n_max'),

            "z+": config.getint('settings', 'z_p_max'),
            "z-": config.getint('settings', 'z_n_max')
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