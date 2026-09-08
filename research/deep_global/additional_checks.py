"""Cash access, no-rerating returns, combined adverse paths, auditable probabilities."""
import json,copy,pathlib,sys,datetime as dt
P=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]));import model
FX=6.7108
cs=json.loads((P/'inputs.json').read_text());out={}
def returns(c,sc,discount=0):
 r=model.shareholder_return(c,sc)
 flows=[(dt.date.fromisoformat(f['date']),f['per_share']) for f in r['cashflows']]
 # Forecast VIPS annual dividend is April24 based on recent cadence; already-paid2026 excluded.
 if c['ticker']=='VIPS':flows=[(dt.date(d.year,4,24) if j not in (0,len(flows)-1) else d,v) for j,(d,v) in enumerate(flows)]
 flows[-1]=(flows[-1][0],flows[-1][1]*(1-discount))
 return dict(annualized_return=model.xirr(flows),terminal_price=flows[-1][1],cashflows=[dict(date=d.isoformat(),per_share=v) for d,v in flows])
def fixed_discount_buyback(c,sc,discount=.35,annual_buyback_m=400):
 start=model.date(c['valuation_date']);end=start.replace(year=start.year+5)
 cash=model.excess_cash(c);shares=c['shares_m'];debt=c['debt_m'];flows=[(start,-c['price'])];events=[]
 for row in sc['years']:
  ps,pe=model.period(row);overlap=max(0,(min(pe,end)-max(ps,start)).days)
  if not overlap:continue
  f=overlap/(pe-ps).days;interest=debt*c['debt_interest_rate']*(1-row['tax_rate'])
  cash+=(model.operating(row)['fcff']-interest)*f
  pay=dt.date(row['year'],4,24)
  if start<pay<=end:
   div=row['dividend_per_share'];cash-=div*shares
   if div:flows.append((pay,div))
  if start<pe<=end:
   ev=model.operating_value(sc,pe)[0]
   equity=ev+cash+c['other_assets_m']-debt-c['senior_claims_m']
   traded=(1-discount)*equity/shares
   buy=min(annual_buyback_m,max(0,cash)) if row['year']>2026 else 0
   retired=min(shares*.5,buy/traded)
   cash-=buy;shares-=retired
   events.append(dict(year=row['year'],buyback_m=buy,execution_price=traded,retired_shares_m=retired,shares_after_m=shares))
 ev=model.operating_value(sc,end)[0];eq=ev+cash+c['other_assets_m']-debt-c['senior_claims_m']
 flows.append((end,(1-discount)*eq/shares))
 return dict(annualized_return=model.xirr(flows),terminal_price=flows[-1][1],events=events,cashflows=[dict(date=d.isoformat(),per_share=v) for d,v in flows],notes='Supplemental assumption:400mUSDyearly2027-2030, sharesrepurchasedat35%discounttopre-buybackintrinsicclaims. Noautomaticdiscountclosure. BaseDCFdoesnotassumethis. Aprildivdates; buybacksDecember31; noneafter2030asfiveyearhorizonSep2031. SBCalreadychargedGAAPEBITsoallmodeledrepurchasesincremental.')
