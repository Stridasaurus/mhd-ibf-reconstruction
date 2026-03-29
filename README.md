# mhd-ibf-reconstruction
A computational framework designed to reconstruct 3D wave fields in the magnetosphere using ground-based magnetometer array data. This project implements Generalized Inverse Beamforming (GIBF) to identify source distributions and characterize MHD wave propagation.


The project is divided into two main phases:

**Phase 1 – The Control**  
- Define a 3D space and generate wave pulses with known parameters.  
- Simulate time series at selected spatial points.  
- Apply FFT to isolate spectral signals.  
- Use IBF to reconstruct the wave and compare with the original.

**Phase 2 – The Experiment**  
- Apply the same IBF approach to real magnetometer time series collected from Earth’s surface.  - Reconstruct MHD waves from the data.
