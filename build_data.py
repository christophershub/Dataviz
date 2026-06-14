# -*- coding: utf-8 -*-
"""
Build the four sourced CSV datasets for the China-US climate scenario explorer.
Raw values were gathered from World Bank CCKP (CMIP6/ERA5), NGFS Phase V / IEA,
IPCC WGIII / IEA, and Armstrong McKay et al. 2022 (Science). See README for sourcing.

Transformation applied to physical projections: the CCKP climatology product reports
20-year windows (2020-2039, 2040-2059, ...). We relabel each window to its centre year
(2030, 2050, 2070, 2090) so projected lines splice cleanly onto observed data at 2020
instead of producing a vertical jump. hot_days timeseries points are aligned to the
same decadal grid for a consistent x-axis.
"""
import csv, os

os.makedirs("data", exist_ok=True)

# ----------------------------------------------------------------------------
# 1) PHYSICAL CLIMATE  (World Bank CCKP: CMIP6 ensemble projections; ERA5 observed)
#    raw projection years 2020/2040/2060/2080/2100 -> centre years 2030/2050/2070/2090/2100
# ----------------------------------------------------------------------------
PROJ_YEAR_MAP = {2020: 2030, 2040: 2050, 2060: 2070, 2080: 2090, 2100: 2100}
SRC_MAP = {
    "CCKP-CMIP6": "World Bank CCKP (CMIP6 ensemble)",
    "CCKP-CMIP6-est": "World Bank CCKP (CMIP6 ensemble; end-century held)",
    "CCKP-CMIP6-historical": "World Bank CCKP (CMIP6 historical run)",
    "CCKP-ERA5": "World Bank CCKP (ERA5 observed)",
}

