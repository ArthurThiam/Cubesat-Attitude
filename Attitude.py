import configparser
import serial
import time

class Data:

    def __init__(self, data):
        self.data = data

    # average sensor values
    def averaged(self):
        x_pos_avg = 0.5 * (self.data[10]+self.data[11])
        x_neg_avg = 0.5 * (self.data[6]+self.data[7])
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

    def calibrated(self):
        config = configparser.ConfigParser()
        config.read('calibration.ini')

        calibration_ranges = {
            "x+": config.getint('settings', 'x_p_max') - config.getint('settings', 'x_p_min'),
            "x-": config.getint('settings', 'x_n_max') - config.getint('settings', 'x_n_min'),

            "y+": config.getint('settings', 'y_p_max') - config.getint('settings', 'y_p_min'),
            "y-": config.getint('settings', 'y_n_max') - config.getint('settings', 'y_n_min'),

            "z+": config.getint('settings', 'z_p_max') - config.getint('settings', 'z_p_min'),
            "z-": config.getint('settings', 'z_n_max') - config.getint('settings', 'z_n_min')
        }

        calibrated_data = {
            "x+": self.averaged()["x+"]*(1023/calibration_ranges["x+"]),
            "x-": self.averaged()["x-"]*(1023/calibration_ranges["x-"]),
            "y+": self.averaged()["y+"]*(1023/calibration_ranges["y+"]),
            "y-": self.averaged()["y-"]*(1023/calibration_ranges["y-"]),
            "z+": self.averaged()["z+"]*(1023/calibration_ranges["z+"]),
            "z-": self.averaged()["z-"]*(1023/calibration_ranges["z-"])
        }

        return calibrated_data

    def sorted(self):
        return {key: value for key, value in sorted(self.calibrated().items(), key=lambda item: item[1])}

ser = serial.Serial('COM4', 9600)
time.sleep(2)
b = ser.readline()

#measurement = Data([900, 902, 0, 5, 880, 890, 950, 952, 1000, 1012, 20, 25])
#print(measurement.sorted())
