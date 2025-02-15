#!/usr/bin/env python

import os
import pickle

import georinex
import gtsam
import gtsam_gnss
import numpy as np
import pandas as pd
import xarray as xr

# Set example data path.
script_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(script_dir, 'data')

# Read RINEX observation/navigation file.
#
# Note: The georinex parser is very slow. For example, reading the example rover_1Hz.obs takes over a minute, and much
# longer in the debugger. We cache the returned data for faster future loading.
def load_rinex(path):
    cache_path = os.path.realpath(path) + '.pkl'
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    else:
        print(f'Loading {path}. This may take a few minutes...')
        result = georinex.load(path)
        with open(cache_path, 'wb') as f:
            pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)
        return result

obs = load_rinex(os.path.join(data_path, "rover_1Hz.obs"))
nav = load_rinex(os.path.join(data_path, "base.nav"))

# Make the time step of the observation constant (insert NaN)
def fixed_interval(obs: xr.Dataset) -> xr.Dataset:
    dt_ns = np.diff(obs.time)
    min_dt_ns = np.min(dt_ns)
    missing_idx = np.where(dt_ns > min_dt_ns)[0] + 1
    for i in missing_idx:
        gap_start = obs.time[i - 1].values + min_dt_ns
        gap_end = obs.time[i].values - min_dt_ns
        missing_times = np.arange(gap_start, gap_end, min_dt_ns)
        missing_time_da = xr.DataArray(missing_times, dims=["time"], coords=[missing_times])
        full_time = xr.concat([obs.time, missing_time_da], dim="time")
        obs = obs.reindex(time=full_time, fill_value=np.nan).sortby("time")
    return obs

# Extract data info.
dt_sec = (obs.time[1] - obs.time[0]).item() * 1e-9
num_epochs = len(obs)
num_sat = len(obs.sv)
num_sys = len(np.unique([sv[0] for sv in obs.sv.values]))

# Read reference position
ref = pd.read_csv(os.path.join(data_path, "reference.csv"))
orgllh = ref.iloc[0, 2:5].to_numpy()

# TODO Need RTKLIB to evaluate ephemeris...
pass
