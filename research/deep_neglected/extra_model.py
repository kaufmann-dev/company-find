"""Reproduce these companies using root DCF plus dated distributions/funding stress.

Run python research/deep_neglected/extra_model.py. No dependencies. Writes only HERE.
"""
import calendar
import copy
import csv
import datetime as dt
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('common_dcf',HERE.parents[1]/'model.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)

def custom_return(c,sc,recognition_discount=0,share_settlement=False):
 start=model.date(c['valuation_date']);end=start.replace(year=start.year+5)
 cash=model.excess_cash(c);debt=c['debt_m'];shares=c['shares_m']
 claims=c['senior_claims_m'];unused_revolver=24.5 if c['ticker']=='GRSD' else 0
 flows=[(start,-c['price'])];events=[];failed=False;peak_draw=0;totaldraw=0;refinance=0
 liquidity_checks=[]
 # Daily integration permits exact acquisition settlement, dividend and refinancing dates.
 # No investment interest is imputed to cash; loans bear the scenario borrowing rate.
 today=start
 while today<end:
  nextday=today+dt.timedelta(days=1)
  row=next(r for r in sc['years'] if r['year']==today.year)
  f=1/(366 if calendar.isleap(today.year) else 365)
  rate=(.08 if today<dt.date(2028,2,28) else (.10 if sc['wacc']>=.15 else .09))
  cash+=(model.operating(row)['fcff']-debt*rate*(1-row['tax_rate']))*f
  if c['ticker']=='OPRA':
   # Current July 2026 dividend is already removed from starting cash. No future
   # 2026 dividend is invented. January/July payment dates are analyst approximations.
   if today.year>=2027 and (today.month,today.day) in [(1,15),(7,15)]:
    div=min(row['dividend_per_share']/2,max(0,cash)/shares);cash-=div*shares
    if div:flows.append((today,div))
    events.append(dict(date=today.isoformat(),type='assumed regular dividend',cash_m=-div*shares))
   if today==dt.date(2026,9,30):cash-=1;claims-=1
   if today in [dt.date(2026,10,1),dt.date(2027,1,1),dt.date(2027,4,1),dt.date(2027,7,1)]:cash-=1.25;claims-=1.25
  else:
   if today==dt.date(2026,9,9):cash-=.5;claims-=.5
   if today.month in [1,4,7,10] and today.day==1 and today<dt.date(2028,2,28):
    pay=min(debt,2.8125);cash-=pay;debt-=pay
    events.append(dict(date=today.isoformat(),type='scheduled term amortization',cash_m=-pay))
   if today==dt.date(2027,4,1):
    face=27.966;claims-=26.479
    if share_settlement:
     # Explicit fixed issue-price stress. Acquisition debt is removed, and the
     # new shares receive subsequent value; no simultaneous cash claim remains.
     issue_price=c['price'];newshares=face/issue_price;shares+=newshares
     events.append(dict(date=today.isoformat(),type='acquisition settlement in shares at current price, stress assumption',new_shares_m=newshares,issue_price=issue_price))
    else:
     cash-=face;events.append(dict(date=today.isoformat(),type='acquisition settlement in cash',cash_m=-face))
   if today==dt.date(2028,2,28):
    pay=max(0,min(cash,debt));cash-=pay;debt-=pay;refinance=debt
    if sc['wacc']>=.15:
     failed=True;events.append(dict(date=today.isoformat(),type='adverse refinancing unavailable; equity impaired',unfunded_m=debt));break
    fee=debt*.02;debt+=fee
    events.append(dict(date=today.isoformat(),type='assumed refinance at 9%, 2% fee financed in new loan; no new acquisition',refinanced_m=debt,financed_fee_m=fee))
   if today==dt.date(2028,4,1):cash-=.149;claims-=.126
   if cash<0:
    draw=-cash
    if totaldraw+draw>unused_revolver+1e-8:
     failed=True;events.append(dict(date=today.isoformat(),type='cash need exceeds disclosed revolver availability',unfunded_m=totaldraw+draw-unused_revolver));break
    cash+=draw;debt+=draw;totaldraw+=draw;peak_draw=max(peak_draw,totaldraw)
  if (c['ticker']=='GRSD' and today<dt.date(2028,2,28)
      and today.month in (3,6,9,12) and nextday.month!=today.month):
   # Credit agreement sections 1.1 and 9.15(b): Availability + Qualified
   # Cash must be at least $15m at quarter end. Treating ALL modeled cash
   # and undrawn commitments as eligible is an optimistic upper bound;
   # controlled-account eligibility and other draw conditions are unknown.
   # cash excludes the operating reserve, which must be restored here.
   liquidity=cash+c.get('minimum_cash_m',0)+unused_revolver-totaldraw
   liquidity_checks.append(dict(date=today.isoformat(),liquidity_upper_bound_m=liquidity,
      required_m=15,shortfall_at_least_m=max(0,15-liquidity)))
  today=nextday
 horizon_ev=model.operating_value(sc,end)[0]
 other=sc.get('other_assets_m',c.get('other_assets_m',0))
 # Discount operating equity, not accumulated cash or nonoperating assets.
 operating_equity=max(0,horizon_ev-debt-max(0,claims))
 future=max(0,operating_equity*(1-recognition_discount)+cash+other) if not failed else 0
 if not failed and horizon_ev-debt-max(0,claims)<0:
  future=max(0,(horizon_ev-debt-max(0,claims))*(1-recognition_discount)+cash+other)
 flows.append((end,future/shares))
 covenant_shortfall=any(q['shortfall_at_least_m']>1e-8 for q in liquidity_checks)
 return dict(annualized_return=model.xirr(flows),future_equity_per_share=future/shares,exit_recognition_discount=recognition_discount,future_operating_ev_m=horizon_ev,horizon_debt_m=debt,horizon_cash_m=cash,unpaid_claims_m=max(0,claims),horizon_shares_m=shares,additional_revolver_draw_m=peak_draw,refinancing_required_m=refinance,financing_failed=failed,
   liquidity_checks=liquidity_checks,unresolved_covenant_shortfall=covenant_shortfall,
   return_status=('conditional on unmodeled covenant cure; no cure cost or dilution included' if covenant_shortfall else 'scenario assumptions apply'),
   covenant_scope=('Quarter-end liquidity upper bound only. Leverage, fixed-charge coverage, cash eligibility and replacement-loan terms remain unverified. A shortfall is a modeled funding dependency, not a reported breach or assumed total loss.' if c['ticker']=='GRSD' else 'not applicable'),
   events=events,cashflows=[dict(date=d.isoformat(),per_share=v) for d,v in flows])

def stresses(c):
 base=copy.deepcopy(c['scenarios']['base']);out=[]
 def add(label,sc,cc=None):
  val=model.equity_value(cc or c,sc)
  out.append(dict(stress=label,fair_value_per_share=val['fair_value_per_share'],enterprise_value_m=val['enterprise_value_m']))
 if c['ticker']=='OPRA':
  for p in [.25,.5]:
   sc=copy.deepcopy(base)
   for row in sc['years'][1:]:
    q=row['segments'][1];lost=q['revenue']*p;q['revenue']-=lost
    # 60% marginal cash profit loss, with some avoided traffic/marketing expense.
    oldmargin=q['ebit_margin'];q['ebit_margin']=(q['revenue']*oldmargin-lost*(.60-oldmargin))/q['revenue']
   add(f'Query payments {p:.0%} permanently lower from 2027; 60% contribution loss',sc)
  sc=copy.deepcopy(base);sc['other_assets_m']=0;add('OPay worth zero; operating forecast unchanged',sc)
  sc=copy.deepcopy(base)
  for row in sc['years']:
   row['segments'][0]['ebit_margin']-=.03
  add('Advertising inventory/partner costs 3pp of ad revenue higher',sc)
 else:
  sc=copy.deepcopy(base)
  for row in sc['years'][1:]:
   row['segments'][1]['revenue']*=.30
   row['segments'][1]['ebit_margin']-=.15
   row['corporate_cost']+=3
  add('Injunction/data rights disruption: data sales -70% from 2027, data margin -15pp, annual legal/repair cost $3m',sc)
  for damages in [10,25,50,100]:
   cc=copy.deepcopy(c);cc['senior_claims_m']+=damages
   add(f'Additional litigation claim ${damages}m; base operations survive (not estimated legal outcome)',base,cc)
  sc=copy.deepcopy(base)
  for row in sc['years'][1:]:
   years=row['year']-2026;row['segments'][0]['revenue']*=.90**years
   row['segments'][0]['ebit_margin']-=.05
  add('Marketing 10% annual incremental erosion plus 5pp lower margin',sc)
  cc=copy.deepcopy(c);cc['shares_m']+=5.374306;cc['other_assets_m']+=5.374306*8.14
  add('All existing options exercised at weighted strike, including all founders awards; upside option dilution bound',c['scenarios']['upside'],cc)
 return out

def main():
 companies=json.loads((HERE/'inputs.json').read_text());results=[];annual=[]
 for c in companies:
  result=model.run_company(c)
  result['dated_return_cases']={}
  for name,sc in c['scenarios'].items():
   result['dated_return_cases'][name]={str(int(discount*100)):custom_return(c,sc,discount) for discount in [0,.2,.4]}
   if c['ticker']=='GRSD':result['dated_return_cases'][name]['cash_constrained_share_settlement']=custom_return(c,sc,.2,True)
   for row in model.forecast_years(sc):
    annual.append(dict(ticker=c['ticker'],scenario=name,year=row['year'],**model.operating(row),**{k:row.get(k,0) for k in ['corporate_cost','tax_rate','da','capex','delta_nwc','shares_m','dividend_per_share']}))
  result['adverse_stresses']=stresses(c)
  result['unresolved_covenant_shortfall']=any(v['0']['unresolved_covenant_shortfall'] for v in result['dated_return_cases'].values())
  result['return_status']='unconfirmed: aggregate returns include unpriced covenant cure' if result['unresolved_covenant_shortfall'] else 'scenario assumptions apply'
  result['base_mos']=1-c['price']/result['scenarios']['base']['fair_value_per_share']
  for discount in ['0','20','40']:
   cashflows={}
   for name,sc in c['scenarios'].items():
    for item in result['dated_return_cases'][name][discount]['cashflows']:
     cashflows[item['date']]=cashflows.get(item['date'],0)+sc['probability']*item['per_share']
   result[f'probability_weighted_cashflow_irr_exit_discount_{discount}']=model.xirr([(model.date(d),v) for d,v in sorted(cashflows.items())])
   result[f'weighted_average_scenario_irr_exit_discount_{discount}']=sum(sc['probability']*result['dated_return_cases'][n][discount]['annualized_return'] for n,sc in c['scenarios'].items())
  results.append(result)
 (HERE/'valuations.json').write_text(json.dumps(results,indent=2)+'\n')
 with (HERE/'annual_forecasts.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(annual[0]));w.writeheader();w.writerows(annual)
 for r in results:
  print(r['ticker'],'price',r['price'],'fair',round(r['probability_weighted_fair_value'],2),'cases',[round(v['fair_value_per_share'],2) for v in r['scenarios'].values()])
  print('  recognition IRR',[round(r[f'probability_weighted_cashflow_irr_exit_discount_{d}']*100,1) for d in ['0','20','40']])
  print('  adverse',r['adverse_stresses'])

if __name__=='__main__':main()
