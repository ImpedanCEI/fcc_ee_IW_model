# FCC-ee Impedance/Wake Model

This repository contains the updated impedance and wake conttubutions from different elements 

## Status (updated 29.04.2025)

The impedance model represents the cumulative electromagnetic interaction between the beam and surrounding accelerator structures.

Each element shapes the overall impedance spectrum, directly impacting beam dynamics and potentially leading to instabilities.

- Included elements:
  - Beam pipe: circular copper cross-section with a radius of 30 mm coated with a thin 150 nm layer of Non-Evaporable Getter (NEG)
  -  IW2D + numerical form factor for both driving and detuning
    impedance/wake, considering the realistic shape of the vacuum chamber.    
  - Collimators: Geometrical (CST) and RW (IW2D) contributions are considered.
    Approximation using a linear taper - Version 2023 of the collimation optics is considered.
  - 10000 BPMs
  - 10000 bellows
  - 132 single-cell 400 MHz RF cavities
  - 33 tapers
