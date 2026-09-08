"""Conditional physical activity models. Standard library; all forecasts assumptions.
Run python research/power_water/demand_supply.py from repository root.
Numbers are scenario bounds, not verified industry capacity estimates.
"""
import json
from pathlib import Path
OUT=Path(__file__).parent
years=list(range(2026,2036))
paths={
 "persistent_scarcity":{"gross_activity_growth":[.045,.05,.05,.045,.04,.035,.03,.025,.025,.025],"efficiency":[.01]*10,"supply":[51,55,61,68,75,82,88,92,96,100],"replacement_rate":[.006,.0065,.007,.0075,.008,.0085,.009,.009,.009,.009],"housing":[1.35,1.45,1.55,1.6,1.65,1.7,1.7,1.7,1.7,1.7],"water_usable":[19,20,21,22.5,24,25.5,27,28,29,30]},
 "orderly_normalization":{"gross_activity_growth":[.04,.04,.038,.035,.033,.03,.028,.027,.026,.025],"efficiency":[.01]*10,"supply":[53,60,69,79,87,93,98,102,106,110],"replacement_rate":[.005,.0052,.0054,.0056,.0058,.006,.0062,.0064,.0066,.0068],"housing":[1.3,1.35,1.4,1.43,1.45,1.46,1.47,1.48,1.49,1.5],"water_usable":[19,20.5,22,23.5,25,26,27,28,29,30]},
 "oversupply_disappointment":{"gross_activity_growth":[.028,.018,.02,.025,.025,.025,.025,.025,.025,.025],"efficiency":[.012]*10,"supply":[55,66,79,91,99,103,105,107,109,111],"replacement_rate":[.0048,.0045,.0045,.0048,.005,.0052,.0054,.0055,.0056,.0057],"housing":[1.25,1.1,1.15,1.2,1.25,1.3,1.32,1.34,1.36,1.38],"water_usable":[20,22,24,26,28,29,29,30,30,31]}
}
result={
 "status":"conditional demand/supply stress tests, not verified shortage forecasts. Absolute equipment capacity, supplier market shares, and company-specific product contents unresolved; cannot establish a finalist shortage thesis.",
 "units_and_sources":{
  "energy":"2025 US total end-use demand4200TWh(PW22). Annual net growth=(1+gross_activity_growth)*(1-efficiency)-1. Gross activity already includes efficiency-induced extra usage; no separate rebound add-on.",
  "grid":"Incremental peak requirement GW=incremental annual TWh/(8.76*0.60 assumed load factor). One US network interface exposure per peak GW is multiplied1.5 for incremental connections/redundancy. Annual replacements20GW-equivalent assumed separately. These are standardized connection-duty GW-equivalents, not gas generationGW, transformerGVA, or physical switchgear panels.",
  "grid_supply":"Usable custom connection-equipment supply in the same assumed GW-equivalent measure. No industry census supports levels; paths deliberately test different supply responses. Already adjusted for staff, yield and qualification; do not adjust twice. Existing base assumed55-60GW annual nameplate; usable51-55GW. New plant/equipment additions and productivity in scenario arrays; financing/qualification of specific expansions not verified. PW17 independently establishes expansion direction only, not this output.",
  "water":"Starting installed mains2200000miles from EPA(PW24, itself citing ASCE2021; not independent duplicate). Renewed miles=beginning mains*renewal rate. New miles=housing starts(million)*1000000*0.004miles/home assumed. Renewals do not grow installed stock; new miles do. Legacy0.5% annual rate from EPA2018 p24(PW25) stale, used scenario anchor only.",
  "water_supply":"Usable installed/renewed mains thousand miles/year constrained jointly by crews, local budgets, approvals and equipment; scenario assumption not known valve foundry capacity. Six replacement/new valves per worked mile and $3000 per valve used only illustrative component intensity, not addressable market or Mueller revenue estimate.",
  "water_budget":"Financed completion=min(desired miles,usable miles,budget_mUSD/cost_per_mile). Cost$1m/mile and budget$21bn in2026 rising3% annually assumptions. Does not add EPA625bn need to customer spending. American Water3.7bn includes acquisitions; H1 tangible/nonacquisition investment1.454bn verifies some actual spending but is not extrapolated to all utilities."
 },
 "scenarios":{}
}
for name,p in paths.items():
 energy=4200
 mains=2200000
 rows=[]
 for i,y in enumerate(years):
  prev=energy
  energy*= (1+p["gross_activity_growth"][i])*(1-p["efficiency"][i])
  inc=energy-prev
  grid_demand=inc/(8.76*.60)*1.5+20
  renewal=mains*p["replacement_rate"][i]
  new=p["housing"][i]*1000000*.004
  wanted=renewal+new
  watercap=p["water_usable"][i]*1000
  budget=21000*1.03**i
  feasible=min(wanted,watercap,budget)
  rows.append({"year":y,"electricity_TWh":round(energy,1),"gross_activity_growth":p["gross_activity_growth"][i],"efficiency_reduction":p["efficiency"][i],"incremental_peak_GW":round(inc/(8.76*.60),2),"grid_replacement_duty_GW_equivalent":20,"grid_demand_GW_equivalent":round(grid_demand,2),"grid_usable_supply_GW_equivalent_ASSUMED":p["supply"][i],"grid_supply_to_demand":round(p["supply"][i]/grid_demand,3),"beginning_mains_miles":round(mains),"renewal_rate":p["replacement_rate"][i],"renewal_miles":round(renewal),"housing_starts_million":p["housing"][i],"new_mains_miles":round(new),"desired_water_miles":round(wanted),"usable_water_supply_miles_ASSUMED":watercap,"water_budget_mUSD_ASSUMED":round(budget),"feasible_water_miles":round(feasible),"illustrative_valves_units":round(feasible*6),"illustrative_valve_revenue_mUSD":round(feasible*6*.003,2)})
  mains+=new
 result["scenarios"][name]=rows
(OUT/"demand_supply.json").write_text(json.dumps(result,indent=2)+"\n")
for name,rows in result["scenarios"].items():
 print(name,[(r["year"],r["grid_demand_GW_equivalent"],r["grid_usable_supply_GW_equivalent_ASSUMED"],r["feasible_water_miles"]) for r in rows])

