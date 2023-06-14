heat_transfer_resistance = {
    "Rsi": {"upward": 0.10, "horizontal": 0.13, "downward": 0.17},
    "Rse": 0.04,
    "REarth": 0,
}


def material_default_value():
    return {
        "Herstellungsphase": 0,
        "Erneuerung": 0,
        "Energiebedarf": 0,
        "Lebensendphase": 0
    }
