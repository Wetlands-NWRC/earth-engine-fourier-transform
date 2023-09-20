import math
import ee

from typing import Callable

from .rmath import NDVI


class TimeSeries:
    def __init__(self, collection: ee.ImageCollection, dependent: str) -> None:
        self.collection = collection
        self.dependent: str = dependent
        self.independent: list[str] = []

    def __add_to_independed(self, value):
        """helper func add"""
        if value not in self.independent:
            self.independent.append(value)
        return None

    @staticmethod
    def _mk_freq_name(prefix: str, freq: int = 5) -> list[str]:
        return [f"{prefix}_{f}" for f in range(1, freq + 1)]

    def add_cloud_mask(self, algo: Callable):
        self.collection = self.collection.map(algo)
        return self

    def add_constant(self):
        def _add_constant(image):
            return image.addBands(ee.Image(1))

        self.__add_to_independed("constant")
        self.collection = self.collection.map(_add_constant)
        return self

    def add_time(self, omega: int = 1):
        def _add_time(image):
            date = image.date()
            years = date.difference(ee.Date("1970-01-01"), "year")
            time_radians = ee.Image(years.multiply(2 * math.pi * omega))
            return image.addBands(time_radians.rename("t").float())

        self.__add_to_independed("t")
        self.collection = self.collection.map(_add_time)
        return self

    def add_harmonics(self, freq: int = 5):
        if "t" not in self.independent:
            raise ValueError(
                "You need to add time to time seies before added harmonics"
            )
        if "constant" not in self.independent:
            raise ValueError(
                "You need to add Image Constant to time sereis before adding harmonics"
            )
        cos = self._mk_freq_name("cos", freq)
        sin = self._mk_freq_name("sin", freq)
        freqs = list(range(1, freq + 1))

        def _add_harmonics(image):
            frequencies = ee.Image.constant(freqs)
            time = ee.Image(image).select("t")
            cos_img = time.multiply(frequencies).cos().rename(cos)
            sin_img = time.multiply(frequencies).sin().rename(sin)
            return image.addBands(cos_img).addBands(sin_img)

        self.independent.extend(cos)
        self.independent.extend(sin)
        self.collection = self.collection.map(_add_harmonics)
        return self

    def build(self):
        return self
