# FCC-ee Impedance Wake (IW) Model – 2026 Version

![CST Simulation](https://img.shields.io/badge/CST-✅-green)
![IW2D Simulation](https://img.shields.io/badge/IW2D-✅-green)
![ABCI Simulation](https://img.shields.io/badge/ABCI-✅-green)

**Folder:** `FCC_ee_IW_2026 model`  
**Optics considered:** `LCCv106`

**Description:**  
This file summarizes the components included in the FCC-ee impedance and wakefield model used in the 2026 version of the FCC_ee_IW model. The elements listed here represent the main impedance contributors. Wake and impedance calculations were performed using **CST Studio Suite** and **IW2D** where applicable.

All CST simulation input files are stored in the repository folder:
```bash
Simulation files/
```

---

## 📂 Model Components

<details>
<summary>1. Beam Position Monitors (BPMs)</summary>

### Beam Position Monitors (BPMs)

- **Number of elements:** 10,000 BPM units  
- **Description:** Distributed diagnostic devices used to measure transverse beam position along the ring. Their geometric structure produces broadband wakefields contributing to the overall machine impedance.  
- **Simulation method:** Full 3D electromagnetic wakefield simulation using CST Studio Suite  
- **Simulation input file:**
```text
Simulation files/BPM/BPM_trapezoid_button_vacuum_seal_4mm.cst
```
- **Notes:** Design development ongoing, new release expected soon. 

</details>

<details>
<summary>2. RF Cavities</summary>

### RF Cavities

- **Number of elements:** 132 RF cavities  
- **Description:** Double-cell RF cavities operating at 400 MHz  
- **Operating frequency:** 400 MHz  
- **Simulation method:** 3D CST wakefield simulation of the cavity geometry  
- **Simulation input file:**
```text
Simulation files/RF_cavity/TwoCell_elliptical_L180mm_400MHz.cst
```
- **Notes:** Short-range wakefields for single bunch dynamics assessment. Studies ongoing for a more advanced model.

</details>

<details>
<summary>3. Bellows</summary>

### Bellows

- **Number of elements:** Multiple sections distributed along the ring  
- **Description:** Compensate for thermal expansion and mechanical tolerances in the vacuum chamber. Their geometry introduces additional geometric impedance and wakefields. Bellows impedance is mitigated with RF fingers.  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:**
```text
Simulation files/Bellows/Bellows_70mm_diameter_400um_200mm.cst
```
- **Notes:** Current bellows model is obsolete (to be updated with the latest design).

</details>

<details>
<summary>4. Collimators</summary>

### Collimators

- **Number of elements:** 13 collimators  
- **Description:** Beam protection devices designed to intercept halo particles and protect sensitive machine components. Narrow apertures generate significant geometric and resistive-wall impedance contributions.  
- **Simulation methods:** IW2D flat chamber + analytical formula for taper transitions ([PyWIT repo](https://github.com/your-repo/PyWIT))  
- **Notes:** Only primary and secondary collimators included. Taper angle: 15°. Total impedance includes geometric and resistive-wall effects. Advanced CST models under development.

</details>

<details>
<summary>5. Beam Pipe</summary>

### Beam Pipe

- **Geometry:** Circular beam pipe  
- **Radius:** 30 mm  
- **Material:** 2 mm thick Copper  
- **Coating:** 150 nm NEG (Non-Evaporable Getter) layer  
- **Description:** Baseline vacuum chamber geometry throughout most of the machine. Resistive-wall impedance is a significant contributor to the broadband impedance of the accelerator.  
- **Simulation method:** IW2D calculations for round chamber combined with numerical form factors from CST to account for winglets ([PyWIT repo](https://github.com/your-repo/PyWIT))  
- **Simulation input files:**
```text
Simulation files/Beam_chamber/RoundPipe_dipx.cst
Simulation files/Beam_chamber/NoAbsorber_dipx.cst
```
- **Notes:** Includes both driving and detuning wakefield contributions, taking into account realistic vacuum chamber geometry.

</details>

<details>
<summary>6. Tapers</summary>

### RF Tapers

- **Number of elements:** 66 taper transitions (33 taper in + 33 taper out)  
- **Description:** Geometric transitions used to smoothly connect RF cavities and vacuum chamaber.
- **Simulation input files (ABCI):**
```text
Simulation files/RF_tapers/taper_out_ABCI.txt
Simulation files/RF_tapers/taper_in_ABCI.txt
```

</details>

---

## 📝 Summary Table

| Component      | Number       | Simulation Method       |
|----------------|--------------|------------------------|
| BPMs           | 10,000       | CST                    |
| RF Cavities    | 132          | CST                    |
| Bellows        | 10,000       | CST                    |
| Collimators    | 13           | Analytics + IW2D       |
| Beam Pipe      | 90,658.5 m   | IW2D + CST             |
| RF Tapers      | 66           | ABCI                   |

