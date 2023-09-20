// Compute phase and amplitude.
var phase = harmonicTrendCoefficients.select('sin')
    .atan2(harmonicTrendCoefficients.select('cos'))
    // Scale to [0, 1] from radians.
    .unitScale(-Math.PI, Math.PI);
var amplitude = harmonicTrendCoefficients.select('sin')
    .hypot(harmonicTrendCoefficients.select('cos'))
    // Add a scale factor for visualization.
    .multiply(5);
// Compute the mean NDVI.
var meanNdvi = filteredLandsat.select('NDVI').mean();
// Use the HSV to RGB transformation to display phase and amplitude.
var rgb = ee.Image.cat([phase, amplitude, meanNdvi]).hsvToRgb();
Map.addLayer(rgb, {}, 'Phase (hue), Amplitude (sat), NDVI (val)');