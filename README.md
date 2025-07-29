# A Clearer View of the Current Phase of Unrest at Campi Flegrei Caldera

This repository is set up for the project **"A Clearer View of the Current Phase of Unrest at Campi Flegrei Caldera."** It includes example scripts, retrained PhaseNet models, velocity models, and processed outputs in our earthquake monitoring workflow.

---

## Code

- **`phase_picking.py`**  
  Example of phase picking for station CAWE from 2024-01-01 to 2025-01-01 using the retrained PhaseNet model. (Note that the retrained model was trained on seismograms applied with a highpass filter (1Hz).)

- **`cleaning_phasent_picks.ipynb`**  
  Example notebook for quality control of raw phase picks.

- **`association.ipynb`**  
  Example of running earthquake association using GaMMA.

---

## Models

- **`1d_vmod_velest.mod`**  
  1D velocity model file in VELEST format. Inverted with VELEST using a subset of high-quality earthquakes and used as input for VELEST-based relocations.

- **`3d_vmod/`**  
  Folder containing 3D velocity model files used for TomoDD relocation.
  - J. Battaglia, A. Zollo, J. Virieux, D. D. Iacono, Merging active and passive data sets in traveltime tomography: the case study of Campi Flegrei caldera (Southern Italy). Geophysical Prospecting 56, 555–573 (2008).


- **`phasenet_retrained.json`, `phasenet_retrained.pt`**  
  - `.json`: Contains model configuration and architecture.  
  - `.pt`: PyTorch model weights.  
  Retrained PhaseNet model for Campi Flegrei seismic data. (Note that the retrained model was trained on seismograms applied with a highpass filter (1Hz).)

- **`stations.csv`**  
  CSV file listing station metadata: network, station code, channel type, latitude, longitude, and elevation.  
  Used across waveform processing and model input generation.  

- **`stations_velest.dat`**  
  Station file in VELEST format, including station locations, elevations, and P/S phase corrections for VELEST-based location routines.

---

## Output

- **`associated_phases.csv.zip`**  
  Associated phases of cataloged events.

- **`catalog.csv`**  
  Contains information on 54,319 seismic events, including origin time, relocated coordinates, local magnitude, azimuthal gap, and other event parameters.  
  Values such as `NCCP`, `NCCS`, `NCTP`, `NCTS`, `RCC`, and `RCT` are reported by TomoDD.  
  Coordinates `x (km)` and `y (km)` are relative to the reference point (14.14°E, 40.82°N).

- **`focal_mechanism.csv`**  
  Focal mechanism solutions computed from gCAP and SKHASH.  
  - From SKHASH: `strike_skhash`, `dip_skhash`, `rake_skhash`, `quality`, `fault_plane_uncertainty`, `aux_plane_uncertainty`, `num_p_pol`, `num_sp_ratios`, `polarity_misfit`, `prob_mech`, `sta_distribution_ratio`, `sp_misfit`, `mult_solution_flag`, `origin_depth_km`, `horz_uncert_km`, `vert_uncert_km`.  
  - From gCAP: `strike_gcap`, `dip_gcap`, `rake_gcap`.

- **`polarity.csv`**  
  Polarity and S/P amplitude ratio readings of large earthquake traces.  
  Used as input for SKHASH to compute focal mechanism solutions.

- **`s1.html`**
  Interactive 3D plots of the seismicity. 
