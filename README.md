# How climate futures could diverge in China and the United States

An interactive **scenario explorer** comparing physical-climate outcomes and transition
pathways for China and the United States under alternative global scenarios. Built for the
*From Prompt to Plot — Data Visualization with AI Copilots* portfolio (Task 12, interactive
visualization).

**Live:** https://christophershub.github.io/Dataviz/

This is a scenario explorer, not a forecast. Scenarios are conditional futures under
different assumptions, not statistically predicted outcomes.

## What it does

Two linked analytical views, driven by shared controls (countries, indicator, scenario,
time range):

- **Climate outcomes** — country-level observed history (solid lines) and CMIP6 projections
  (dashed lines, with 10th–90th-percentile uncertainty ribbons) for three indicators:
  mean temperature anomaly, annual precipitation change, and days above 35 °C. A
  warming-level strip below shows tipping-point thresholds as uncertainty ranges.
- **Transition choices** — NGFS emissions pathways, plus an abatement-package builder:
  tick sectoral options to update annual investment, annual and cumulative abatement, and
  remaining 2050 emissions. Mitigation choices deliberately do **not** recalculate the
  physical-climate chart (that would require an integrated climate model).

### Implemented interaction modes
Filtering (show/hide countries) · scenario selection · indicator remapping (updates data,
axis, units, subtitle, finding) · temporal navigation (dual-handle year range) · details on
demand (tooltips) · coordinated view updates (one control set drives both views and the
summary cards) · reset.

## Run locally

The page loads data via `fetch`, so it must be served over HTTP, not opened as a `file://`:

```bash
python -m http.server 8000
# then open http://localhost:8000/
```

## Project structure

```
index.html   markup + controls + footer (sources)
styles.css   editorial design system
app.js       data loading, filtering, charting, summary logic (data-driven; no hard-coded values)
build_data.py  regenerates the four CSVs from the sourced raw values
data/
  physical_climate.csv      country, year, scenario, indicator, value, lower/upper, unit, baseline, source
  transition_pathways.csv   country, year, scenario, emissions, investment, carbon price, source
  abatement_options.csv     country, option, sector, investment, annual/cumulative abatement, confidence, source, notes
  tipping_points.csv        element, lower/central/upper warming level, consequence, confidence, source
```

To update the data, edit the CSVs (or `build_data.py`) and reload — no code changes needed.

## Data sources

- **Physical climate** — World Bank Climate Change Knowledge Portal (CMIP6 multi-model
  ensemble for projections; ERA5 for observed history). Temperature anomalies converted to a
  1981–2010 baseline. Projection points plotted at 20-year-window centres (2030/2050/2070/2090).
- **Transition pathways** — NGFS Phase V scenarios (Current Policies / Delayed Transition /
  Net Zero 2050); base-year emissions and investment from IEA and US EIA. Trajectories between
  published anchor points are interpolated consistent with NGFS scenario logic.
- **Abatement options** — IEA Net Zero Roadmap (2023), IEA China carbon-neutrality roadmap
  (2021), IPCC AR6 WGIII, Rhodium Group, IEA Global Methane Tracker (2024). Indicative values.
- **Tipping points** — Armstrong McKay, D.I. et al. (2022), "Exceeding 1.5 °C global warming
  could trigger multiple climate tipping points," *Science* 377, eabn7950.

### Caveats / still to refine
- CMIP6 and NGFS come from different modelling frameworks; the Low/Intermediate/High labels
  align them conceptually only.
- Abatement-option effects are an illustrative additive sum; overlaps and economy-wide
  feedbacks are not modelled.
- Transition-pathway intermediate points are interpolated and should be validated against a
  direct pull from the NGFS Scenario Explorer before any non-academic use.

## Tools

HTML / CSS / JavaScript with Plotly.js (CDN). Hosted on GitHub Pages. Built with Claude Code
and verified in-browser with the Playwright MCP. Data sourced with research subagents.
