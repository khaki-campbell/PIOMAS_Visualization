# Functions to package salinity (osali1_10) binary files from https://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/data/model_grid
# into netCDFs
import struct 
import xarray as xr
import numpy as np
import pandas as pd

# Input a list of years
def process_piomas_list(years, input_directory, output_directory):
    dims = (120,360)
    grids = define_grid()
    for year in years:
        process_piomas(year,  input_directory, output_directory, grids)

# A latititude and longitude grid is necessary, this is the one downloaded from the PIOMAS website. 
# if this fails, pull the latitude/longitude grid from the ice thickness netCDFs (heff)
def define_grid():
    dims = (120,360)
    grids = {}
    for i in ['lon','lat']:    
        grid = np.array(pd.read_csv('/Users/lilymueller/Desktop/Beaufort/PIOMAS/Variables/grid.txt',
                                header=None,
                                delim_whitespace=True))

        flat_grid = grid.ravel()
    
        if i == 'lat':
            shaped_grid = flat_grid[:43200].reshape(dims)
        else:
            shaped_grid = flat_grid[43200:86400].reshape(dims)
        
        grids[i] = shaped_grid
    return grids

# Reformat into netCDF 
def process_piomas(year, in_directory, output_dir, grids):
# (2, months, 10, dims[0], dims[1])
    dims = (120,360)
    version = '_V2'
    binary_dir = in_directory + f'osali1_10.H{year}'
    ############################################################
    ### For monthly datasets ###
    months=12
    
    # Read File
        
    with open(binary_dir, mode='rb') as file:
    
        fileContent = file.read()
        
        
        if len(fileContent) % 4 != 0:
            print("Error: Invalid file size.")
            exit()
        
        data = struct.unpack("f" * (len(fileContent)// 4), fileContent) # modify 8? try that
        
       # print(len(data)/months)
        
        if len(data) % months != 0:
            print("Error: Invalid data length.")
            exit()
    ############################################################
    
    # Put it in a 3D array

        native_data = np.full(( months, 10, dims[0], dims[1]), np.nan)

        for month in range(1, months+1):
            start = (month - 1) * (dims[0] * dims[1])*10 #+ 518400 # remove the 2
            end = month * (dims[0] * dims[1])*10 #+ 518400
            
            # Ensure indices are within bounds
            if end <= len(data):
                thickness_list = np.array(data[start:end])
               
                # Reshape the flattened data to a 2D array
                gridded = thickness_list.reshape(10, dims[0], dims[1]) # problem occurs
        
                # Store the gridded data in the 3D array
                native_data[ month - 1,:, :, :] = gridded
                #native_data[ 1,month - 1, :, :,:] = gridded[1]
                
            else:
                print(f"Error: Data for month {month} is out of bounds.")
                
        
    # Output to NetCDF4

        ds = xr.Dataset( data_vars={'osali1_10':(['m','layer','x','y'],native_data)},
                      #   data_vars={'u':(['t', 'layer','x','y'],native_data[0])},
                         coords =  {'longitude':(['x','y'],grids['lon']),
                                    'latitude':(['x','y'],grids['lat']),
                                    'month':(['t'],np.array(range(1,months+1)))})
        
        ds.attrs['data_name'] = 'Monthly mean Piomas Salinity data'
        
        ds.attrs['description'] = """Ocean Salinity in psu on the lat/lon grid, 
                                    data produced by University of Washington Polar Science Center"""
        
        ds.attrs['year'] = f"""These data are for the year {year}"""
        
        ds.attrs['citation'] = """
                                Zhang, Jinlun and D.A. Rothrock: Modeling global sea 
                                ice with a thickness and enthalpy distribution model 
                                in generalized curvilinear coordinates,
                                Mon. Wea. Rev. 131(5), 681-697, 2003."""
        
        ds.attrs['code to read'] = """  # Example code to read a month of this data 
    
                                        def read_month_of_piomas(year,month):
    
                                            data_dir = 'output/' 

                                            with xr.open_dataset(f'{data_dir}{year}.nc') as data: 

                                                ds_month = data.where(int(month) == data.month, drop =True) 

                                                return(ds_month)"""
        
        ds.to_netcdf(f'{output_dir}{year}.nc','w')

    return native_data
