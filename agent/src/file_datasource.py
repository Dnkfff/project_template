from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_file = None
        self.gps_file = None
        self.parking_file = None

    def read(self) -> AggregatedData:
        while True:  # Infinite loop for continuous reading
            try:
                accelerometerData = self.readAccelerometeData()
                gpsData = self.readGpsData()
                parkingData = self.readParkingData()
                return AggregatedData(
                    datetime.now(),
                    accelerometerData,
                    gpsData,
                    parkingData,
                    config.USER_ID
                )
            except StopIteration:
                self.startReading()  # Reopen files when end of file is reached

    def readAccelerometeData(self):
        column = next(reader(self.accelerometer_file))
        return Accelerometer(*map(float, column))

    def readGpsData(self):
        column = next(reader(self.gps_file))
        return Gps(*map(float, column))

    def readParkingData(self):
        empty_count, latitude, longitude = map(float, next(reader(self.parking_file)))
        gps = Gps(latitude, longitude)
        return Parking(empty_count, gps)

    def startReading(self):
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')
        next(self.accelerometer_file)
        next(self.gps_file)
        next(self.parking_file)

    def stopReading(self):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
        if self.parking_file:
            self.parking_file.close()
