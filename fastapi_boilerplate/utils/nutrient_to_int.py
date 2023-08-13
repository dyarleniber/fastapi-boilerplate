def nutrient_to_int(nutrient: float | None) -> int | None:
    if nutrient and nutrient > 0:
        return int(round(nutrient, 2) * 100)
    return None
