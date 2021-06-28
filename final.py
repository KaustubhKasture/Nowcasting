import sys
import io
import os
import datetime
import urllib.request
import keras
import numpy as np
import wradlib as wrl
from nowcasting import nowcast
import matplotlib.pyplot as plt

model = nowcast()
model.load_weights("nowcast_weights.h5")
#model.summary()
def download_and_read_RY(RY_timestamp):
    url = f"https://opendata.dwd.de/weather/radar/radolan/ry/raa01-ry_10000-{RY_timestamp}-dwd---bin"
    new=urllib.request.urlopen(url)
    print(new)
    data_binary = urllib.request.urlopen(url).read()
    data, attr = wrl.io.read_radolan_composite( io.BytesIO( data_binary ), missing=0 )
    data = data.astype("float32")
    return data, attr

def download_data():
    latest_scan, latest_attr = download_and_read_RY("latest")
    latest_datetime = latest_attr["datetime"]
    list_for_downloading = [ts.strftime("%y%m%d%H%M") for ts in 
    [latest_datetime - datetime.timedelta(minutes=t) for t in [15, 10, 5]]]
    previous_scans = np.array([download_and_read_RY(ts)[0] for ts in list_for_downloading])
    scans = np.concatenate([previous_scans, latest_scan[np.newaxis, ::, ::]], axis=0)
    return scans, latest_datetime

def Scaler(array):
    return np.log(array+0.01)

def invScaler(array):
    return np.exp(array) - 0.01

def pad_to_shape(array, from_shape=900, to_shape=928, how="mirror"):
    # calculate how much to pad in respect with native resolution
    padding = int( (to_shape - from_shape) / 2)
    # for input shape as (batch, W, H, channels)
    if how == "zero":
        array_padded = np.pad(array, ((0,0),(padding,padding),(padding,padding),(0,0)), mode="constant", constant_values=0)
    elif how == "mirror":
        array_padded = np.pad(array, ((0,0),(padding,padding),(padding,padding),(0,0)), mode="reflect")
    return array_padded

def pred_to_rad(pred, from_shape=928, to_shape=900):
    # pred shape 12,928,928
    padding = int( (from_shape - to_shape) / 2)
    return pred[::, padding:padding+to_shape, padding:padding+to_shape].copy()

def data_preprocessing(X):
    # 0. Right shape for batch
    X = np.moveaxis(X, 0, -1)
    X = X[np.newaxis, ::, ::, ::]
    # 1. To log scale
    X = Scaler(X)
    # 2. from 900x900 to 928x928
    X = pad_to_shape(X)
    
    return X

def data_postprocessing(nwcst):   
    # 0. Squeeze empty dimensions
    nwcst = np.squeeze(np.array(nwcst))
    # 1. Convert back to rainfall depth
    nwcst = invScaler(nwcst)
    # 2. Convert from 928x928 back to 900x900
    nwcst = pred_to_rad(nwcst)
    # 3. Return only positive values
    nwcst = np.where(nwcst>0, nwcst, 0)
    return nwcst

def prediction(model_instance, input_data, lead_time=12):
    input_data = data_preprocessing(input_data)
    nwcst = []
    for _ in range(lead_time):
        # make prediction
        pred = model_instance.predict(input_data)
        # append prediction to holder
        nwcst.append(pred)
        # append prediction to the input shifted on one step ahead
        input_data = np.concatenate([input_data[::, ::, ::, 1:], pred], axis=-1)
    nwcst = data_postprocessing(nwcst)
    return nwcst

def display_outputs(nwcst):
    lis = []
    s=1
    # get coordinates
    radolan_grid_xy = wrl.georef.get_radolan_grid(900,900)
    x = radolan_grid_xy[:,:,0]
    y = radolan_grid_xy[:,:,1]
    for i in nwcst:
        lis.append(i)
    last_data = lis[0]
    #plt.figure(figsize=(10,8))
    plt.pcolormesh(x,y,last_data)
    plt.axis('off')
    #SAVE FILE LOCALLY
    #plt.savefig('nowcast.png',dpi=300,transparent=True,bbox_inches='tight', pad_inches=0)
    plt.show()

RY_latest, RY_latest_timestep = download_data()
print(RY_latest_timestep)
nwcst = prediction(model, RY_latest)
display_outputs(nwcst)