# This file contains tools to plot ice thickness in the Arctic given the netCDF files 
# (under 'heff') available here: https://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/data/model_grid
import netCDF4
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import cmocean

# create ice thickness plot given latitude, longitude and ice thickness. Latitude and longitude are in the netCDF.

def create_ice_thickness_plot(lat_scalar,lon_scalar,thickness,label):
    # lat_scalar: latitude as given in the netCDF
    # lon_scalar: longitude as packaged in the netCDF
    # thickness: ice thickness as packaged in the netCDF
    # label: whatever you want to call this

    myfig =  plt.figure() 
    myax = plt.subplot(111)

    
    m = Basemap(projection='npstere',boundinglat=67,lon_0=270,resolution='l',round =True)
    # 'npstere' projection is the north Polar Stereographic Projection 
    # boundinglat = 67 means that I'm displaying lattitudes about 67 N 
    # lon_0 is what longitude is at the 0 mark
    # low resolution since this is for eyeballing
    # round = True means the projection is round (otherwise it looks terrible)
    m.drawmapboundary(fill_color='k')
    m.drawlsmask(land_color='k',ocean_color='k') # fill the continents and sea with black
    m.drawcoastlines(color='aqua',linewidth=0.7) # draw the coastlines in 'aqua' 
    
    barlim = np.arange(0,6,1) # this is the range of the colorbar
    
    cmap = cmocean.cm.thermal # set colourmap

    # creates contours for every 0.25 meters of sea ice from 0 to 5.1 meters
    cs = m.contourf(lon_scalar,lat_scalar,thickness, np.arange(0,5.1,0.25),extend='max', alpha=1,latlon=True,cmap=cmap)
  
    # creates the title
    t = plt.annotate(label,textcoords='axes fraction',
                xy=(0,0), xytext=(-0.4,0.85),
            fontsize=20,color='k')
    # creates the colourbars
    cbar = m.colorbar(cs,drawedges=True,location='bottom',pad = 0.14,size=0.07)
    # creates the ticks for the colourbars
    ticks = np.arange(0,6,1)
    cbar.set_ticks(ticks)
    labels = list(map(str,np.arange(0,6,1)))
    cbar.set_ticklabels(labels)
    # sets label under the colourbar
    cbar.set_label('Sea Ice Thickness (m)',fontsize=10,color='k')
    cbar.ax.tick_params(axis='x', size=.01)
    cbar.ax.tick_params(labelsize=6) 
    plt.rcParams['axes.linewidth'] = 0.1
    return m, myfig
    

# replace NaNs in heff data
def heff_replaceNaNs(thickness):
    replaced = thickness
    replaced[np.where(thickness ==9999.9)] = np.nan       # NaNs are given the value of 9999.9 in the heff data
    return replaced 
# mask below a certain threshold
def remove_below_thresh(thickness, thresh):
    replaced = thickness
    replaced[np.where(thickness <= thresh)] = np.nan       
    return replaced 
