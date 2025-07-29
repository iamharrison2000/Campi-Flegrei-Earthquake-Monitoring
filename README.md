Code:

phase_picking.py: 
Example of phase picking of station CAWE from 2024-01-01 to 2025-01-01 with retrained PhaseNet.

cleaning_phasent_picks.ipynb
Example of running quality control of the raw phases.

association.ipynb:
Example of using GaMMA is to run an earthquake association.



Models: 

1d_vmod_velest.mod:
1D velocity model file in VELEST format. Inverted with VELEST based on a subset of high quality earthquakes and further used as input for VELEST. 

3d_vmod:
3D velocity model files used for TomoDD relocation. 

phasenet_retrained.json, phasenet_retrained.pt:
.json contains model configuration and architecture.
.pt is the PyTorch model weights file.
Custom retrained PhaseNet model for Campi Flegrei seismic data.

stations.csv
CSV file listing station metadata (network, station code, channel type, latitude, longitude, elevation).

Used across waveform processing and model input generation.
Renamed from stations-2.csv.

stations_velest.dat
Station file in VELEST format. Contains station locations, elevations, and P/S phases station corrections for use with VELEST-based location routines.


