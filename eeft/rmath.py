from abc import ABC
from typing import Any
import ee


class NDVI:
    def __init__(self, nir: str, red: str, name: str = None) -> None:
        self.nir = nir
        self.red = red
        self.name = "NDVI" if name is None else name

    def __call__(self, image: ee.Image) -> Any:
        return image.addBands(self.compute(image=image))

    def compute(self, image: ee.Image):
        return image.normalizedDifference([self.nir, self.red]).rename(self.name)
