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


# Dictionary mapping variable keys to their display titles and field lengths
VARIABLES_NAME = {
    "east": {"title": "east", "length": 3},                                     # luminosity east
    "west": {"title": "west", "length": 3},                                     # luminosity west
    "north": {"title": "north", "length": 3},                                   # luminosity north
    "south": {"title": "south", "length": 3},                                   # luminosity south
    "average": {"title": "average", "length": 3, "skip": 8},                    # average luminosity
    "v_panel": {"title": "volt panel", "length": 3},                            # solar panel voltage
    "v_battery": {"title": "volt battery", "length": 3},                        # battery voltage
    "c_panel": {"title": "current panel", "length": 3},                         # solar panel current
    "c_battery": {"title": "current battery", "length": 3},                     # battery current
    "charging": {"title": "charging", "length": 2},                             # charge indicator
    "full": {"title": "full", "length": 2},                                     # full charge indicator
    "empty": {"title": "empty", "length": 2},                                   # empty charge indicator

    "light_on": {"title": "light on", "length": 3},                             # the leds that are on
    "light_lvl": {"title": "light level", "length": 3},                         # lighting level

    "curr_elev": {"title": "current elev", "length": 3},                        # elevation motor current
    "curr_azim": {"title": "current azim", "length": 3, "skip": 6},             # azimuth motor current
    "angle_azim": {"title": "angle azim", "length": 3},                         # azimuth motor current
    "angle_elev": {"title": "current elev", "length": 3, "skip": 2},            # elevation motor angle

    "corr_mode": {"title": "mode", "length": 2},                                # automatic correction mode (0 = off, 1 = on)
    "corr_interval": {"title": "corr. interval", "length": 3},                  # correction interval (minutes)
    "corr_threshold": {"title": "corre. threshold", "length": 3}                # luminosity deviation threshold for correction
}
