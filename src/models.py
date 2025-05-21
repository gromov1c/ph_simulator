"""
Data Models and Constants for the pH Calculator.
Defines UI colors, concentration values, and mappings between
chemical formulas and their properties for use throughout the application.
"""
from calculations import pKA_HC2H3O2, pKA_NH4Cl, pKA_NaH2PO4, pKA_NaHCO3, pKA_H2CO3

# Colors
ASH_GREY = "#BCC9D1"

#"#BCC9D1" light blue
#"#CAD2C5" original
ASHIER_GREY = "#A5B4BC"
#"#A4B19B"
CAMBRIDGE_BLUE = "#A5B4BC"
BURNT_ORANGE = "#EA710C"
BLACK = "#000000"

# Concentration values - from low to high
CONCENTRATION_VALUES = [
    0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009,
    0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009,
    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1
]

# Buffer concentration values - from low to high (same as general concentration values)
BUFFER_CONCENTRATION_VALUES = CONCENTRATION_VALUES.copy()

# pH color mapping for pH strip display
PH_COLORS = {
    0: "#8B0000",  # Very acidic - Dark Red
    1: "#B22222",  # Strong acid - Firebrick
    2: "#E63900",  # Strong acid - Reddish Orange
    3: "#FF4500",  # Moderately acidic - Orange Red
    4: "#FF7F00",  # Moderately acidic - Deep Orange
    5: "#FFA500",  # Weak acid - Orange
    6: "#FFD700",  # Approaching neutral - Golden Yellow
    7: "#ADFF2F",  # Neutral - Yellow Green
    8: "#32CD32",  # Weak base - Lime Green
    9: "#228B22",  # Moderately basic - Forest Green
    10: "#008080",  # Basic - Teal
    11: "#0000FF",  # Strong base - Blue
    12: "#0000CD",  # Strong base - Medium Blue
    13: "#00008B",  # Very basic - Dark Blue
    14: "#191970",  # Extremely basic - Midnight Blue
}

# Mapping for full buffer names to keys used in pKa dictionary
BUFFER_NAME_MAPPING = {
    "HC\u2082H\u2083O\u2082 / NaC\u2082H\u2083O\u2082: Acetic Acid / Sodium Acetate": "HC\u2082H\u2083O\u2082 / NaC\u2082H\u2083O\u2082",
    "NH\u2084Cl / NH\u2083: Ammonium Chloride / Ammonia": "NH\u2084Cl / NH\u2083",
    "NaH\u2082PO\u2084 / Na\u2082HPO\u2084: Sodium Dihydrogen Phosphate / Disodium Hydrogen Phosphate": "NaH\u2082PO\u2084 / Na\u2082HPO\u2084",
    "NaHCO\u2083 / Na\u2082CO\u2083: Sodium Bicarbonate / Sodium Carbonate": "NaHCO\u2083 / Na\u2082CO\u2083",
    "H\u2082CO\u2083 / NaHCO\u2083: Carbonic Acid / Sodium Bicarbonate": "H\u2082CO\u2083 / NaHCO\u2083"
}

# Mapping buffer solutions to their pKa values
BUFFER_PKA_VALUES = {
    "HC\u2082H\u2083O\u2082 / NaC\u2082H\u2083O\u2082": pKA_HC2H3O2,
    "NH\u2084Cl / NH\u2083": pKA_NH4Cl,
    "NaH\u2082PO\u2084 / Na\u2082HPO\u2084": pKA_NaH2PO4,
    "NaHCO\u2083 / Na\u2082CO\u2083": pKA_NaHCO3,
    "H\u2082CO\u2083 / NaHCO\u2083": pKA_H2CO3,
}