phys_raw = """\
CHN,1980,historical,temp_anomaly,-0.56,,,degC,1981-2010,CCKP-ERA5
CHN,1990,historical,temp_anomaly,0.12,,,degC,1981-2010,CCKP-ERA5
CHN,2000,historical,temp_anomaly,-0.10,,,degC,1981-2010,CCKP-ERA5
CHN,2010,historical,temp_anomaly,0.32,,,degC,1981-2010,CCKP-ERA5
CHN,2020,historical,temp_anomaly,0.71,,,degC,1981-2010,CCKP-ERA5
CHN,2020,SSP1-2.6,temp_anomaly,1.34,0.96,1.69,degC,1981-2010,CCKP-CMIP6
CHN,2040,SSP1-2.6,temp_anomaly,1.89,1.30,2.42,degC,1981-2010,CCKP-CMIP6
CHN,2060,SSP1-2.6,temp_anomaly,2.13,1.37,2.69,degC,1981-2010,CCKP-CMIP6
CHN,2080,SSP1-2.6,temp_anomaly,2.01,1.16,2.82,degC,1981-2010,CCKP-CMIP6
CHN,2100,SSP1-2.6,temp_anomaly,2.01,1.16,2.82,degC,1981-2010,CCKP-CMIP6-est
CHN,2020,SSP2-4.5,temp_anomaly,1.32,0.94,1.84,degC,1981-2010,CCKP-CMIP6
CHN,2040,SSP2-4.5,temp_anomaly,2.14,1.61,2.79,degC,1981-2010,CCKP-CMIP6
CHN,2060,SSP2-4.5,temp_anomaly,2.76,1.78,3.37,degC,1981-2010,CCKP-CMIP6
CHN,2080,SSP2-4.5,temp_anomaly,3.20,2.23,3.80,degC,1981-2010,CCKP-CMIP6
CHN,2100,SSP2-4.5,temp_anomaly,3.20,2.23,3.80,degC,1981-2010,CCKP-CMIP6-est
CHN,2020,SSP5-8.5,temp_anomaly,1.51,1.07,1.91,degC,1981-2010,CCKP-CMIP6
CHN,2040,SSP5-8.5,temp_anomaly,2.68,1.95,3.51,degC,1981-2010,CCKP-CMIP6
CHN,2060,SSP5-8.5,temp_anomaly,4.03,3.05,5.35,degC,1981-2010,CCKP-CMIP6
CHN,2080,SSP5-8.5,temp_anomaly,5.64,4.03,7.64,degC,1981-2010,CCKP-CMIP6
CHN,2100,SSP5-8.5,temp_anomaly,5.64,4.03,7.64,degC,1981-2010,CCKP-CMIP6-est
USA,1980,historical,temp_anomaly,-0.24,,,degC,1981-2010,CCKP-ERA5
USA,1990,historical,temp_anomaly,0.22,,,degC,1981-2010,CCKP-ERA5
USA,2000,historical,temp_anomaly,0.15,,,degC,1981-2010,CCKP-ERA5
USA,2010,historical,temp_anomaly,0.25,,,degC,1981-2010,CCKP-ERA5
USA,2020,historical,temp_anomaly,1.01,,,degC,1981-2010,CCKP-ERA5
USA,2020,SSP1-2.6,temp_anomaly,1.30,0.92,1.79,degC,1981-2010,CCKP-CMIP6
USA,2040,SSP1-2.6,temp_anomaly,1.79,1.21,2.55,degC,1981-2010,CCKP-CMIP6
USA,2060,SSP1-2.6,temp_anomaly,1.99,1.34,2.98,degC,1981-2010,CCKP-CMIP6
USA,2080,SSP1-2.6,temp_anomaly,1.90,1.17,3.04,degC,1981-2010,CCKP-CMIP6
USA,2100,SSP1-2.6,temp_anomaly,1.90,1.17,3.04,degC,1981-2010,CCKP-CMIP6-est
USA,2020,SSP2-4.5,temp_anomaly,1.35,0.87,1.84,degC,1981-2010,CCKP-CMIP6
USA,2040,SSP2-4.5,temp_anomaly,2.13,1.56,2.94,degC,1981-2010,CCKP-CMIP6
USA,2060,SSP2-4.5,temp_anomaly,2.70,1.96,3.83,degC,1981-2010,CCKP-CMIP6
USA,2080,SSP2-4.5,temp_anomaly,3.20,2.23,4.01,degC,1981-2010,CCKP-CMIP6
USA,2100,SSP2-4.5,temp_anomaly,3.20,2.23,4.01,degC,1981-2010,CCKP-CMIP6-est
USA,2020,SSP5-8.5,temp_anomaly,1.40,1.05,2.13,degC,1981-2010,CCKP-CMIP6
USA,2040,SSP5-8.5,temp_anomaly,2.64,2.08,3.62,degC,1981-2010,CCKP-CMIP6
USA,2060,SSP5-8.5,temp_anomaly,4.02,3.27,5.50,degC,1981-2010,CCKP-CMIP6
USA,2080,SSP5-8.5,temp_anomaly,5.53,4.49,7.53,degC,1981-2010,CCKP-CMIP6
USA,2100,SSP5-8.5,temp_anomaly,5.53,4.49,7.53,degC,1981-2010,CCKP-CMIP6-est
CHN,1980,historical,precip_change,0.05,,,percent,1981-2010,CCKP-ERA5
CHN,1990,historical,precip_change,7.60,,,percent,1981-2010,CCKP-ERA5
CHN,2000,historical,precip_change,1.46,,,percent,1981-2010,CCKP-ERA5
CHN,2010,historical,precip_change,-0.26,,,percent,1981-2010,CCKP-ERA5
CHN,2020,historical,precip_change,-0.91,,,percent,1981-2010,CCKP-ERA5
CHN,2020,SSP1-2.6,precip_change,7.70,2.78,10.19,percent,1981-2010,CCKP-CMIP6
CHN,2040,SSP1-2.6,precip_change,9.41,6.34,15.70,percent,1981-2010,CCKP-CMIP6
CHN,2060,SSP1-2.6,precip_change,12.35,7.04,17.80,percent,1981-2010,CCKP-CMIP6
CHN,2080,SSP1-2.6,precip_change,12.06,7.19,17.47,percent,1981-2010,CCKP-CMIP6
CHN,2100,SSP1-2.6,precip_change,12.06,7.19,17.47,percent,1981-2010,CCKP-CMIP6-est
CHN,2020,SSP2-4.5,precip_change,6.18,2.66,9.75,percent,1981-2010,CCKP-CMIP6
CHN,2040,SSP2-4.5,precip_change,11.09,5.90,14.61,percent,1981-2010,CCKP-CMIP6
CHN,2060,SSP2-4.5,precip_change,14.51,6.16,18.57,percent,1981-2010,CCKP-CMIP6
CHN,2080,SSP2-4.5,precip_change,16.00,8.63,23.03,percent,1981-2010,CCKP-CMIP6
CHN,2100,SSP2-4.5,precip_change,16.00,8.63,23.03,percent,1981-2010,CCKP-CMIP6-est
CHN,2020,SSP5-8.5,precip_change,7.12,1.77,10.92,percent,1981-2010,CCKP-CMIP6
CHN,2040,SSP5-8.5,precip_change,12.48,7.55,20.08,percent,1981-2010,CCKP-CMIP6
CHN,2060,SSP5-8.5,precip_change,18.88,13.11,26.38,percent,1981-2010,CCKP-CMIP6
CHN,2080,SSP5-8.5,precip_change,27.34,18.82,40.60,percent,1981-2010,CCKP-CMIP6
CHN,2100,SSP5-8.5,precip_change,27.34,18.82,40.60,percent,1981-2010,CCKP-CMIP6-est
USA,1980,historical,precip_change,-2.93,,,percent,1981-2010,CCKP-ERA5
USA,1990,historical,precip_change,4.07,,,percent,1981-2010,CCKP-ERA5
USA,2000,historical,precip_change,-7.99,,,percent,1981-2010,CCKP-ERA5
USA,2010,historical,precip_change,-3.98,,,percent,1981-2010,CCKP-ERA5
USA,2020,historical,precip_change,-2.68,,,percent,1981-2010,CCKP-ERA5
USA,2020,SSP1-2.6,precip_change,3.89,1.22,7.89,percent,1981-2010,CCKP-CMIP6
USA,2040,SSP1-2.6,precip_change,6.40,3.25,10.65,percent,1981-2010,CCKP-CMIP6
USA,2060,SSP1-2.6,precip_change,7.80,2.44,11.17,percent,1981-2010,CCKP-CMIP6
USA,2080,SSP1-2.6,precip_change,8.22,2.77,12.83,percent,1981-2010,CCKP-CMIP6
USA,2100,SSP1-2.6,precip_change,8.22,2.77,12.83,percent,1981-2010,CCKP-CMIP6-est
USA,2020,SSP2-4.5,precip_change,3.80,0.94,7.04,percent,1981-2010,CCKP-CMIP6
USA,2040,SSP2-4.5,precip_change,6.51,2.61,8.89,percent,1981-2010,CCKP-CMIP6
USA,2060,SSP2-4.5,precip_change,8.02,3.43,10.75,percent,1981-2010,CCKP-CMIP6
USA,2080,SSP2-4.5,precip_change,9.79,4.08,13.94,percent,1981-2010,CCKP-CMIP6
USA,2100,SSP2-4.5,precip_change,9.79,4.08,13.94,percent,1981-2010,CCKP-CMIP6-est
USA,2020,SSP5-8.5,precip_change,4.42,1.70,7.45,percent,1981-2010,CCKP-CMIP6
USA,2040,SSP5-8.5,precip_change,6.90,3.41,11.90,percent,1981-2010,CCKP-CMIP6
USA,2060,SSP5-8.5,precip_change,11.64,5.65,17.20,percent,1981-2010,CCKP-CMIP6
USA,2080,SSP5-8.5,precip_change,12.58,6.89,22.78,percent,1981-2010,CCKP-CMIP6
USA,2100,SSP5-8.5,precip_change,12.58,6.89,22.78,percent,1981-2010,CCKP-CMIP6-est
CHN,2020,SSP1-2.6,hot_days,6.34,3.50,10.90,days,1981-2010,CCKP-CMIP6
CHN,2040,SSP1-2.6,hot_days,8.22,4.36,15.08,days,1981-2010,CCKP-CMIP6
CHN,2060,SSP1-2.6,hot_days,11.21,6.19,17.80,days,1981-2010,CCKP-CMIP6
CHN,2080,SSP1-2.6,hot_days,10.62,5.12,20.28,days,1981-2010,CCKP-CMIP6
CHN,2100,SSP1-2.6,hot_days,10.02,5.22,18.55,days,1981-2010,CCKP-CMIP6
CHN,2020,SSP2-4.5,hot_days,6.18,3.50,10.38,days,1981-2010,CCKP-CMIP6
CHN,2040,SSP2-4.5,hot_days,9.35,5.27,16.58,days,1981-2010,CCKP-CMIP6
CHN,2060,SSP2-4.5,hot_days,12.89,7.28,21.55,days,1981-2010,CCKP-CMIP6
CHN,2080,SSP2-4.5,hot_days,14.52,8.14,25.34,days,1981-2010,CCKP-CMIP6
CHN,2100,SSP2-4.5,hot_days,16.47,8.30,27.61,days,1981-2010,CCKP-CMIP6
CHN,2020,SSP5-8.5,hot_days,6.91,3.12,11.73,days,1981-2010,CCKP-CMIP6
CHN,2040,SSP5-8.5,hot_days,10.79,4.66,18.76,days,1981-2010,CCKP-CMIP6
CHN,2060,SSP5-8.5,hot_days,17.80,9.63,31.23,days,1981-2010,CCKP-CMIP6
CHN,2080,SSP5-8.5,hot_days,28.11,15.22,47.09,days,1981-2010,CCKP-CMIP6
CHN,2100,SSP5-8.5,hot_days,38.53,19.28,65.90,days,1981-2010,CCKP-CMIP6
USA,2020,SSP1-2.6,hot_days,15.69,7.21,28.23,days,1981-2010,CCKP-CMIP6
USA,2040,SSP1-2.6,hot_days,20.23,9.58,33.02,days,1981-2010,CCKP-CMIP6
USA,2060,SSP1-2.6,hot_days,23.47,9.77,37.01,days,1981-2010,CCKP-CMIP6
USA,2080,SSP1-2.6,hot_days,21.85,11.83,35.93,days,1981-2010,CCKP-CMIP6
USA,2100,SSP1-2.6,hot_days,20.36,9.13,35.79,days,1981-2010,CCKP-CMIP6
USA,2020,SSP2-4.5,hot_days,15.91,7.92,26.30,days,1981-2010,CCKP-CMIP6
USA,2040,SSP2-4.5,hot_days,21.67,12.19,32.97,days,1981-2010,CCKP-CMIP6
USA,2060,SSP2-4.5,hot_days,25.09,12.30,41.79,days,1981-2010,CCKP-CMIP6
USA,2080,SSP2-4.5,hot_days,32.15,16.76,50.63,days,1981-2010,CCKP-CMIP6
USA,2100,SSP2-4.5,hot_days,32.29,16.36,53.11,days,1981-2010,CCKP-CMIP6
USA,2020,SSP5-8.5,hot_days,16.39,7.37,28.83,days,1981-2010,CCKP-CMIP6
USA,2040,SSP5-8.5,hot_days,24.16,11.85,38.27,days,1981-2010,CCKP-CMIP6
USA,2060,SSP5-8.5,hot_days,34.10,18.18,53.79,days,1981-2010,CCKP-CMIP6
USA,2080,SSP5-8.5,hot_days,51.67,28.55,74.05,days,1981-2010,CCKP-CMIP6
USA,2100,SSP5-8.5,hot_days,68.26,41.38,97.40,days,1981-2010,CCKP-CMIP6
CHN,1980,historical,hot_days,3.09,1.43,5.74,days,1981-2010,CCKP-CMIP6-historical
CHN,1990,historical,hot_days,3.63,1.96,6.19,days,1981-2010,CCKP-CMIP6-historical
CHN,2000,historical,hot_days,4.48,2.38,7.30,days,1981-2010,CCKP-CMIP6-historical
CHN,2010,historical,hot_days,4.96,2.69,8.16,days,1981-2010,CCKP-CMIP6-historical
USA,1980,historical,hot_days,7.74,3.20,14.53,days,1981-2010,CCKP-CMIP6-historical
USA,1990,historical,hot_days,9.08,4.43,14.88,days,1981-2010,CCKP-CMIP6-historical
USA,2000,historical,hot_days,10.18,4.33,16.97,days,1981-2010,CCKP-CMIP6-historical
USA,2010,historical,hot_days,12.35,5.60,19.91,days,1981-2010,CCKP-CMIP6-historical"""

