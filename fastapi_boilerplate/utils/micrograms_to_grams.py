def micrograms_to_grams(ug: float | None) -> float | None:
    if ug and ug > 0:
        return ug / 1000000
    return None
