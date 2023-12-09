# Velocity Flow Transformation Model for the Developmental Mouse Brain Common Coordinate Framework

## Description

A multimodal 3D developmental common coordinate framework (DevCCF) spanning 
mouse embryonic day (E) 11.5, E13.5, E15.5, E18.5, and postnatal day (P) 4, 
P14, and P56 with anatomical segmentations defined by a developmental ontology
is described in [Kronman et al.](https://www.biorxiv.org/content/10.1101/2023.09.14.557789v1).
At each age, the DevCCF features undistorted morphologically averaged atlas 
templates created from Magnetic Resonance Imaging and co-registered high-
resolution templates from light sheet fluorescence microscopy. Expert-curated 
3D anatomical segmentations at each age are [also available](). 
As part of this work, we generate a [diffeomorphic velocity flow model](https://en.wikipedia.org/wiki/Large_deformation_diffeomorphic_metric_mapping)
permitting deformations between the above mouse developmental stages and
at any continuous point within the developmental range.  The transformation
model is generated using the publicly available data provided through the
above cited work and using [ANTsX tools](https://github.com/ANTsX).  This
repository provides the scripts to both reproduce and utilize the velocity
flow field.

## Code usage

Before attempting to use any of the code found in this repository, please 
attempt to reproduce this small [self-contained example](https://gist.github.com/ntustison/12a656a5fc2f6f9c4494c88dc09c5621#file-b_3_ants_velocity_flows-md)
illustrating the code and principles used.  The idea is to create a time-
parameterized velocity flow model in the range $t=[0,1]$ from three 2-D point 
sets comprising 8 points each representing a rectangle at $t=0.0$, a square 
at $t=0.5$, and a circle at $t=1.0$.  The ANTsPy example should produce the 
following plots:

<p align="middle">
  <img src="https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/dbc63553-27ad-4130-8bbf-c10cdf8fc893" width="300" />
  <img src="https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/cd78595b-1e12-47fc-b606-ae4b5012cbd6" width="300" /> 
  <img src="https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/c7ee9ad6-1f3a-4da4-832e-ba64b1b15f31" width="300" /> 
</p>

<!--
![original_data](https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/dbc63553-27ad-4130-8bbf-c10cdf8fc893)
![warping_between_endpoints](https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/cd78595b-1e12-47fc-b606-ae4b5012cbd6)
![warping_to_middle](https://github.com/ntustison/MouseBrainVelocityFlow/assets/324811/c7ee9ad6-1f3a-4da4-832e-ba64b1b15f31)
-->



