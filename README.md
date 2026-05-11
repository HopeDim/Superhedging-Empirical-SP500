# Empirical Analysis: Super-Hedging with Transaction Costs

**Open Research Study | Preprint 2026**

---

## 📚 Overview

This repository contains a complete empirical study on **model-free super-hedging of European options under proportional transaction costs**, with applications to real market data (SPY ETF).

### Authors
- **Emmanuel Lepinette** (CEREMADE, UMR CNRS 7534, Université Paris-Dauphine, PSL)
- **Amal Omrani** (CEREMADE, UMR CNRS 7534, Université Paris-Dauphine, PSL)

### Paper Status
📝 **Preprint, 2026** 

---

## 🎯 What's in This Repository

```
GithubEmpericalStudy/
├── Empirical_Analysis.ipynb          # Main Jupyter notebook with complete analysis
├── def_plots.py                       # Helper functions for plotting and data processing
├── results_kappa_*.csv                # Simulation results for different κ values
├── results_kappa_grid_test.csv        # Fine-grid study results (single period)
├── README.md                          # This file
└── data/
    └── (SPY data is downloaded automatically via yfinance)
```

---

## 🚀 Quick Start

### Prerequisites
```bash
python >= 3.8
pandas
numpy
matplotlib
seaborn
yfinance
scikit-learn
jupyter
```


## 📊 What You'll Find

### **Section 1: Setup & Data Loading**
- Import 5 CSV files with pre-computed super-hedging results
- κ values: {0, 5×10⁻⁴, 10⁻³, 5×10⁻³, 9×10⁻³}
- Data loading and label standardization

### **Section 2: Distribution Analysis**
Empirical distributions of key metrics:
- **RSE** (ε^j): Relative super-hedging error
- **Pj** (P^j(κ)): Normalized initial super-hedging price
- **Cost Impact** (I^j(κ)): Marginal price increase per unit κ

Visualized as histograms and boxplots for each κ value.

### **Section 3: Time-Series Overlay**
Comprehensive visualization showing:
- SPY price path (Jan 2020 – Feb 2026)
- Dynamically calibrated support bands
- Evolution of normalized prices P^j(κ) over time

**Key finding:** SPY remains within support bands throughout the period, validating model assumptions.

### **Section 4: Robustness Check**
Filter for stable market periods where:
- Lower bound α^j ≥ 0.96
- Upper bound β^j ≤ 1.04

**Result:** Under tight conditions, mean RSE improves from **5% → 3%**, showing model efficiency in stable markets.

### **Section 5: Grid Study**
Detailed analysis of a single period (March 2023) with dense grid of 100 κ values:
- **P(κ)**: Smooth, strictly increasing, convex growth
- **I(κ)**: Cost impact elasticity curves
- **ε(κ)**: Super-hedging error trajectory

Shows price nearly **triples** as κ goes from 0 to 0.01.



---

## 🔧 Key Definitions

### **Support Band Calibration**
For each 21-day trading period j:
- **α^j**: min{S_{t+1}/S_t : t in past 252 days}
- **β^j**: max{S_{t+1}/S_t : t in past 252 days}

### **Key Metrics**

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **RSE** (ε^j) | (V_T^j - payoff) / S_T^j | Terminal surplus as % of final price |
| **Pj** (P^j(κ)) | V_0^j / S_0^j | Initial capital per unit initial price |
| **Cost Impact** (I^j(κ)) | (P^j(κ) - P^j(0)) / κ | Price elasticity to transaction costs |

### **Payoff Structure**
- **Type**: European call option
- **Strike**: ATM (K^j = S_0^j, initial price of period j)
- **Horizon**: N = 21 days

---

## 📈 Main Empirical Results

### **1. Super-Hedging Constraint Validation**
- RSE always **non-negative** across all periods
- SPY **never exits** support bands (by construction)
- Model assumptions validated empirically

### **2. Transaction Cost Impact**
Mean RSE by κ value:
| κ | Mean RSE | Interpretation |
|---|----------|---|
| 0 | 5.0% | Frictionless benchmark |
| 5×10⁻⁴ | 6.0% | Minimal friction |
| 10⁻³ | 7.0% | Small friction |
| 5×10⁻³ | 12.0% | Larger friction |

