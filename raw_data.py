import wradlib as wrl
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import pylab as pl
import io

def download_and_read_RY(RY_timestamp):
    url = f"https://opendata.dwd.de/weather/radar/radolan/ry/raa01-ry_10000-{RY_timestamp}-dwd---bin"
    new=urllib.request.urlopen(url)
    print(new)
    data_binary = urllib.request.urlopen(url).read()
    data, attr = wrl.io.read_radolan_composite( io.BytesIO( data_binary ), missing=0 )
    data = data.astype("float32")
    return data, attr

data,metadata=download_and_read_RY('latest')
data = data.astype("float32")
print(metadata['datetime'])
maskeddata = np.ma.masked_equal(data,metadata["nodataflag"])

radolan_grid_xy = wrl.georef.get_radolan_grid(900,900)
x = radolan_grid_xy[:,:,0]
y = radolan_grid_xy[:,:,1]

pl.figure(figsize=(10,8))
pl.pcolormesh(x, y,data)
pl.show()