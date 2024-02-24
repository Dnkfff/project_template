from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename) -> None:
        self.accelerometer_filename = accelerometer_filename;
        self.gps_filename = gps_filename;
        self.parking_filename = parking_filename;
        self.accelerometer_file = None;
        self.gps_file = None;
        self.parking_file = None;

    def read(self) -> AggregatedData:
        accelerometerData = None;
        gpsData = None;
        ParkingData = None;

        if self.accelerometer_file:
            accelerometerData = self.readAccelerometeData();

        if self.gps_file:
            gpsData = self.readGpsData();
        
        if self.gps_file:
            parkingData = self.readParkingData();

        # Place the return statement within the function
        return AggregatedData(
            datetime.now(),
            accelerometerData,
            gpsData,
            parkingData,
            config.USER_ID
        )

    def readAccelerometeData(self):
        # accelerometer info [x, y, z]
        column = next(reader(self.accelerometer_file));
        return Accelerometer(*map(float, column));

    def readGpsData(self):
        # gps details info[longitude, latitude]
        try:
            column = next(reader(self.gps_file));
            return Gps(*map(float, column));
        except StopIteration:
            column = next(reader(self.gps_file));
            return Gps(*map(float, column));  # Or raise a custom exception if preferred

    def readParkingData(self):
        # parking information[longitude, latitude]
        try:
            column = next(reader(self.parking_file));
            empty_count, latitude, longitude = map(float, column)
            gps = Gps(latitude, longitude)
            return Parking(empty_count, gps);
        except StopIteration:
            column = next(reader(self.parking_file));
            empty_count, latitude, longitude = map(float, column)
            gps = Gps(latitude, longitude)
            return Parking(empty_count, gps); # Or raise a custom exception if preferred

    def startReading(self, *args, **kwargs):
        self.accelerometer_file = open(self.accelerometer_filename, 'r');
        self.gps_file = open(self.gps_filename, 'r');
        self.parking_file = open(self.parking_filename, 'r');

        # Continuing to next column
        next(self.accelerometer_file);
        next(self.gps_file);
        next(self.parking_file);

    def stopReading(self, *args, **kwargs):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
        if self.parking_file:
            self.parking_file.close()