for c in cs:
 name=c['ticker'];r=model.run_company(c);base=c['scenarios']['base'];d={}
 d['persistent_discount_returns']={case:{str(disc):returns(c,s,disc) for disc in [0,.20,.40]} for case,s in c['scenarios'].items()}
 currentdisc=1-c['price']/r['scenarios']['base']['fair_value_per_share']
 d['unchanged_current_base_discount']=dict(discount=currentdisc,**returns(c,base,currentdisc))
 d['loss_of_all_shareholder_access_tail']={str(p):dict(weighted_value=(1-p)*r['probability_weighted_fair_value'],upside=(1-p)*r['probability_weighted_fair_value']/c['price']-1) for p in [.05,.10]}
 # Cash haircut is independent sensitivity, not embedded in WACC or operating probabilities.
 pool=model.excess_cash(c)+c['other_assets_m']
 d['current_financial_asset_access_sensitivity']={str(access):max(0,r['scenarios']['base']['fair_value_per_share']-(1-access)*pool/c['shares_m']) for access in [0,.5,1]}
 d['fx_sensitivity']={str(move):max(0,r['scenarios']['base']['fair_value_per_share']/(1+move)) for move in [-.10,0,.10]}
 d['probability_sensitivity']={str(weights):sum(w*r['scenarios'][case]['fair_value_per_share'] for w,case in zip(weights,['downside','base','upside'])) for weights in [[.25,.55,.2],[.4,.5,.1],[.5,.4,.1]]}
 # All assumptions adverse together; no piecemeal fake downside.
 bad=copy.deepcopy(c);s=bad['scenarios']['base']
 for row in s['years']:
  if row['year']>=2027:
   for seg in row['segments']:seg['revenue']*=.80;seg['ebit_margin']-=.04 if name=='PDD' else .02
   row['capex']*=1.3;row['delta_nwc']+=1000/FX if name=='PDD' else 300/FX
 s['terminal_growth']=0
 bad['other_assets_m']*=.5
 d['combined_adverse']=dict(fair_value=model.equity_value(bad,s)['fair_value_per_share'],returns_at_40pct_persistent_discount=returns(bad,s,.4),notes='Base2027onwardrevenue20%lower,marginsPDD4pp/VIPS2pplower,capex30%higher,NWCadditional1bn/0.3bnRMBannual,terminalg0,otherinvestments50%loss,40%futuretradingdiscount.')
 if name=='PDD':
  flat=copy.deepcopy(base)
  for row in flat['years']:
   revenue=sum(s['revenue'] for s in row['segments']);margin=(93102.131/FX)/revenue
   for seg in row['segments']:seg['ebit_margin']=margin
  d['flat_2025_EBIT']=dict(fair_value=model.equity_value(c,flat)['fair_value_per_share'],return_at_20pct_discount=returns(c,flat,.2),return_at_40pct_discount=returns(c,flat,.4),notes='EBITfixedRMB93.102bn2026-35;2026knownH147.33bn;maintainbasecapex/NWC/tax. Thereafterterminalnominalg1.5%withrequiredreinvestment.')
  offshore_floor=(282132-20000)/FX
  onshore=max(0,pool-offshore_floor)
  d['onshore_only_asset_access_stress']=dict(assumed_accessible_offshore_USD_m=offshore_floor,assumed_onshore_USD_m=onshore,base_if_onshore_current_assets_zero=max(0,r['scenarios']['base']['fair_value_per_share']-onshore/c['shares_m']),notes='Decoutside-mainlandcash+shortinvestment282132mRMB heldconstant;subtract20000operatingcash; Junegeographyunknown. Excludesallcurrentonshoreassetvaluebutdoesnotdeletefutureoperatingearnings; diagnostic, notcompletepermanentVIEfailurecase.')
  d['portfolio_shock']=dict(fair_value_after_50pct_loss_on_Dec_equity_security_proxy=r['scenarios']['base']['fair_value_per_share']-.5*66033.596/FX/c['shares_m'])
  extra_tax=150575.935*.10-10000
  remitted=copy.deepcopy(base)
  for row in remitted['years']:row['tax_rate']=1-(1-row['tax_rate'])*.9
  d['remittance_tax_sensitivity']=dict(undistributed_earnings_RMB_m=150575.935,recorded_tax_payable_reserved_RMB_m=27637,additional_unrecorded_remittance_reserve_RMB_m=10000,reserve_percent_of_earnings_pool=10000/150575.935,base_with_full_10pct_reserve_on_existing_pool=r['scenarios']['base']['fair_value_per_share']-extra_tax/FX/c['shares_m'],base_without_additional_reserve=r['scenarios']['base']['fair_value_per_share']+10000/FX/c['shares_m'],base_with_10pct_withholding_on_all_future_after_tax_operating_profit=model.equity_value(c,remitted)['fair_value_per_share'],notes='20-F Note15 F-34/F-36:10% statutory outbound withholding subject to treaty relief; majority of earnings intended indefinitely reinvested and associated deferred tax not provided. Existing recorded taxes payable and additional unprovided remittance reserve are distinct. Future-profit test increases operating cash tax25% to32.5%, retaining the existing cash reserve; maximum all-profit remittance assumption, not a legal conclusion on each entity. No shareholder-level tax modeled.')
 else:
  d['supplemental_buyback_case']=fixed_discount_buyback(c,base)
  d['claim_uncertainties']=dict(if_REIT_tax_already_paid=r['scenarios']['base']['fair_value_per_share']+1630/FX/c['shares_m'],if_other_investments_realized_at_full_book=r['scenarios']['base']['fair_value_per_share']+.5*4980.862/FX/c['shares_m'],if_all_nonoperating_investments_worth_zero=r['scenarios']['base']['fair_value_per_share']-c['other_assets_m']/c['shares_m'])
 out[name]=d
(P/'additional_checks.json').write_text(json.dumps(out,indent=2)+'\n')
for n,d in out.items():print(n,'unchangeddiscountIRR',d['unchanged_current_base_discount']['annualized_return'],'20/40baseIRR',[d['persistent_discount_returns']['base'][str(x)]['annualized_return'] for x in [.2,.4]],'combined',d['combined_adverse']['fair_value']);print('tail',d['loss_of_all_shareholder_access_tail']);print('flat',d.get('flat_2025_EBIT',{}).get('fair_value'),'buyback',d.get('supplemental_buyback_case',{}).get('annualized_return'))
