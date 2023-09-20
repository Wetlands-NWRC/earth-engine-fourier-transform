import re
import ee

from .model import HarmonicModel
from .calcs import phase, amplitude


class FourierTransform:
    def __init__(self, model: HarmonicModel) -> None:
        self.model = model
        self._fitted = False
        self._transformed = None

    def fit(self):
        """add coefficients to the model.time_series.collection"""
        self.model.time_series.collection = self.model.time_series.collection.map(
            lambda x: x.addBands(self.model.harmonic_coefficients)
        )
        self._fitted = True
        return self

    def transform(self) -> ee.Image:
        if self._transformed is not None:
            return self._transformed

        if not self._fitted:
            raise ValueError("You must fit before transforming... ")

        pattern = r"(sin|cos)_\d+"
        sin_cos_elements = [
            element
            for element in self.model.time_series.independent
            if re.match(pattern, element)
        ]

        modes = len(sin_cos_elements) // 2
        for mode in range(1, modes + 1):
            phase_calc = phase(mode)
            amplitude_calc = amplitude(mode)
            self.model.time_series.collection = self.model.time_series.collection.map(
                phase_calc
            ).map(amplitude_calc)

        selectors = f"{self.model.time_series.dependent}|.*coef|amp.*|phase.*"
        self.model.time_series.collection = self.model.time_series.collection.select(
            selectors
        )
        self._transformed = self.model.time_series.collection.median().unitScale(-1, 1)
        return self._transformed
