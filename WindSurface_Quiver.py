
#################### Plotting Wind Surface Pattern ###########################

#################### Quiver Python Commands ##########################

 #https://cds.climate.copernicus.eu/terms#!/dataset/reanalysis-era5-land-monthly-means?tab=form
 # Monthly averaged reanalysis (Year 2020)
 # lat: 33 ta 34
 # lon: 51 ta 52
 
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import num2date
import cftime
import netCDF4
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import calendar

f = Dataset ('/home/lida/Desktop/OUREH/QUIVER/monthquiver.nc')

uten = f.variables['u10']
vten = f.variables['v10']
time = f.variables ['time']
latitudes = f.variables ['latitude']
longitudes = f.variables ['longitude']
#print(latitudes[1], longitudes[0])
time = num2date (time[:], units=time.units)

def domain_bounderies(year, month, day, lat1, lat2, lon1, lon2):
    
    lat_b = latitudes[:]>=lat1
    lat_s = latitudes[:]<=lat2
    lat = [a and b for a, b in zip(lat_b, lat_s)]
    
    times = time[:] == cftime.DatetimeGregorian(year,month,day)
    
    l = len(times)
       
    lon_b = longitudes[:]>=lon1
    lon_s = longitudes[:]<=lon2
    lon = [a and b for a, b in zip(lon_b, lon_s)]

    m=Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2, llcrnrlon=lon1,urcrnrlon=lon2,resolution='c')

    times_grid, latitudes_grid, longitudes_grid = [x.flatten() for x in np.meshgrid(time[times], latitudes[lat], longitudes[lon], indexing='ij')]

    x, y = m(longitudes_grid, latitudes_grid)

    vtenv = vten[times,lat,lon].flatten()
    
    utenu = uten[times,lat,lon].flatten()
    
    ws = (utenu*utenu + vtenv*vtenv)**0.5
    
    latflat = latitudes[lat].flatten()
    lonflat = longitudes[lon].flatten()
    
    yy=np.arange(0,len(latflat),3)
    xx=np.arange(0,len(lonflat),3)  
    
    points=np.meshgrid(yy,xx) 
   
    m.quiver(x,y,utenu,vtenv,ws, latlon=True)

    df = pd.DataFrame({'time':times_grid, 'lat': latitudes_grid, 'lon': longitudes_grid, 'uten': utenu, 'vten':vtenv})
   
    return df

for month in range (1,13):     # 12 months in range (1,13) 
    latlon_value = domain_bounderies(2020,month,1, 33, 34, 51, 52) 

    # Adding plot title.
    plt.title("QUIVER for month " + str(month) +': ' + calendar.month_name[month])

    fname='/home/lida/Desktop/atan/' + str(month) +':' + calendar.month_abbr[month] + '.png'

    plt.savefig(fname,format='png',dpi=300)   
    plt.close() 
    

