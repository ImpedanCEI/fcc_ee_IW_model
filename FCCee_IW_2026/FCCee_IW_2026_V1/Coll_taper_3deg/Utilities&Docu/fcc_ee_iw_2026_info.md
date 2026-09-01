# FCC-ee Impedance Wake (IW) Model – 2026 Version

![CST Simulation](https://img.shields.io/badge/CST-✅-green)
![IW2D Simulation](https://img.shields.io/badge/IW2D-✅-green)
![ABCI Simulation](https://img.shields.io/badge/ABCI-✅-green)

**Folder:** `FCC_ee_IW_2026_V1`   
**Optics considered:** `LCCv106`

**Important** : the recommended version of the wake file to be used for beam dynamics simulations is the **Wtotal_xwakes_recommented.txt**
and **Wtotal_pyheadtail_recommended.txt** in Wakes/Total with the following elements described here, considering the optimized version of the kickers, without the vacuum flanges and electromagnetic separator.

While the **Wtotal_pyheadtail_all.txt** or **Wtotal_xwakes_all.txt** is the same but only without the vacuum flanges.

While the **Wtotal_pyheadtail_noRF_noEMS.txt** or **Wtotal_xwakes_noRF_noEMS.txt** is the same but  without the vacuum flanges, RF and electromagnetic separator.

**Description:**  
This file summarizes the components included in the FCC-ee impedance and wakefield model used in the 2026 version of the FCC_ee_IW model. The elements listed here represent the main impedance contributors. Wake and impedance calculations were performed using **CST Studio Suite**, **IW2D**, **ABCI**, and analytical formulas where applicable.

All CST simulation input files are stored in the repository folder:
```bash
Simulation files/
```

---

## 📂 Model Components

<details>
<summary>1. Beam Position Monitors (BPMs)</summary>

### Beam Position Monitors (BPMs)

- **Number of elements:** 2220 arcs BPM  
- **Description:** Distributed diagnostic devices used to measure transverse beam position along the ring.
- **Simulation method:** 3D CST wakefield simulation 
- **Simulation input file:**
```text
Simulation files/BPM/BPM_trapezoid_button_vacuum_seal_4mm.cst
```
- **Notes:** Design development ongoing (more [here](https://indico.cern.ch/event/1552126/timetable/#152-status-of-the-arc-bpm-desi)), new impedance release expected soon.

</details>

<details>
<summary>2. RF Cavities</summary>

### RF Cavities

- **Number of elements:** 33 cryomodules  
- **Description:** Each cryomodules is composed by 4 double-cell RF cavities operating at 400 MHz, for a total of 132 cavitites. The 2026 version includes a further improved RF cavity impedance model with modes considered up to 3 GHz.  
- **Simulation method:** 3D CST wakefield and eigenmode simulations  
- **Simulation input file:**
```text
Simulation files/RF_cavity/TwoCell_elliptical_L180mm_400MHz.cst
```
- **Notes:** Updated model w.r.t the IW_2026_V0 with simulations up to 3 GHz. To be refined. More detailed about current model [here ](https://indico.cern.ch/event/1552126/timetable/#285-studies-on-the-longitudina)

</details>

<details>
<summary>3. Interconnecting modules</summary>

### Interconnecting modules

- **Number of elements:** 4384 bellows units  
- **Description:** Compensate for thermal expansion and mechanical tolerances in the vacuum chamber. 
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:**
```text
Simulation files/Bellows/Interconnect_LoopedRFFingers_oval_long.cst
```
- **Notes:** Updated model w.r.t the IW_2026_V0 version from vacuum, more details by P. Krkotic [here](https://indico.cern.ch/event/1552126/timetable/#79-impedance-considerations-fo).

</details>

<details>
<summary>4. Collimators</summary>

### Collimators

- **Number of elements:** 40 collimators  
- **Description:** Beam protection devices designed to intercept halo particles and protect sensitive machine components.
- **Simulation methods:** 3D CST electromagnetic simulation   
- **Notes:** Primary, secondary tertiary and SR collimators included from last version with LCC106 optics (see [here](https://indico.cern.ch/event/1552126/contributions/7132598/attachments/3291994/5886565/FCCweek2026_GB.pdf)). Taper angle: 3° and Collimator lenght of 3 cm.
</details>

<details>
<summary>5. Beam Pipe</summary>

### Beam Pipe

- **Geometry:** Circular beam pipe  
- **Length:** 90,658.5 m  
- **Radius:** 30 mm  
- **Material:** 2 mm thick Copper  
- **Coating:** 150 nm NEG (Non-Evaporable Getter) layer  
- **Description:** Baseline vacuum chamber geometry throughout most of the machine.   
- **Simulation method:** IW2D calculations for round chamber combined with numerical form factors from CST to account for winglets ([PyWIT repo](https://github.com/your-repo/PyWIT))  
- **Simulation input files:**
```text
Simulation files/Beam_chamber/RoundPipe_dipx.cst
Simulation files/Beam_chamber/NoAbsorber_dipx.cst
```
- **Notes:** Includes both driving and detuning wakefield contributions, taking into account realistic vacuum chamber geometry.

</details>

<details>
<summary>7. Stripline Kickers</summary>

### Stripline Kickers

- **Number of elements:** 12 stripline kickers  
- **Description:** Stripline kicker impedance model. The model considers a half-aperture between electrodes of 26 mm.  
- **Half-aperture between electrodes:** 26 mm  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:**
```text
Simulation files/Stripline_kickers/
```
- **Notes:** Model with new electrodes aperture, see more [here ](https://indico.cern.ch/event/1552126/timetable/#300-rf-kicker-design-for-trans).

</details>

<details>
<summary>8. Injection and Extraction Kickers</summary>

### Injection and Extraction Kickers
Non optimized version, named Z_*kickers in repository:
    - **Total length:** 40 m  
    - **Description:** FCC kickers system based on window frame magnet design without shielding of the ferrite.  
    - **Simulation method:** Analytical formula  
    - **Simulation input file:**
    ```text
    Simulation files/Injection_extraction_kickers/
    ```
    - **Notes:** The impedance contribution is preliminarly computed with an analytical model (Tsutsui formalism). A more detailed numerical model may be introduced in future releases.

Optimized version named Z_*kickers_opt in repository:
    - **Total length:** 40 m  
    - **Description:** FCC kickers system based on window frame magnet design with 1 micron shielding of the ferrite.
    - **Simulation method:** 3D CST electromagnetic simulation
    - **Simulation input file:**
 
    - **Notes:**Simulations currently ongoing, the input file will be released soon.


</details>

<details>
<summary>9. Synchrotron Radiation Absorbers</summary>

### Synchrotron Radiation Absorbers

- **Number of elements:** 13,140 SR absorbers  
- **Description:** Synchrotron radiation absorbers distributed around the ring. 
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:**
```text
Simulation files/SR_absorbers/SRA_40cm_long.cst
```
- **Notes:** Added as a new impedance contributor in the 2026 model, see more [here](https://indico.cern.ch/event/1552126/timetable/#79-impedance-considerations-fo).

</details>

<details>
<summary>10. Vacuum Flanges</summary>

### Vacuum Flanges

- **Number of elements:** 13,140 vacuum flanges  
- **Description:** Vacuum flanges used to connect vacuum chamber sections.  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:**
```text
Simulation files/Vacuum_flanges/SMA_flange_02mm_gap_long.cst
```
- **Notes:** Added as a new distributed impedance contributor in the 2026 model, see  [here](https://indico.cern.ch/event/1552126/timetable/#79-impedance-considerations-fo).


<details>
<summary>12. Interaction Region (IR)</summary>

### Interaction Region (IR)

- **Number of elements:** 4 interaction regions  
- **Description:** Interaction region impedance contribution, considered four times to account for the four FCC-ee experimental regions.  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:**
```text
Simulation files/Interaction_region/
```
- **Notes:** Model based on the development of a preliminary design which features: central beam pipe, ellipto-conical chamber, Y chamber and lateral chamber with two 2 SR masks. See more [here](https://indico.cern.ch/event/1552126/timetable/#249-interaction-region-impedan).

</details>

---

## 📝 Summary Table

| Component                       | Number / Length                | Simulation Method       |
|---------------------------------|--------------------------------|-------------------------|
| BPMs                            | 2,200                          | CST                     |
| RF Cavities + Tapers            | 33 cryo-modules                | CST                     |
| Int. modules                    | 4384                           | CST                     |
| Collimators                     | 13                             | Analytics + IW2D        |
| Beam Pipe                       | 90,658.5 m                     | IW2D + CST              |
| Stripline Kickers               | 12                             | CST                     |
| Injection / Extraction Kickers  | 38 m                           | Analytical              |
| SR Absorbers                    | 13,152                         | CST                     |
| Vacuum Flanges                  | 13,152                         | CST                     |
| Interconnecting Modules         | 4,384                          | CST                     |
| Interaction Region (IR)         | 4                              | CST                     |

---

