import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import cmocean

# plot salinity
def plot_salinity(lat_scalar,lon_scalar,salinity,label):
    min_val = 27
    max_val =35
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
    m.drawcoastlines(color='aliceblue',linewidth=0.7) # draw the coastlines in 'alice blue' 
    
    barlim = np.arange(min_val,max_val,1) # this is the range of the colorbar
    
    cmap = cmocean.cm.haline # set colourmap

    # creates contours for every 0.5 PSU from 27 to 35 PSU
    cs = m.contourf(lon_scalar,lat_scalar, salinity, np.arange(min_val,max_val,0.5),extend='max', alpha=1,latlon=True,cmap=cmap)
  
    # creates the title
    t = plt.annotate(label,textcoords='axes fraction',
                xy=(0,0), xytext=(-0.4,0.85),
            fontsize=20,color='k')
    # creates the colourbars
    cbar = m.colorbar(cs,drawedges=True,location='bottom',pad = 0.14,size=0.07)
    # creates the ticks for the colourbars
    ticks = np.arange(min_val,max_val,1)
    cbar.set_ticks(ticks)
    
    # sets label under the colourbar
    cbar.set_label('Salinity (psu)',fontsize=10,color='k')
    cbar.ax.tick_params(axis='x', size=.01)
    cbar.ax.tick_params(labelsize=6) 
    plt.rcParams['axes.linewidth'] = 0.1
    return m, myfig
