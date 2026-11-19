import math

def circle_area(radius):
    try:
        radius = float(radius)
        if not math.isfinite(radius) or radius < 0:
            return "Invalid input"
        return round(math.pi * radius ** 2, 2)
    except (TypeError, ValueError, OverflowError):
        return "Invalid input"


def handle(form):
    return {'circle_result': circle_area(form.get('radius'))}