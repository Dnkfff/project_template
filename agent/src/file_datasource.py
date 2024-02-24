from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str,gps_filename: str,) -> None:
        self.accelerometer_filename = accelerometer_filename;
        self.gps_filename = gps_filename;
        self.accelerometer_file = None;
        self.gps_file = None;

    def read(self) -> AggregatedData:
        accelerometerData = None;
        gpsData = None;

        if self.accelerometer_file:
            accelerometerData = self.readAccelerometeData();

        if self.gps_file:
            gpsData = self.readGpsData();

        # Place the return statement within the function
        return AggregatedData(
            accelerometerData,
            gpsData,
            datetime.now(),
            config.USER_ID,
        )

    def readAccelerometeData(self):
        # x, y, z
        column = next(reader(self.accelerometer_file));
        return Accelerometer(*map(float, column));

    def readGpsData(self):
        # longitude, longitude
        try:
            column = next(reader(self.gps_file));
            return Gps(*map(float, column));
        except StopIteration:
            column = next(reader(self.gps_file));
            return Gps(*map(float, column));  # Or raise a custom exception if preferred

    def startReading(self, *args, **kwargs):
        self.accelerometer_file = open(self.accelerometer_filename, 'r');
        self.gps_file = open(self.gps_filename, 'r');

        # Skipping the columns with names
        next(self.accelerometer_file);
        next(self.gps_file);
        # while True:
        #     try:
        #         yield self.read()
        #     except StopIteration:
        #         self.startReading()  # Reopen files and start a new iteration if StopIteration appears

    def stopReading(self, *args, **kwargs):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