### **3. Pricing Behavior**
- P^j(κ) is **strictly convex** in κ
- Illustrates **dominant role** of transaction costs
- Higher κ → wider support bands → larger buffer needed

### **4. Market Stability Effect**
- **Full data**: Mean RSE = 5.0% (κ=0)
- **Filtered (tight bands)**: Mean RSE = 3.0% (κ=0)
- Model becomes **more efficient** when volatility decreases

---

## 🗂️ Data Files

### Provided CSV Files
- `results_kappa_0.csv`: κ = 0 (frictionless)
- `results_kappa_0.0005.csv`: κ = 5×10⁻⁴
- `results_kappa_0.001.csv`: κ = 10⁻³
- `results_kappa_0.005.csv`: κ = 5×10⁻³
- `results_kappa_0.009.csv`: κ = 9×10⁻³
- `results_kappa_grid_test.csv`: Fine grid (100 points, one period)

### Downloaded Data
- SPY closing prices are **automatically downloaded** via `yfinance`
- Period: Jan 1, 2020 – Feb 23, 2026
- Requires internet connection

---

## 💻 Code Structure

### Main Notebook Cells

| Cell | Purpose |
|------|---------|
| 1-2 | Setup & imports |
| 3-5 | Load all CSV data |
| 6-10 | Distribution analysis (RSE, Pj, Cost Impact) |
| 11-15 | Support band construction & overlay plot |
| 16-18 | Robustness filtering |
| 19-20 | Grid study: P(κ) and I(κ) curves |
| 21-22 | Quadratic fitting |
| 23+ | LaTeX table export |

### Helper Functions (def_plots.py)

```python
# Data loading
load_and_metrics(path, label)      # Load CSV, compute metrics

# Visualization
plot_rse(df, ycol, savepath)       # RSE boxplot + stripplot
plot_pj_logscale(df, ycol, savepath)  # Pj log-scale boxplot
plot_impact_cost(df, ycol, savepath)  # Cost impact boxplot

# Computation
compute_I(df, pj_col, kappa_col)   # Compute I(κ) from Pj data
to_float(x)                        # Parse numeric strings
```

---

## 📊 Output Files

The notebook generates:

### Figures (PDF & PNG)
- `fig_rse_hist.pdf` – RSE histogram
- `fig_pj_hist.pdf` – Pj histogram
- `Fig_RSE.pdf` – RSE boxplot
- `Fig_Pj_logscale.pdf` – Pj boxplot (log scale)
- `Fig_Impact_Cost.pdf` – Cost impact boxplot
- `fig_spy_support_pj_overlay.pdf` – **Main figure**: SPY + bands + Pj curves
- `fig_p_kappa_continuous.pdf` – P(κ) curve
- `fig_i_kappa_continuous.pdf` – I(κ) curve
- `fig_epsilon_kappa_continuous.pdf` – ε(κ) curve
- `fig_quadratic_fit_p.pdf` – Quadratic approximation

### Tables (LaTeX)
- `table_cost_impact.tex` – Cost impact statistics (full data)
- `table_relative_superhedging_error.tex` – RSE statistics (full data)
- `table_normalized_price.tex` – Pj statistics (full data)
- `table_*_bis.tex` – Same tables for filtered (stable) periods

---



## 📚 Mathematical Background

### **Model-Free Super-Hedging**
Given:
- Support bounds: S_t ∈ [α_t S_{t-1}, β_t S_{t-1}]
- Transaction costs: κ (proportional)
- Payoff: φ(S_T)

Find: Minimum V_0 such that ∃ admissible strategy φ_t with V_T ≥ φ(S_T)

### **Key Theoretical Results** (from paper)
- Super-hedging prices computed **backward in time** (no arbitrage condition needed)
- Admissible hedge is **unique interval** [φ^l(p), φ^h(p)]
- Closed-form formulas for **convex payoffs**

---

## 🎓 For Researchers

### Citation
```bibtex
@article{Lepinette-Omrani-2026,
  title={Pricing Vanilla Options under Transaction Costs: A Model-Free Approach},
  author={Lepinette, Emmanuel and Omrani, Amal},
  year={2026},
  note={Preprint}
}
```





