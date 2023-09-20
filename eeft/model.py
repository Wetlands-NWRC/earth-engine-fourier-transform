import ee

from .time_series import TimeSeries


class HarmonicModel:
    def __init__(self, time_series: TimeSeries) -> None:
        self.time_series = time_series

    @property
    def harmonic_trend(self) -> ee.Image:
        selectors = [*self.time_series.independent, self.time_series.dependent]
        return self.time_series.collection.select(selectors=selectors).reduce(
            ee.Reducer.linearRegression(len(self.time_series.independent), 1)
        )

    @property
    def harmonic_coefficients(self) -> ee.Image:
        return self.harmonic_trend.select("coefficients").arrayFlatten(
            [self.time_series.independent, ["coef"]]
        )
