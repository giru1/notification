from enum import Enum


class CloudMessageTypes(Enum):
    FCM = 'FCM'
    GCM = 'GCM'


class BrowserTypes(Enum):
    CHROME = 'CHROME'
    FIREFOXv1 = "FIREFOXv1"
    FIREFOXv2 = "FIREFOXv2"
    OPERA = "OPERA"
    EDGE = "EDGE"
    SAFARI = "SAFARI"
