# GW Instek Screen Capture (gwicap)

<p align="center">
  <picture align="center">
    <img alt="gwicap logo" src="https://github.com/danlindleybaker/gwicap/blob/65641639f573c77b75765065b707277fcf1ae35b/images/gwicap_logo.svg">
  </picture>
</p>

<!-- ![gwicap logo](https://github.com/danlindleybaker/gwicap/blob/65641639f573c77b75765065b707277fcf1ae35b/images/gwicap_logo.svg) -->

This is a simple UI to enable a user to save data from a GW Instek Oscilloscope (tested with a GDS-1102-U). The frontend has been built with [DearPyGUI](https://github.com/hoffstadt/DearPyGui) and serial connection to the oscilloscope is achieved with [PySerial](https://github.com/pyserial/pyserial).

## Installation

Requires a Python installation (>3.9 - recommended is 3.12)

```shell

git clone https://github.com/danlindleybaker/gwicap
python -m pip install gwicap
```

## Usage

```shell

python -m gwicap
```

![Screenshot of gwicap's main window](https://github.com/danlindleybaker/gwicap/blob/02a95c1061c755dbcca644a47101a95cc749dedc/images/gwicap_screenshot.PNG)

1. Press the camera button to capture the screen of the oscilloscope. 
2. Press the save button to save a .png of whatever is on the graph. 
3. Press the Excel button to save an .xlsx of the data.

## License

Licensed under the [MIT](LICENSE) license