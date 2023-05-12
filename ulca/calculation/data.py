material = {
    "Gipsputz": {"lambda": 0.52},
    "KS-Mauerwerk": {"lambda": 0.79},
    "Steinwolle-Daemmstoff": {"lambda": 0.035},
    "WDVS Verklebung und Beschichtung": {"lambda": 0.1},
    "Stahlbeton": {"lambda": 2.5},
    "Bitumen": {"lambda": 0.23},
    "Estrich": {"lambda": 1.4},
    "Extrudierter Polystyrolschaum (XPS)": {"lambda": 0.035},
    "Dampfsperre": {"lambda": 0.4},
    "Sauberkeitsschicht": {"lambda": 2.1},
    "Kies": {"lambda": 0.7},
    "Expandierter Polystyrolschaum (EPS)": {"lambda": 0.035},
    "Schaumglas": {"lambda": 0.035},
}

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
