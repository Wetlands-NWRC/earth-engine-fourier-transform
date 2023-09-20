# Earth Engine Fourier Transform
This repository contains a Google Earth Engine implementation of the Fourier Transform. The Fourier Transform is a mathematical tool that allows us to decompose a signal into its constituent frequencies. The Fourier Transform is widely used in signal processing, physics, and engineering. In this repository, we will use the Fourier Transform to analyze the frequency content of time series data.

This repository is a companion to the [Earth Engine Time Series Modeling](https://developers.google.com/earth-engine/tutorials/community/time-series-modeling) tutorial.

## Installation
### From Source
```bash
git clone 
```
```bash
pip install build
```
```bash
python -m build .
```
```bash
pip install dist/eeft-0.1.0.tar.gz
```

### From Release (Recommended)
1) Download the latest release from the [releases page]()
2) move the `eeft.tz.gz` bianries folder to your project directory
3) pip install `eeft.tgz.gz`


## Usage
```python
import ee
import eeft

ee.Initialize()

# Define a point of interest
point = ee.Geometry.Point(-77.3832, 44.1628)
# Do some pre-processing, filtering, and masking
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate('2018', '2021')
    .filterBounds(point)
    .map(mask_s2_clouds)
)

# Create the time series
time_series = eeft.TimeSeries(collection=collection, dependent='B11')
time_series = (
    ts.add_constant()
    .add_time()
    .add_harmonics()
    .build()
)

model = eeft.HarmonicModel(time_series=time_series)
ft = eeft.FourierTransform(model=model)
ft.fit()
ft = ft.transform()

```
