# from csv import reader
# from datetime import datetime
# from domain.accelerometer import Accelerometer
# from domain.gps import Gps
# from domain.aggregated_data import AggregatedData
# import config

# class FileDatasource:
# def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
# pass
# def read(self) -> AggregatedData:
# """Метод повертає дані отримані з датчиків"""
# def startReading(self, *args, **kwargs):
# """Метод повинен викликатись перед початком читання даних"""
# def stopReading(self, *args, **kwargs):
# """Метод повинен викликатись для закінчення читання даних"""

-------------------------------------------------------------------

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
        # gps details
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

    def stopReading(self, *args, **kwargs):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()


-------------------------------------------------------------------
from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
import config


class FileDatasource:
        def __init__(self, file_paths):
        self.files = {}
        for filename, data_type in file_paths.items():
            self.files[filename] = self._open_file(filename, data_type)

    def read_data(self):
        data = {}
        for filename, file_obj in self.files.items():
            try:
                data[filename] = self._read_file(file_obj)
            except StopIteration:
                # Handle file exhaustion (e.g., raise an exception or return None)
                pass
        return data

    def _open_file(self, filename, data_type):
        # Open the file based on data type (e.g., CSV reader for sensor data, JSON reader for metadata)
        if data_type == "csv":
            return open(filename, "r")
        else:
            raise NotImplementedError(f"Unsupported data type: {data_type}")

    def _read_file(self, file_obj):
        # Read the file line by line and parse data based on data type
        if isinstance(file_obj, csv.reader):
            column = next(file_obj)
            return self._parse_data(column, data_type)
        else:
            raise NotImplementedError(f"Unsupported file type: {type(file_obj)}")

    def _parse_data(self, column, data_type):
        # Convert data based on data type (e.g., map floats for sensor data, extract specific features from JSON)
        if data_type == "csv":
            return self._parse_accelerometer_data(column)  # Replace with your parsing logic
        else:
            raise NotImplementedError(f"Unsupported data type: {data_type}")

    def _parse_accelerometer_data(self, column):
        # Assuming x, y, z format
        return Accelerometer(*map(float, column))

    def close(self):
        for file_obj in self.files.values():
            file_obj.close()

# Example usage with more flexibility for different data types
# data_reader = FileDatasource({
#     "data/accelerometer.csv": "csv",
#     "data/gps.json": "json",  # Add more data sources as needed
# })
# data = data_reader.read_data()
# data_reader.close()

# Access parsed data (example for accelerometer)
# accelerometer_data = data["data/accelerometer.csv"]
