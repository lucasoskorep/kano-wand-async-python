from enum import Enum

class INFO(Enum):
    """Enum containing info UUIDs"""
    SERVICE = '64a70010-f691-4b93-a6f4-0968f5b648f8'
    ORGANIZATION_CHAR = '64a7000b-f691-4b93-a6f4-0968f5b648f8'
    SOFTWARE_CHAR = '64a70013-f691-4b93-a6f4-0968f5b648f8'
    HARDWARE_CHAR = '64a70001-f691-4b93-a6f4-0968f5b648f8'

class IO(Enum):
    """Enum containing _IO UUIDs"""
    SERVICE = '64a70012-f691-4b93-a6f4-0968f5b648f8'
    BATTERY_CHAR = '64a70007-f691-4b93-a6f4-0968f5b648f8'
    USER_BUTTON_CHAR = '64a7000d-f691-4b93-a6f4-0968f5b648f8'
    VIBRATOR_CHAR = '64a70008-f691-4b93-a6f4-0968f5b648f8'
    LED_CHAR = '64a70009-f691-4b93-a6f4-0968f5b648f8'
    KEEP_ALIVE_CHAR = '64a7000f-f691-4b93-a6f4-0968f5b648f8'

class SENSOR(Enum):
    """Enum containing sensor UUIDs"""
    SERVICE = '64a70011-f691-4b93-a6f4-0968f5b648f8'
    TEMP_CHAR = '64a70014-f691-4b93-a6f4-0968f5b648f8'
    QUATERNIONS_CHAR = '64a70002-f691-4b93-a6f4-0968f5b648f8'
    # RAW_CHAR = '64a7000a-f691-4b93-a6f4-0968f5b648f8'
    # MOTION_CHAR = '64a7000c-f691-4b93-a6f4-0968f5b648f8'
    MAGN_CALIBRATE_CHAR = '64a70021-f691-4b93-a6f4-0968f5b648f8'
    QUATERNIONS_RESET_CHAR = '64a70004-f691-4b93-a6f4-0968f5b648f8'


class PATTERN(Enum):
    """Enum for wand vibration patterns"""
    REGULAR = 1
    SHORT = 2
    BURST = 3
    LONG = 4
    SHORT_LONG = 5
    SHORT_SHORT = 6
    BIG_PAUSE = 7