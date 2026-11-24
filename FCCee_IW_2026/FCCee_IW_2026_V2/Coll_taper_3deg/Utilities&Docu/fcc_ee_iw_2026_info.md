# FCC-ee Impedance Wake (IW) Model – 2026 Version

![CST Simulation](https://img.shields.io/badge/CST-✅-green)
![IW2D Simulation](https://img.shields.io/badge/IW2D-✅-green)
![ABCI Simulation](https://img.shields.io/badge/ABCI-✅-green)

**Folder:** `FCCee_IW_2026_V2/Coll_taper_3deg`   
**Release:** `V2.c` (see [releases](https://github.com/ImpedanCEI/fcc_ee_IW_model/releases))   
**Optics considered:** `LCCv106`

**Important:** From V2.c, **two recommended wakes** are provided for beam-dynamics simulations, located in *`Wakes/Total/`*:

* **recommended1** (rough pipe + **optimized collimators**):
  * **`Wtotal_xwakes_recommended1.txt`**
  * **`Wtotal_pyheadtail_recommended1.txt`**

* **recommended2** (rough pipe + **non-optimized collimators**):
  * **`Wtotal_xwakes_recommended2.txt`**
  * **`Wtotal_pyheadtail_recommended2.txt`**

Both files contain the wake contributions from **all devices included in the model**, as described in the following sections, using the **optimized kicker** version, the **beam pipe with surface roughness** (Rq = 0.3 µm) and the new **beam instrumentation** (BPMs, electro-optical and beamstrahlung monitors). The **vacuum flanges** and **electromagnetic separator (EMS)** are excluded.

The **only difference** between the two is the collimator model:

| Recommended wake   | Beam pipe                   | Collimators                                                  |
|--------------------|-----------------------------|--------------------------------------------------------------|
| **recommended1**   | RW + roughness (`Rq03`)     | **Optimized** (`collSA3cmOpt`): coated TCS, TCT and TCR       |
| **recommended2**   | RW + roughness (`Rq03`)     | **Not optimized** (`collSA3cm`)                               |

For completeness, additional total wake files are provided, **each in two versions** following the same collimator convention (**1** = optimized collimators, **2** = non-optimized collimators):

* **`Wtotal_xwakes_all1.txt`** / **`Wtotal_pyheadtail_all1.txt`** and **`Wtotal_xwakes_all2.txt`** / **`Wtotal_pyheadtail_all2.txt`**
  These contain the **same device contributions as recommended1 and recommended2** respectively, but with the **EMS included**. The **vacuum flanges remain excluded**.

* **`Wtotal_xwakes_recommended1_noRF.txt`** / **`Wtotal_pyheadtail_recommended1_noRF.txt`** and **`Wtotal_xwakes_recommended2_noRF.txt`** / **`Wtotal_pyheadtail_recommended2_noRF.txt`**
  These contain the **same device contributions as recommended1 and recommended2** respectively, but with the **RF cavities** **excluded** (The **vacuum flanges and EMS remain excluded**).

| Configuration | Collimators optimized (`collSA3cmOpt`) | Collimators not optimized (`collSA3cm`) |
|---------------|----------------------------------------|-----------------------------------------|
| Recommended   | **recommended1**                       | **recommended2**                        |
| All (EMS included) | **all1**                          | **all2**                                |
| No RF         | **recommended1_noRF**                  | **recommended2_noRF**                   |

In all configurations, the **optimized kicker** impedance/wake contribution, the **beam pipe with roughness** and the **beam instrumentation** are used.

The same configurations and naming convention apply to the corresponding impedance files located in *`Impedances/Total/`*.


**Description:**  
This file summarizes the components included in the FCC-ee impedance and wakefield model used in the 2026 version of the FCC_ee_IW model. The elements listed here represent the main impedance contributors. Wake and impedance calculations were performed using **CST Studio Suite**, **IW2D**, **ABCI**, and analytical formulas where applicable.

---

## 🏷️ V2 releases

| Tag      | What it adds |
|----------|--------------|
| `V2`     | Optimized kicker (realistic 3D model, coating, 20 m), shower absorbers of the collimators, recommended wake |
| `V2.a`   | Fixes in a few wake data (single and total), RW impedance extended up to 300 GHz |
| `V2.b`   | RW impedance and wake with surface roughness (Rq = 0.3 µm), impedances resampled, Git LFS no longer needed |
| `V2.c`   | New BPM model, electro-optical and beamstrahlung monitors, optimized collimators, two recommended wakes (**recommended1** and **recommended2**) |

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
- **Notes:** New BPM model released in V2.c. Design development ongoing (more [here](https://indico.cern.ch/event/1552126/timetable/#152-status-of-the-arc-bpm-desi)).

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
- **Simulation input file:** *To be redesigned.*

- **Notes:** Updated model w.r.t the IW_2026_V0 version from vacuum, more details by P. Krkotic [here](https://indico.cern.ch/event/1552126/timetable/#79-impedance-considerations-fo).

</details>

<details>
<summary>4. Collimators</summary>

### Collimators

- **Number of elements:** 40 collimators  
- **Description:** Beam protection devices designed to intercept halo particles and protect sensitive machine components.
- **Simulation methods:** 3D CST electromagnetic simulation   
- **Notes:** Primary, secondary, tertiary, synchrotron radiation and shower absorbers collimators included from last version with LCC106 optics (see [here](https://indico.cern.ch/event/1552126/contributions/7132598/attachments/3291994/5886565/FCCweek2026_GB.pdf)). Taper angle: 3° and Collimator lenght of 3 cm. More info about the collimator materials can be found [here] (https://indico.cern.ch/event/1604870/contributions/6763283/attachments/3175979/5648123/251118_Update_Collimators_Impedance_Studies_Gibellieri.pdf)

**Two versions** are available from V2.c:

* **Optimized version**, named `Z_*_collSA3cmOpt` in the repository: coating of the secondary, tertiary and SR absorbers (**TCS, TCT, TCR**). Used in **recommended1**.
* **Non-optimized version**, named `Z_*_collSA3cm` in the repository. Used in **recommended2**.

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
- **Surface roughness:** Impedance and wake data including surface roughness are available (since V2.b), based on a preliminary roughness model using the gradient model.  
  An RMS roughness (Rq) of 0.3 µm is assumed, to be confirmed by future measurements.  
  Files: `Z_*_pipe_rw_Rq03` (impedances) and `W_pipe_RW_Rq03.txt` (wake).  
  The **rough pipe is used in both recommended wakes** (recommended1 and recommended2).

- **Notes:** Includes both driving and detuning wakefield contributions, taking into account realistic vacuum chamber geometry.

</details>

<details>
<summary>6. Electro-Optical (EO) Monitor</summary>

### Electro-Optical (EO) Monitor

- **Number of elements:** 1 per beam  
- **Description:** Beam instrumentation device with a copper winglet chamber, new in V2.c, named `Z_*_EOmonitor` in the repository.  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:** *To be released soon.*

- **Notes:** Preliminary design. Included in both recommended wakes.

</details>

<details>
<summary>7. Stripline Kickers</summary>

### Stripline Kickers

- **Number of elements:** 12 stripline kickers  
- **Description:** Stripline kickers for depolarizer and feedback system. The model considers a half-aperture between electrodes of 26 mm.  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:** *To be released soon.*

- **Notes:** Model for 25 ns filling scheme, see more [here ](https://indico.cern.ch/event/1552126/timetable/#300-rf-kicker-design-for-trans).

</details>

<details>
<summary>8. Injection and Extraction Kickers</summary>

### Injection and Extraction Kickers

**Optimized version**, named `Z_*optimizedkicker` in the repository:

* **Total length:** 20 m (reduced length w.r.t. V1)
* **Description:** FCC kickers system based on a window-frame magnet design with a 1 µm titanium coating on the ceramic chamber and eddy-current shielding.
* **Simulation method:** 3D CST electromagnetic simulation
* **Simulation input file:** *To be released soon.*
* **Notes:** It is the most optimized version at the current stage.


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
- **Simulation input file:** *To be redesigned.*

- **Notes:** Added as a new distributed impedance contributor in the 2026 model, see  [here](https://indico.cern.ch/event/1552126/timetable/#79-impedance-considerations-fo).

</details>

<details>
<summary>11. Beamstrahlung (BS) Monitor</summary>

### Beamstrahlung (BS) Monitor

- **Number of elements:** 8 per beam  
- **Description:** Beam instrumentation device, new in V2.c, named `Z_*_BSmonitor` in the repository.  
- **Simulation method:** 3D CST electromagnetic simulation  
- **Simulation input file:** *To be released soon.*

- **Notes:** Preliminary design. Included in both recommended wakes.

</details>

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
| Collimators (optimized / not optimized) | 13                     | CST                     |
| Beam Pipe (with roughness)      | 90,658.5 m                     | IW2D + CST              |
| EO Monitor                      | 1 per beam                     | CST                     |
| Stripline Kickers               | 12                             | CST                     |
| Injection / Extraction Kickers  | 20 m                           | CST                     |
| SR Absorbers                    | 13,152                         | CST                     |
| Vacuum Flanges                  | 13,152                         | CST                     |
| BS Monitor                      | 8 per beam                     | CST                     |
| Interconnecting Modules         | 4,384                          | CST                     |
| Interaction Region (IR)         | 4                              | CST                     |

---
