from dataclasses import dataclass
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking


@dataclass
class AggregatedData:
    timestamp: datetime
    accelerometer: Accelerometer
    gps: Gps
    parking: Parking
    user_id: int
