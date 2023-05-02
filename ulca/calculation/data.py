material = {
    "Gipsputz": {"rho": 1800, "lambda": 0.52},
    "KS-Mauerwerk": {"rho": 2000, "lambda": 0.79},
    "Steinwolle-Daemmstoff": {"rho": 1250, "lambda": 0.03},
    "WDVS Verklebung und Beschichtung": {"rho": 1500, "lambda": 0.52},
}

heat_transfer_resistance = {
    "Rsi": {"upward": 0.10, "horizontal": 0.13, "downward": 0.17},
    "Rse": 0.04,
    "REarth": 0,
}


def jsonfield_default_value():
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
