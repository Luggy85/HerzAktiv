def calculate_bmi(weight, height):
    """Berechnet den Body-Mass-Index (BMI).

    Args:
        weight (float): Gewicht in Kilogramm.
        height (float): Größe in Metern.

    Returns:
        float: Der berechnete BMI.
        str: Die BMI-Kategorie.
    """
    if height <= 0:
        raise ValueError("Die Höhe muss größer als 0 sein.")
    if weight <= 0:
        raise ValueError("Das Gewicht muss größer als 0 sein.")

    bmi = round(weight / (height ** 2),2)

    if bmi < 18.5:
        category = "Untergewicht"
    elif 18.5 <= bmi < 24.9:
        category = "Normalgewicht"
    elif 25 <= bmi < 29.9:
        category = "Übergewicht"
    else:
        category = "Adipositas"

    return bmi, category

