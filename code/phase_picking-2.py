import glob as glob
import numpy 
import obspy
import seisbench
import seisbench.models as sbm
import datetime
from obspy import UTCDateTime
from scipy.signal import spectrogram
import numpy as np
from datetime import datetime, timedelta
import sys
import torch
import pandas as pd
import os

df_stations = pd.read_json('new_stations.json')
ch_dict = {}
for one_station in df_stations.columns:
    if one_station == 'IV.CSTH..EH':
        continue
    ch_dict[one_station.split('.')[1]] = one_station.split('.')[-1]

def compute_date(date_string = "2023-02-06"):
    # Define the date
    date_format = "%Y-%m-%d"

    # Convert string to datetime
    date_obj = datetime.strptime(date_string, date_format)

    # Compute the day of the year
    day_of_year = date_obj.timetuple().tm_yday

    return day_of_year


def pick_one_trace(pn_model, station_name, one_trace, overlap, year, n=0, stacking='max'):    
    frequency_band = {
        1:{'type':'highpass', 'freq':1},
        2:{'type':'bandpass', 'freqmin':2.5, 'freqmax':25}
    }

    flag = 1
    stream = obspy.read(one_trace)
    if station_name == 'V0102':
        stream.resample(100, no_filter=False)
    dir_name0 = './phases'
    if not os.path.exists(dir_name0):
        os.makedirs(dir_name0)
    dir_name = f'./phases/phase_seisbench_{year}'
    # Check if the directory already exists
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(dir_name+f'/{station_name}_trace.txt', 'a') as f:
        for trace in stream:
            fmt = '%Y-%m-%d %H:%M:%S.%f'
            f.write(f"{trace.stats.starttime.strftime(fmt)} {trace.stats.endtime.strftime(fmt)}\n")
            if trace.stats.npts>=3000:
                flag=0
    if flag==1:
        print('Traces all too short!')
        return

    stream.merge(method=1, interpolation_samples=2)
    stream = stream.split()
    stream.detrend('linear')
    stream.detrend('constant')
    stream = stream.filter('bandpass', zerophase=True, 
                                        freqmin=1, freqmax=49)
    stream.merge(fill_value=0)
    channel_type = stream[0].stats.channel[:2]
    pn_pred = pn_model.annotate(stream, parallelism=n, overlap=overlap, stacking=stacking)
    
    pn_preds = []
    pn_preds.append(pn_pred)
    # stream = stream.split()
    st = pn_pred[0].stats.starttime
    et = pn_pred[0].stats.endtime
    
    if False:
        for key, filter_spec in frequency_band.items():
            
            if filter_spec['type'] == 'bandpass':
                stream = stream.filter('bandpass', zerophase=True, 
                                        freqmin=filter_spec['freqmin'], freqmax=filter_spec['freqmax'])
            else:  # highpass
                stream = stream.filter(filter_spec['type'], zerophase=True,  freq=filter_spec['freq'])
            stream.merge()
            pn_pred = pn_model.annotate(stream, parallelism=n,overlap=overlap, stacking=stacking)
            stream = stream.split()
            stream.detrend('linear')
            pn_preds.append(pn_pred.trim(st, et, pad=True, fill_value=0))

    pn_preds_final = pn_preds[0]
    # pn_preds_final = pn_preds[0].copy()
    # if len(pn_preds[0])!=0:
    #     pn_preds_final[1].data = np.max(np.array([pred[1].data for pred in pn_preds]), axis=0)
    #     pn_preds_final[2].data = np.max(np.array([pred[2].data for pred in pn_preds]), axis=0)
    #     pn_preds_final[0].data = np.maximum(0, (1 - pn_preds_final[1].data - pn_preds_final[2].data))
    
    output = pn_model.classify_aggregate(pn_preds_final, {'P_threshold': 0.2, 'S_threshold': 0.2})
    
    pick_list = []
    for each_pick in output.picks:
        pick_list.append([each_pick.trace_id + channel_type, each_pick.peak_value, 
                          each_pick.peak_time.datetime, each_pick.phase, 
                          each_pick.start_time.datetime, each_pick.end_time.datetime])
    
    # Write the list into a txt file named station_picks.txt
    with open(dir_name+f'/{station_name}_picks.txt', 'a') as f:
        for each_pick in output.picks:
            fmt = '%Y-%m-%d %H:%M:%S.%f'
            content = f"{each_pick.trace_id}{channel_type} {each_pick.peak_value:.3f} {each_pick.peak_time.strftime(fmt)} {each_pick.phase} "    
            f.write(f"{content}\n")
    
    print(f'{one_trace} processing finished.')


# print(sys.argv)

# Define the start and end dates
year=2024
start_date = datetime.strptime('2024-10-1', '%Y-%m-%d')
end_date = datetime.strptime('2024-12-31', '%Y-%m-%d')
# Generate the list of dates
date_generated = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
# Convert dates to strings
date_list = [date.strftime('%Y-%m-%d') for date in date_generated]
# Printing the list
start_date_num = compute_date(date_list[0])
end_date_num = compute_date(date_list[-1])

#get all of the waveforms
path_dir = f'../napoli/waveforms_web/{year}'
all_stations = glob.glob(f'{path_dir}/*')
station_names = [station_dir.split('/')[-1] for station_dir in all_stations]
stacking = 'max'

# station_names = ['CFB1', 'CFB3']
# pn_model100 = sbm.PhaseNet.from_pretrained("original")
# index = int(sys.argv[1])
# one_station = station_names[index]
one_station = 'CAWE'
station_ch = ch_dict[one_station]
station_ch = 'HH'

pn_model100 = sbm.PhaseNet.load("../napoli/phasenet_model/phasenet_ce_1119_clean_149_narrow_noisy")
# pn_model100.norm_detrend=True
pn_model100.norm = 'peak'
pn_model100.norm_amp_per_comp = True

pn_model100.sampling_rate = 100
torch.set_num_threads(1)
path2wf = f'{path_dir}/{one_station}/integrate/*{station_ch}*'
station_wf = glob.glob(f'{path2wf}')
station_wf.sort()
fs = 100

overlap=fs*28
# print(station_wf)
for one_trace in station_wf:
    if (int(one_trace.split('.')[-2]) >= start_date_num) and (int(one_trace.split('.')[-2]) <= end_date_num):
        # print('y')
        pick_one_trace(pn_model = pn_model100, overlap=overlap, n=1, stacking=stacking, year=year,
                       station_name=one_station, one_trace=one_trace)
print(one_station+' finished!')