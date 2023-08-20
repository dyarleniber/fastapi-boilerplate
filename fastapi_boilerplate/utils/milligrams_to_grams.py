def milligrams_to_grams(mg: float | None) -> float | None:
    if mg and mg > 0:
        return mg / 1000
    return None
