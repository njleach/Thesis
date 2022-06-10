## Dependencies
import numpy as np
import scipy as sp
import seaborn as sn
import pandas as pd
import time
from tqdm import tqdm
import os
import xarray as xr
import gc
import multiprocessing

from mystatsfunctions import OLSE,LMoments

## Define system
def lorenz(xyz, t, rho=28, sigma=10, beta=8/3, F=0, theta=0):
    
    "Defines the lorez63 dynamical system. Standard default values."
    
    x, y, z = xyz
    x_dot = sigma * (y - x) + F * np.cos(theta)
    y_dot = x * rho - x * z - y + F * np.sin(theta)
    z_dot = x * y - beta * z
    return [x_dot, y_dot, z_dot]


## set solver parameters
## run over this many ICs to generate branches
branches = 101

# set Lorenz system + forcing parameters
s = 10
r = 28
b = 8/3
F = (8,np.deg2rad(-40))

## original ICs
IC0 = [0.01,0,0]
IC1 = IC0[:]

## ICs if restarting mid-integration
# start_from = 42
# X = xr.open_dataset('Lorenz63-realisations/00'+str(start_from)+'.nc')
# IC0 = X.isel(time=0).sel(type='unforced').to_array().values.flatten()
# IC1 = X.isel(time=0).sel(type='forced').to_array().values.flatten()

for branch in tqdm(np.arange(branches)[:]):
    
    runlength = 100000
    timestep = 0.01
    start = branch * runlength
    end = (branch+1) * runlength
    timeindex = np.arange(start,end,timestep)
    
    # unforced system
    X0 = sp.integrate.odeint(lorenz, IC0, np.arange(0,runlength+timestep,timestep), (r,s,b,0,0)).reshape(-1,1,3)
    IC0 = X0[-1,0,:]
    X0 = xr.DataArray(data=X0[:-1],dims=['time','branch','dim'],coords=dict(time=timeindex,branch=[branch],dim=['x','y','z'])).to_dataset(dim="dim")

    # system with external forcing
    ## define forcing in terms of magnitude + direction
    X1 = sp.integrate.odeint(lorenz, IC1, np.arange(0,runlength+timestep,timestep), (r,s,b,*F)).reshape(-1,1,3)
    IC1 = X1[-1,0,:]
    X1 = xr.DataArray(data=X1[:-1],dims=['time','branch','dim'],coords=dict(time=timeindex,branch=[branch],dim=['x','y','z'])).to_dataset(dim="dim")

    X = xr.concat([X0.expand_dims({'type':['unforced']}),X1.expand_dims({'type':['forced']})],dim='type')
    
    X.to_netcdf('./Lorenz63-realisations/'+f"{branch:04d}"+'.nc')