CC_MAP = {"CHN": "China", "USA": "United States"}
phys_header = ["country","year","scenario","indicator","value","lower_bound","upper_bound","unit","baseline_period","source"]
phys_rows = []
for line in phys_raw.strip().splitlines():
    c = line.split(",")
    country = CC_MAP[c[0]]
    year = int(c[1]); scen = c[2]; indicator = c[3]
    # Only temperature/precipitation are 20-year climatology windows -> plot at window centre.
    # hot_days are annual timeseries points and keep their true year (so the series starts at 2020).
    if scen != "historical" and indicator in ("temp_anomaly", "precip_change"):
        year = PROJ_YEAR_MAP[year]
    src = SRC_MAP.get(c[9], c[9])
    phys_rows.append([country, year, scen, c[3], c[4], c[5], c[6], c[7], c[8], src])

with open("data/physical_climate.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(phys_header); w.writerows(phys_rows)

# ----------------------------------------------------------------------------
# 2) TRANSITION PATHWAYS  (NGFS Phase V scenario logic; IEA/EIA base years & investment)
# ----------------------------------------------------------------------------
trans = """country,year,scenario,emissions_mtco2e,investment_usd_billion,carbon_price_usd,source
China,2020,Current Policies,11900,300,2,NGFS Phase V / IEA (energy CO2 base year)
China,2025,Current Policies,12200,640,4,NGFS Phase V / IEA WEI 2025
China,2030,Current Policies,12400,700,6,NGFS Phase V / IEA STEPS
China,2035,Current Policies,12300,720,8,NGFS Phase V
China,2040,Current Policies,12000,730,10,NGFS Phase V
China,2045,Current Policies,11700,740,12,NGFS Phase V
China,2050,Current Policies,11400,750,15,NGFS Phase V
China,2020,Delayed Transition,11900,300,2,NGFS Phase V / IEA
China,2025,Delayed Transition,12200,640,4,NGFS Phase V
China,2030,Delayed Transition,12400,720,8,NGFS Phase V
China,2035,Delayed Transition,9800,1100,180,NGFS Phase V
China,2040,Delayed Transition,6800,1300,280,NGFS Phase V
China,2045,Delayed Transition,3800,1300,360,NGFS Phase V
China,2050,Delayed Transition,1500,1200,430,NGFS Phase V
China,2020,Net Zero 2050,11900,300,2,NGFS Phase V / IEA
China,2025,Net Zero 2050,11200,900,40,NGFS Phase V / IEA NZE
China,2030,Net Zero 2050,8800,1500,110,NGFS Phase V / IEA NZE
China,2035,Net Zero 2050,6000,1700,300,NGFS Phase V
China,2040,Net Zero 2050,3600,1700,420,NGFS Phase V
China,2045,Net Zero 2050,1700,1600,520,NGFS Phase V
China,2050,Net Zero 2050,600,1500,620,NGFS Phase V
United States,2020,Current Policies,4600,250,3,NGFS Phase V / US EIA (2020 energy CO2)
United States,2025,Current Policies,4700,300,5,NGFS Phase V / IEA STEPS
United States,2030,Current Policies,4600,330,7,NGFS Phase V
United States,2035,Current Policies,4500,340,9,NGFS Phase V
United States,2040,Current Policies,4400,350,11,NGFS Phase V
United States,2045,Current Policies,4300,355,13,NGFS Phase V
United States,2050,Current Policies,4200,360,16,NGFS Phase V
United States,2020,Delayed Transition,4600,250,3,NGFS Phase V / US EIA
United States,2025,Delayed Transition,4700,300,5,NGFS Phase V
United States,2030,Delayed Transition,4500,330,8,NGFS Phase V
United States,2035,Delayed Transition,3400,600,180,NGFS Phase V
United States,2040,Delayed Transition,2200,650,280,NGFS Phase V
United States,2045,Delayed Transition,1100,620,370,NGFS Phase V
United States,2050,Delayed Transition,400,550,440,NGFS Phase V
United States,2020,Net Zero 2050,4600,250,3,NGFS Phase V / US EIA
United States,2025,Net Zero 2050,4100,500,45,NGFS Phase V / IEA NZE
United States,2030,Net Zero 2050,2900,750,120,NGFS Phase V / IEA NZE
United States,2035,Net Zero 2050,1900,800,300,NGFS Phase V
United States,2040,Net Zero 2050,1100,800,430,NGFS Phase V
United States,2045,Net Zero 2050,500,750,530,NGFS Phase V
United States,2050,Net Zero 2050,100,700,640,NGFS Phase V
"""
with open("data/transition_pathways.csv", "w", newline="", encoding="utf-8") as f:
    f.write(trans)

# ----------------------------------------------------------------------------
# 3) ABATEMENT OPTIONS  (IEA NZE / China roadmap; IPCC WGIII; Rhodium; IEA Methane Tracker)
#    Values are indicative annual investment (USD bn/yr) and abatement potential.
# ----------------------------------------------------------------------------
abate_rows = [
 ["China","Renewable electricity expansion","Power",250,2500,50000,"High","IEA NZE 2023; IEA China roadmap 2021; IPCC WGIII","Annual investment; China share of global NZE wind+solar spend"],
 ["China","Coal phase-down","Power",50,3000,60000,"High","IEA China carbon-neutrality roadmap 2021","Unabated coal ends by 2050; abatement vs ~11 Gt baseline"],
 ["China","Electricity grid & storage","Power",90,600,12000,"Medium","IEA China roadmap 2021","Enabling investment; abatement is indirect"],
 ["China","Transport electrification","Transport",70,800,16000,"Medium","IEA China roadmap 2021; IPCC WGIII","China ~40% of global EV sales"],
 ["China","Building & industrial efficiency","Industry & Buildings",80,1500,30000,"Medium","IEA China roadmap 2021; IPCC WGIII","Industry is China's largest emitting sector"],
 ["China","Methane abatement","Cross-cutting",10,400,8000,"Medium","IEA Global Methane Tracker 2024; China Methane Plan 2023","Coal-mine + oil & gas + agriculture; no binding target"],
 ["United States","Renewable electricity expansion","Power",130,1000,20000,"High","IEA NZE 2023; IPCC WGIII; Rhodium","US share of global NZE wind+solar spend"],
 ["United States","Coal phase-down","Power",20,800,16000,"High","Rhodium Pathways to Net-Zero; IEA NZE","Coal displaced by gas + renewables"],
 ["United States","Electricity grid & storage","Power",70,400,8000,"Medium","IEA NZE 2023; Rhodium","Transmission + storage; abatement is indirect"],
 ["United States","Transport electrification","Transport",80,700,14000,"Medium","IPCC WGIII; Rhodium; IEA","Transport is the largest US emitting sector"],
 ["United States","Building & industrial efficiency","Industry & Buildings",60,500,10000,"Medium","IPCC WGIII; IEA NZE; Rhodium","Efficiency + heat pumps + electrification"],
 ["United States","Methane abatement","Cross-cutting",8,250,5000,"High","IEA Global Methane Tracker 2024; Global Methane Pledge; EPA rules","Oil & gas + landfill; low-cost, largely regulated"],
]
abate_header = ["country","option","sector","estimated_investment_usd_billion","estimated_annual_abatement_mtco2e","cumulative_abatement_2050_mtco2e","confidence","source","notes"]
with open("data/abatement_options.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(abate_header); w.writerows(abate_rows)

# ----------------------------------------------------------------------------
# 4) TIPPING POINTS  (Armstrong McKay et al. 2022, Science 377, eabn7950)
# ----------------------------------------------------------------------------
tip_rows = [
 ["Greenland Ice Sheet collapse",0.8,1.5,3.0,"~7 m sea-level rise over millennia","High","Armstrong McKay et al. 2022, Science",
  "Both countries' coasts lie far from Greenland, so its meltwater raises local sea level by close to, or above, the global average. Low-lying hubs such as Shanghai, the Pearl River Delta, Florida and the US Gulf Coast are among the most exposed."],
 ["West Antarctic Ice Sheet collapse",1.0,1.5,3.0,"~5 m sea-level rise over millennia","High","Armstrong McKay et al. 2022, Science",
  "Gravitational 'fingerprint' effects mean Antarctic ice loss raises Northern-Hemisphere sea level above the global mean, disproportionately affecting Chinese and US coastlines, including the densely populated US East Coast and China's eastern seaboard."],
 ["Warm-water coral reef die-off",1.0,1.5,2.0,"Near-total loss of low-latitude reefs","High","Armstrong McKay et al. 2022, Science",
  "China's reefs in the South China Sea (around Hainan and the Paracel/Spratly islands) and US reefs off Florida, Hawai'i and the Pacific territories would face near-total loss, hitting fisheries, tourism and natural coastal protection."],
 ["Boreal permafrost abrupt thaw",1.0,1.5,2.3,"Localized abrupt thaw and extra carbon release","Medium","Armstrong McKay et al. 2022, Science",
  "The US has extensive permafrost in Alaska, and China on the Qinghai-Tibet Plateau and in the north-east. Thaw damages infrastructure (roads, the Qinghai-Tibet railway, Alaskan pipelines and buildings) and releases extra CO2 and methane."],
 ["Labrador-Irminger Sea convection collapse",1.1,1.8,3.8,"Regional cooling; European weather extremes","Medium","Armstrong McKay et al. 2022, Science",
  "This North Atlantic convection collapse would cool the north-east US and bring harsher winters to eastern North America and Europe; effects on China are weaker and more indirect, transmitted through the global circulation."],
 ["Atlantic circulation (AMOC) collapse",1.4,4.0,8.0,"Major shifts in regional climate and monsoons","Medium","Armstrong McKay et al. 2022, Science",
  "An AMOC collapse would add extra sea-level rise along the US East Coast and disrupt rainfall across the Americas, while weakening and shifting the East Asian monsoon that much of China's agriculture depends on."],
]
tip_header = ["tipping_element","lower_warming_level","central_warming_level","upper_warming_level","consequence","confidence","source","relevance"]
with open("data/tipping_points.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(tip_header); w.writerows(tip_rows)

print("Wrote:")
for fn in ["physical_climate.csv","transition_pathways.csv","abatement_options.csv","tipping_points.csv"]:
    n = sum(1 for _ in open("data/"+fn, encoding="utf-8")) - 1
    print(f"  data/{fn}  ({n} rows)")
