# Radar-Based Precipitation Nowcasting using Deep Learning

A deep learning powered weather nowcasting system that predicts short-term rainfall using radar reflectivity data from the DWD RADOLAN dataset. Built with a U-Net  based convolutional neural network, this project enables real-time precipitation forecasting up to 1 hour into the future.

---

## Features

- **Real-time 1-hour nowcasting** (12 future 5-minute frames)
- **Deep learning model (U-Net)** for spatiotemporal radar forecasting
- **Radar input data** from the German Weather Service (DWD RADOLAN RY)
- **Autoregressive forecasting** using previous predictions
- **Visualization** of predicted rainfall maps using georeferenced plots
- Includes tools for debugging, visualization, and raw data inspection

---

## Quick Overview

The system downloads the latest radar reflectivity data, preprocesses the last 20 minutes of scans, and feeds them into a U-Net model to predict the next 12 radar frames (i.e., 1 hour ahead). The outputs are postprocessed and visualized on a spatial grid.

---

## Repository Structure

```
📦 nowcasting-project/
├── final.py            # Main production script (end-to-end inference)
├── test.py             # Development/testing variant of final.py
├── nowcasting.py       # U-Net model definition (Keras)
├── raw_data.py         # Raw radar data downloader and visualizer
```

---

## Data Source

**German Weather Service (DWD)**  
- Product: RADOLAN RY (composite radar reflectivity)
- Frequency: Every 5 minutes  
- Format: Binary radar files  
- URL pattern:  
  `https://opendata.dwd.de/weather/radar/radolan/ry/raa01-ry_10000-<timestamp>-dwd---bin`

Read using [`wradlib`](https://docs.wradlib.org/en/stable/).

---

## Model Architecture

- U-Net style fully convolutional network
- Input shape: `928 x 928 x 4` (last 20 min of radar scans)
- Output shape: `928 x 928 x 1` per time step (predicted rainfall)
- Uses skip connections for spatial detail preservation
- Autoregressively predicts 12 future frames

---

## How to Run

### 1. Install Dependencies

```bash
pip install keras tensorflow numpy matplotlib wradlib
```

### 2. Add Pretrained Weights

Download the model weights `nowcast_weights.h5` and place it in the root directory.  
[Download model weights](https://drive.google.com/drive/folders/1n_QVFc8Ked4oTo184dqisqn7UAD4nVyO)

### 3. Run the Main Script

```bash
python final.py
```

This will:
- Download the latest radar scans
- Predict the next 12 frames
- Visualize the output using `matplotlib`

---

## Example Output

The system will generate a plot like this showing the predicted precipitation pattern for the next hour:

![Example Output](media/nowcast(2021-05-12%2010,00,00).png)
 
---

## Testing & Debugging

To experiment or debug locally:

```bash
python test.py
```

To explore raw radar data only:

```bash
python raw_data.py
```

---

## License

MIT License – feel free to use and adapt this project.

---