def nutrient_to_float(nutrient: int | None) -> float | None:
    if nutrient and nutrient > 0:
        return round(nutrient / 100, 2)
    return None
