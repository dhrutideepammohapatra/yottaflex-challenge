# Synthetic Telemetry Data Generator - Cohort Analytics Engine

## 🚀 Project Overview
This repository contains a deterministic synthetic data engine designed to scaffold master and behavioral interaction tables modeling enterprise learning cohorts. The solution handles cascading relational dependencies, maps deterministic padding nomenclatures, models event transaction structures, and exports clean isolated ground-truth anomalies as requested.

## 🛠️ Installation & Generation Steps
The codebase operates fully with native Python systems without external third-party dependencies.

1. **Clone the project workspace directory:**
   ```bash
   git clone https://github.com
   ```
2. **Execute the generator execution command:**
   ```bash
   python generator.py
   ```
3. **Verify the generated outputs:**
   * Review data exports located inside the automatically generated `/output` directory folder.

## 📊 Parametric & Architectural Disclosures
* **Deterministic Pseudo-Random Seed:** Parameterized to fixed constraint seed value `20261022`. Row distributions remain identical across replication cycles.
* **Injected Anomalies Covered:** Captures explicit flagged instances of duplicates inflating metrics and activity records linked to unenrolled entity keys.