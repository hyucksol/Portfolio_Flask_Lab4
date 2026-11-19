import math

def triangle_area(base, height):
    """Area ng triangle: 1/2 x base x height."""
    try:
        base = float(base)
        height = float(height)
        if not (math.isfinite(base) and math.isfinite(height)) or base < 0 or height < 0:
            return "Invalid input"
        result = 0.5 * base * height
        if not math.isfinite(result):
            return "Invalid input"
        return round(result, 2)
    except (TypeError, ValueError, OverflowError):
        return "Invalid input"


def handle(form):
    return {'triangle_result': triangle_area(form.get('base'), form.get('height'))}