# creado por aider con la API de Gemini
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a Celsius temperature to Fahrenheit rounded to 2 decimals.

    Args:
        c: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit rounded to 2 decimal places.
    """
    return round(c * 9.0 / 5.0 + 32.0, 2)
