# Cowlibration: Field
Calibrate relative positions of Apriltags on the field

<img src="docs/screenshot.png" width="480"/>

## Build
```
cmake --preset=default
cmake --build build
```

## Usage
```
./build/FieldCalibrator
  --input-dir [input path to folder]
  --camera-model [input camera model path]
  --ideal-map [input ideal map path]
  --output-file [output map path]
  --fps [detection fps]
```

## Visualize
```
python scripts/visualize.py [ideal field map path] [observed field map path]
```
