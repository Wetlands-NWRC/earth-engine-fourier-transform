import ee

from math import pi
from typing import Callable


def phase(mode: int) -> Callable:
    name = f"phase_{mode}"
    cos, sin = f"cos_{mode}_coef", f"sin_{mode}_coef"

    def wrapper(image: ee.Image):
        image = ee.Image(image)
        calc = (
            image.select(cos).atan2(image.select(sin)).unitScale(-pi, pi).rename(name)
        )
        return image.addBands(calc)

    return wrapper


def amplitude(mode: int) -> Callable:
    name = f"amp_{mode}"
    cos, sin = f"cos_{mode}_coef", f"sin_{mode}_coef"

    def wrapper(image: ee.Image):
        image = ee.Image(image)
        calc = image.select(cos).hypot(image.select(sin)).rename(name)
        return image.addBands(calc)

    return wrapper
