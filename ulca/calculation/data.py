heat_transfer_resistance = {
    "Rsi": {"upward": 0.10, "horizontal": 0.13, "downward": 0.17},
    "Rse": 0.04,
    "REarth": 0,
}


def building_default_value():
    return {
        "floor": {
            "Stahlbeton": 200,
            "Estrich": 50,
            "Sauberkeitsschicht": 50,
            "Abdichtung": 10,
            "Dampfsperre": 2,
            "Schaumglas": 120,
            "Extrudiertes Polystyrol (XPS)": 120,
        },
        "roofbase": {
            "Stahlbeton": 200,
            "Abdichtung": 10,
            "Dampfsperre": 4,
            "Kies": 50,
            "Extrudiertes Polystyrol (XPS)": 180,
        },
        "wall": {
            "WDVS Verklebung und Beschichtung": 15,
            "Steinwolle-Daemmstoff": 140,
            "KS-Mauerwerk": 175,
            "Gipsputz": 15,
        },
    }


def material_default_value():
    return {
        "Herstellungsphase": 0,
        "Erneuerung": 0,
        "Energiebedarf": 0,
        "Lebensendphase": 0
    }
