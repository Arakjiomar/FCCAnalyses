# $ttH \rightarrow \gamma\gamma$ analysis at FCC-hh
Analysis of $ttH \rightarrow \gamma\gamma$ process at FCC-hh.

Preparation of ROOT ntuples starting from `EDM4HEP` samples, event selection, and plotting.

## Quick start
1. Dump ROOT ntuples from `EDM4HEP` samples, based on RDataFrame syntax. Calculate 4-momenta, and other simple object-level and event-level observables.
```
fccanalysis run analysis_stage1.py
```
2. Apply event selection, prepare ntuples with selected events only, prepare histograms of interesting observables.
```
fccanalysis final analysis_final.py
```
3. Plotting tool.
```
fccanalysis plots analysis_plots.py
```