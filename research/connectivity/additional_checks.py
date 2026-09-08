"""One-way and combined falsification of the Comcast model; no new predictions."""
import copy
import json
import sys
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent.parent))
import model
c=json.loads((P/'inputs.json').read_text())[0]
base=c['scenarios']['base']
d=json.loads((P/'operating_drivers.json').read_text())['scenarios']['base']
out={}
def v(company=c,sc=base): return model.equity_value(company,sc)['fair_value_per_share']
out['base']=v()
sc=copy.deepcopy(base)
for r,dr in zip(sc['years'],d):
 if r['year']>=2027:
  loss=dr['domestic_average_broadband_subscribers_m']*12*(dr['broadband_monthly_realized_revenue_usd']-70)
  s=r['segments'][0];old=s['revenue']*s['ebit_margin'];s['revenue']-=loss
  s['ebit_margin']=(old-loss*.75)/s['revenue']
out['broadband_arpu70_from2027_high_incremental_margin75pct']=v(sc=sc)
sc=copy.deepcopy(base)
for r in sc['years']:
 if r['year']>=2027:r['corporate_cost']+=1000
out['additional_permanent_separation_cost1000m_from2027']=v(sc=sc)
sc=copy.deepcopy(base)
for r,dr in zip(sc['years'],d):
 if r['year']>=2027:
  # Remove assumed Peacock EBITDA plus charge a recurring500m loss.
  pm=[-.04,0,.04,.08,.11,.13,.15,.16,.17,.18][r['year']-2026]
  r['corporate_cost']+=dr['peacock_revenue_m']*pm+500
out['peacock_loss500m_every_year_from2027']=v(sc=sc)
sc=copy.deepcopy(base)
for r in sc['years']:
 if r['year']>=2027:r['capex']*=1.15
out['all_capital_spending15pct_higher_from2027']=v(sc=sc)
sc=copy.deepcopy(base)
for r in sc['years']:
 if r['year']>=2027:r['capex']+=1600*(1.50-1.3546) if r['year']==2027 else 0
out['itv_GBPUSD1p50']=v(sc=sc)
sc=copy.deepcopy(base)
for r in sc['years']:
 if r['year']>=2028:r['corporate_cost']-=150
out['itv_incremental_ebit150m_no_extra_reinvestment_sensitivity_only']=v(sc=sc)
cc=copy.deepcopy(c);cc['senior_claims_m']+=4000
out['additional_noncommon_claim4000m']=v(company=cc)
cc=copy.deepcopy(c);cc['other_assets_m']=662
out['portfolio_investments_zero_value_except_insurance']=v(company=cc)
cc=copy.deepcopy(c);cc['shares_m']+=291
out['all291m_antidilutive_awards_as_zero_proceeds_extreme']=v(company=cc)
sc=copy.deepcopy(base)
for r,dr in zip(sc['years'],d):
 if r['year']>=2027:
  loss=dr['domestic_average_broadband_subscribers_m']*12*(dr['broadband_monthly_realized_revenue_usd']-70)
  s=r['segments'][0];old=s['revenue']*s['ebit_margin'];s['revenue']-=loss
  s['ebit_margin']=(old-loss*.75)/s['revenue']
  r['corporate_cost']+=1000
  r['capex']*=1.15
out['combined_arpu70_separation1000m_capex15pct']=v(sc=sc)
out['probability_mix_40_50_10']=.4*v(sc=c['scenarios']['downside'])+.5*v()+.1*v(sc=c['scenarios']['upside'])
(P/'additional_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
