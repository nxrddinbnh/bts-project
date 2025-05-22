from PyQt6.QtGui import QFont

# COLORS
PRIMARY = "#779BDF"
SECONDARY = "#F3C359"
ACCENT = "#FE474A"
BG_100 = "#283142"
BG_200 = "#1B2435"
BG_300 = "#131529"
BG_OPACITY = "rgba(40, 49, 66, 0.3)"
TEXT_100 = "#FFFFFF"
TEXT_200 = "#9e9e9e"

# FONTS
FONT_TITLE = QFont("Lato", 10, 400)
FONT_BODY = QFont("Lato", 8, QFont.Weight.Normal)
FONT_BODY_B = QFont("Lato", 12, QFont.Weight.Bold)
FONT_VALUES = QFont("Lato", 25, QFont.Weight.Bold)

# RADIUS & PADDING
RADIUS_100 = 10
RADIUS_200 = 20
PADD_100 = 5
PADD_200 = 10

# SERIAL COMMANDS
CMD_LIGHT = 0x45
CMD_MOTOR_ELEV = 0x4A
CMD_MOTOR_AZIM = 0x4B
CMD_CORRECT = 0x4C
REQUEST_DATA = 0x52
END_FRAME = 0x0D

# VARIABLES FOR SOLAR PANEL CONTROL DATA
VARIABLES_NAME = [
    "lum_east",         # luminosity east
    "lum_west",         # luminosity west
    "lum_north",        # luminosity north
    "lum_south",        # luminosity south
    "lum_average",      # average luminosity
    "lum_dev_az",       # luminosity deviation azimuth
    "lum_dev_el",       # luminosity deviation elevation
    
    "reserved",

    "volt_panel",       # solar panel voltage
    "volt_batt",        # battery voltage
    "curr_panel",       # solar panel current
    "curr_batt",        # battery current
    "charge",           # charge indicator
    "full_charge",      # full charge indicator
    "empty_charge",     # empty charge indicator

    "light_on",         # lighting indicator
    "light_lvl",        # lighting level

    "curr_m1",          # motor 1 current
    "curr_m2",          # motor 2 current
    "overload_el",      # overload indicator elevation
    "overload_az",      # overload indicator azimuth
    "moving",           # movement indicator (0 = stopped)
    "angle_az",         # azimuth angle
    "angle_el",         # elevation angle
    "limit",            # stop indicator

    "correction_on",    # automatic correction mode (0 = off, 1 = on)
    "correction_int",   # correction interval (minutes)
    "correction_thr"    # luminosity deviation threshold for correction
]

# VARIABLES LENGHT FIELD
FIELD_LENGTHS = [
    3, 3, 3, 3, 3, 3, 3,
    2,
    3, 3, 3, 3,
    2, 2, 2,
    3, 3, 3, 3,
    2, 2, 2,
    3, 3,
    2, 2,
    3, 3, 
]

# VARIABLES FOR THE API
ALLOWED_KEYS = {
    "lum_east", "lum_west", "lum_north", "lum_south", "lum_average",
    "volt_panel", "volt_batt", "curr_panel", "curr_batt",
    "charge", "full_charge", "empty_charge",
    "light_on", "light_lvl",
    "curr_m1", "curr_m2",
    "angle_az", "angle_el",
    "correction_on", "correction_int", "correction_thr"
}

FIELD_TITLES = {
    "id": "ID",
    "datetime": "DATE TIME",
    "lum_east": "EAST",
    "lum_west": "WEST",
    "lum_north": "NORTH",
    "lum_south": "SOUTH",
    "lum_average": "AVERAGE",
    "volt_panel": "VOLT PANEL",
    "volt_batt": "VOLT BATTERY",
    "curr_panel": "CURRENT PANEL",
    "curr_batt": "CURRENT BATTERY",
    "charge_state": "CHARGE STATE",
    "light_on": "LEDS ON",
    "light_lvl": "LIGHT LEVEL",
    "curr_m1": "CURRENT ELEV",
    "curr_m2": "CURRENT AZIM",
    "angle_el": "ANGLE ELEV",
    "angle_az": "ANGLE AZIM",
    "correction_on": "AUTO MOD",
    "correction_int": "CORRECTION INTERVAL",
    "correction_thr": "CORRECTION THRESHOLD ",
}
