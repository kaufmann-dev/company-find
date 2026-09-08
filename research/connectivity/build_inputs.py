"""Analyst-authored Comcast scenario inputs, not consensus or company guidance.

Run from repository root: python research/connectivity/build_inputs.py
USD millions and customer/line/subscriber counts in millions. See research.md.
"""
import csv
import datetime as dt
import json
from pathlib import Path

P = Path(__file__).resolve().parent
K = 'https://www.sec.gov/Archives/edgar/data/1166691/000162828026004994/cmcsa-20251231.htm'
Q = 'https://www.sec.gov/Archives/edgar/data/1166691/000162828026049360/cmcsa-20260630.htm'
sources = [
 {'id':'C1','url':K,'publication_date':'2026-02-03','section':'pp.62-65 consolidated statements; Note 2 segments; Note 8 investments/VIE; Note 11 benefits; Note 12 shares','supports':'2023-25 history, segment economics, deferred compensation, ownership and governance'},
 {'id':'C2','url':Q,'publication_date':'2026-07-23','section':'cover; pp.1-4 statements; Notes 2,3,6,7,9; MD&A capital resources','supports':'June balance, July15 shares, Q2 dilution, transactions, H1 results and operating drivers'},
 {'id':'C3','url':'https://www.cmcsa.com/node/45906','publication_date':'2026-07-23','section':'operating highlights; financial tables and reconciliations','supports':'48m Peacock paid subscribers, first profitable quarter, broadband/wireless and cash flow'},
 {'id':'C4','url':'https://www.cmcsa.com/static-files/ced447a4-4823-4904-b398-bab2a392d1c7','publication_date':'2026-06-29','section':'separation presentation','supports':'planned NBCUniversal and Sky separation mid-2027, no completed distribution yet'},
 {'id':'C5','url':'https://www.sec.gov/Archives/edgar/data/732717/000073271726000294/t-2q2026exhibit991.htm','publication_date':'2026-07-22','section':'Second-Quarter Highlights; Outlook and Capital Allocation Plan','supports':'AT&T 38.6m fiber locations, management >40m2026 and >60m2030, $23-24bn annual capital plan and convergence competition'},
 {'id':'C6','url':'https://ir.charter.com/news-releases/news-release-details/charter-announces-second-quarter-2026-results','publication_date':'2026-07-24','section':'operating results, Capital Expenditures, Liquidity and Financing','supports':'competing cable investment, pressure on EBITDA, debt and Cox integration'},
 {'id':'C7','url':'https://www.sec.gov/Archives/edgar/data/1283699/000128369926000100/tmus06302026ex991.htm','publication_date':'2026-07-23','section':'operating highlights; non-GAAP reconciliation','supports':'wireless/broadband competitive platform; Q2 service revenue19bn, Core EBITDA9.5bn; SBC excluded in that measure'},
 {'id':'C8','url':'https://www.sec.gov/Archives/edgar/data/1166691/000162828026049360/0001628280-26-049360-index.html','publication_date':'2026-07-23','section':'Filing Detail','supports':'filing publication date'},
 {'id':'C9','url':'https://api.massive.com/v2/snapshot/locale/us/markets/stocks/tickers/CMCSA','publication_date':'2026-09-08','section':'ticker.min.c and ticker.min.t; raw quote_CMCSA.json','supports':'intraday stock price; market bridge uses earlier latest disclosed June balance, not an intraday balance'},
 {'id':'C11','url':'https://www.cmcsa.com/static-files/b269b35e-94ff-43d2-8f05-858c92bb7488','publication_date':'2026-07-23','section':'pp.1-3 pro forma revenue/EBITDA; p.6 subscribers/passings; remaining pages capital and notes','supports':'recast 2024-25 ongoing business comparison: Media EBITDA -123/164m, proforma total EBITDA35118/34454m; Q2 consumer weakness and cohort monetization required'},
 {'id':'C12','url':'https://www.nbcuniversal.com/article/nba-and-wnba-return-nbcuniversal-11-year-agreement-regular-season-and-playoff-basketball-nbc-peacock','publication_date':'2024-07-24','section':'announcement','supports':'eleven-year NBA agreement beginning2025-26; do not assume rights cost disappears afterforecast'},
]
specs={
 'downside':dict(p=.30,wacc=.10,g=.005,roic=.10,
  bb=[28.5,27.7,26.7,25.7,24.7,23.8,23.0,22.3,21.7,21.2],
  arpu=[74,70.5,69,69,69.5,70,70.5,71,71.5,72],
  wireless=[10.15,11.4,12.4,13.2,13.8,14.3,14.7,15,15.2,15.4],
  wireless_arpu=[33,31,31,31.5,32,32,32.5,32.5,33,33],
  video_decay=.09,intl_g=.01,ad_g=-.02,other_decay=.09,
  res_ebitda_margin=[.35,.345,.34,.33,.33,.33,.33,.33,.33,.33],
  business=[10700,10900,11100,11400,11700,12000,12300,12600,12900,13200],
  business_margin=[.56,.545,.535,.53,.53,.53,.53,.53,.53,.53],
  peacock_subs=[47,48,49,50,51,52,53,54,55,56],
  peacock_arpu=[11.9,11.8,12,12.1,12.2,12.4,12.5,12.6,12.7,12.8],
  linear_decay=.07,peacock_margin=[-.08,-.09,-.08,-.06,-.04,-.02,0,.02,.04,.05],linear_margin=[.06,.06,.06,.06,.06,.06,.06,.06,.06,.06],
  studios=[12300,11200,11000,11200,11400,11600,11800,12000,12200,12400],studio_margin=[.10,.07,.07,.08,.08,.085,.085,.085,.085,.085],
  parks=[10300,10000,10000,10200,10600,11500,12500,12900,13300,13700],park_margin=[.29,.24,.24,.25,.26,.25,.26,.27,.28,.29],
  da=[14900,14600,14500,14500,14500,14800,15000,15200,15400,15600],
  capex=[15100,15800,16000,16600,16700,16000,14700,14400,14100,13900],
  tax=[.22,.24,.255,.255,.255,.255,.255,.255,.255,.255],
  corp=[2650,3450,3300,2950,2850,2900,2960,3020,3080,3140]),
 'base':dict(p=.50,wacc=.0875,g=.02,roic=.13,
  bb=[28.5,27.95,27.4,26.95,26.6,26.4,26.25,26.2,26.2,26.2],
  arpu=[74,72.5,72.5,73.2,74.3,75.7,77.2,78.7,80.3,82],
  wireless=[10.15,11.9,13.6,15.1,16.4,17.5,18.4,19.2,19.9,20.5],
  wireless_arpu=[33,33,33.5,34,34.5,35,35.2,35.5,35.7,36],
  video_decay=.06,intl_g=.04,ad_g=.01,other_decay=.07,
  res_ebitda_margin=[.36,.36,.365,.37,.375,.38,.38,.38,.38,.38],
  business=[10700,11200,11760,12350,12970,13620,14230,14870,15540,16240],
  business_margin=[.56,.56,.565,.565,.57,.57,.57,.57,.57,.57],
  peacock_subs=[47,50,53,56,59,62,64,66,68,70],
  peacock_arpu=[11.9,12.1,12.4,12.7,13,13.3,13.6,13.8,14,14.2],
  linear_decay=.04,peacock_margin=[-.04,0,.04,.08,.11,.13,.15,.16,.17,.18],linear_margin=[.07,.085,.085,.085,.085,.085,.085,.085,.085,.085],
  studios=[12300,12300,12800,13000,13400,13700,14100,14500,14900,15300],studio_margin=[.12,.11,.12,.12,.125,.125,.13,.13,.13,.13],
  parks=[10300,11000,11700,12300,12900,14200,15100,15700,16300,16900],park_margin=[.30,.31,.32,.325,.33,.31,.325,.33,.33,.33],
  da=[14900,14300,14100,14200,14500,14900,15300,15600,15900,16200],
  capex=[14900,15100,15500,16100,16300,15600,14300,14000,13900,13900],
  tax=[.20,.22,.24,.25,.255,.255,.255,.255,.255,.255],
  corp=[2550,3050,2850,2550,2500,2550,2600,2650,2700,2750]),
 'upside':dict(p=.20,wacc=.08,g=.025,roic=.16,
  bb=[28.5,28.2,28,28,28.15,28.35,28.6,28.85,29.1,29.35],
  arpu=[74,73,74,76,78,80,82,84,86,88],
  wireless=[10.15,12.2,14.4,16.5,18.3,19.9,21.3,22.5,23.6,24.6],
  wireless_arpu=[33,34,35,36,36.5,37,37.5,38,38.5,39],
  video_decay=.04,intl_g=.05,ad_g=.02,other_decay=.05,
  res_ebitda_margin=[.375,.38,.39,.40,.405,.41,.412,.415,.415,.415],
  business=[10700,11350,12080,12860,13690,14510,15380,16230,17120,18060],
  business_margin=[.56,.565,.57,.575,.58,.58,.58,.58,.58,.58],
  peacock_subs=[47,52,58,64,70,76,81,85,89,93],
  peacock_arpu=[11.9,12.4,12.8,13.2,13.6,14,14.3,14.6,14.9,15.2],
  linear_decay=.025,peacock_margin=[0,.06,.11,.15,.18,.20,.21,.22,.23,.23],linear_margin=[.09,.10,.11,.12,.13,.13,.13,.13,.13,.13],
  studios=[12300,13000,13600,14200,14800,15400,16000,16600,17300,18000],studio_margin=[.13,.14,.15,.15,.155,.155,.16,.16,.16,.16],
  parks=[10300,11500,12600,13600,14600,16000,17400,18500,19400,20200],park_margin=[.31,.33,.35,.35,.35,.335,.35,.35,.35,.35],
  da=[14900,14500,14600,15000,15500,16200,16800,17400,17900,18400],
  capex=[14900,15200,15600,16200,16500,16000,15400,15400,15600,15800],
  tax=[.19,.20,.22,.24,.25,.25,.25,.25,.25,.25],
  corp=[2500,2800,2600,2450,2500,2550,2600,2650,2700,2750]),
}
quote=json.loads((P/'quote_CMCSA.json').read_text())['structuredContent']['result']
quote=next(csv.DictReader(quote.splitlines()))
fx=next(csv.DictReader(json.loads((P/'quote_GBPUSD.json').read_text())['structuredContent']['result'].splitlines()))
itv_consideration=1600*float(fx['c'])
sources.append(dict(id='C10',url='https://api.massive.com/v2/aggs/ticker/C:GBPUSD/prev',publication_date='2026-09-08',section='previous forex daily bar; quote_GBPUSD.json',supports='GBPUSD1.3546 bar timestamp2026-09-07T23:59:59.999Z; future 2027 transaction FX remains uncertain'))
basic=3548.636573
shares=basic+6
company=dict(ticker='CMCSA',company='Comcast Corporation — combined current economic claims',currency='USD',valuation_date='2026-09-08',price=float(quote['ticker_min_c']),price_timestamp=dt.datetime.fromtimestamp(int(quote['ticker_min_t'])/1000,dt.timezone.utc).isoformat(),shares_m=shares,basic_shares_m=basic,balance_date='2026-06-30',cash_m=7661,minimum_cash_m=2500,debt_m=90381,senior_claims_m=7882,other_assets_m=4576,debt_interest_rate=.0475,status='fully modelled comparison; attractiveness pending calculated valuation',
 accounting_notes='Combined Comcast+future NBCUniversal/Sky distribution claims; exclude already separated Versant and sold Sky Germany from forward years. July15 basic shares include ClassB, add Q2 6m dilutive proxy. GAAP-like EBIT retains SBC; no SBC addback or assumed future buyback accretion/dilution. Capex includes cash software/intangibles and property; program amortization remains in expense and content investment timing in NWC. Debt includes consolidated Beijing; operating leases remain operating expense, not duplicated debt. Senior claims7882=5097 deferred compensation (Dec2025 latest detailed obligation)+185 redeemableNCI+1500 analyst minority fair-value reserve+1100 unfundedAtairos reserve. Otherassets4576=50% June7828 noncurrent investments+662 Dec2025 life-insurance offset. No Hulu/Versant value. ITV full up-to consideration conservatively charged as2027 reinvestment2160 (GBPUSD1.35 analyst assumption, no speculative earnings credit); no separate claim deduction. Base corporate expense includes 40m Atairos fee, incremental separation/dual-company costs; taxes normalize. Noncommonclaim uncertainty stressed separately. Deferred compensation reserve treated as a present claim; its cash settlement is excluded from future operating NWC to avoid double deduction. Cash reserve is analyst assumption, not legally restricted.',
 history=[dict(year=y,revenue=r,ebit=e,da=d,capex=c,cfo=f,sbc=s,source_ids=['C1'],notes='As reported, includes Versant and Sky Germany; not comparable with 2026 forward perimeter. Capex includes property, software/intangibles and Beijing construction. D&A below from cash-flow statement, rounding can differ from income statement.') for y,r,e,d,c,f,s in [(2023,121572,23314,14336,15677,28501,1241),(2024,123731,23297,14802,15246,27673,1288),(2025,123707,20672,16210,14419,33643,1288)]],sources=sources,scenarios={})
drivers={}
for name,s in specs.items():
 rows=[]; ds=[]
 for i,y in enumerate(range(2026,2036)):
  # Annual average billed domestic subscriber and line stocks, not annual additions.
  broadband=s['bb'][i]*s['arpu'][i]*12
  wireless=s['wireless'][i]*s['wireless_arpu'][i]*12
  device=s['wireless'][i]*161.6
  international=5000*(1+s['intl_g'])**i
  video=24200*(1-s['video_decay'])**i
  ads=3800*(1+s['ad_g'])**i
  other=4500*(1-s['other_decay'])**i
  residential=broadband+wireless+device+international+video+ads+other
  peacock=s['peacock_subs'][i]*s['peacock_arpu'][i]*12
  # Peacock ARPU includes subscriptions AND advertising. Do not add ads again.
  # 2026 has Olympics/WorldCup boosts: recurring 16.0bn linear base +2.0bn event revenue.
  linear=16000*(1-s['linear_decay'])**i + (2000 if y%2==0 else 0)
  media=linear+peacock
  media_ebitda=linear*s['linear_margin'][i]+peacock*s['peacock_margin'][i]
  gross=[residential,s['business'][i],media,s['studios'][i],s['parks'][i]]
  margins=[s['res_ebitda_margin'][i],s['business_margin'][i],media_ebitda/media,s['studio_margin'][i],s['park_margin'][i]]
  # The exact D&A allocation below is an analyst allocation, not disclosed segment GAAP EBIT.
  da_allocation=[.56,.06,.15,.06,.17]
  names=['Residential Connectivity and Platforms','Business Services Connectivity','Media including Peacock','Studios','Theme Parks']
  segments=[dict(name=n,revenue=round(r,4),ebit_margin=m-s['da'][i]*w/r,volume=None,volume_unit='see operating_drivers.json; mixed products',price=None) for n,r,m,w in zip(names,gross,margins,da_allocation)]
  # Reported segment revenue is gross; eliminate internal licensing/distribution once.
  # Other operations retained after Germany sale assumed2bn; internal revenue based on media+studio gross.
  elimination=-(media+s['studios'][i])*.20
  other_revenue=2000*(1.02)**i
  segments += [dict(name='Other revenue less intersegment eliminations',revenue=round(other_revenue+elimination,4),ebit_margin=0,volume=None,volume_unit='USDm reconciliation',price=None)]
  # NWC includes net program/content investment and wireless instalment receivables.
  nwc=(650 if y%2==0 else 350)+(100 if name=='upside' else 0)
  if name=='downside': nwc+=300
  capex=s['capex'][i]+(itv_consideration if y==2027 else 0)
  # Explicit 2032-35 replacement/growth reinvestment normalization. At2035,
  # net reinvestment=Nopat*g/ROIC, exactly consistent with terminal economics.
  if y>=2032:
   ebit=sum(z['revenue']*z['ebit_margin'] for z in segments)-s['corp'][i]
   normalized_capex=s['da'][i]+ebit*(1-s['tax'][i])*s['g']/s['roic']-nwc
   weight=(y-2031)/4
   capex=capex*(1-weight)+normalized_capex*weight
  row=dict(year=y,period_end=f'{y}-12-31',segments=segments,corporate_cost=s['corp'][i],tax_rate=s['tax'][i],da=s['da'][i],capex=capex,delta_nwc=nwc,shares_m=shares,dividend_per_share=(.90 if name=='downside' and y>=2028 else 1.32),net_debt_issuance=0,new_equity_issuance=0,notes='All forward figures analyst assumptions. Underlying EBITDA-to-GAAP EBIT allocation deducts total D&A once; GAAP-like cost base retains SBC. 2027 capex includes2160 conservative ITV total consideration reserve with no earnings credit. Corporate includes separation/stranded costs. Fiscal2026 full-year forecasts use reportedH1 as anchor; rootengine proratesremainingstub.')
  rows.append(row)
  passings=59.95+1.05*i
  ds.append(dict(year=y,domestic_average_broadband_subscribers_m=s['bb'][i],broadband_monthly_realized_revenue_usd=s['arpu'][i],domestic_broadband_revenue_m=broadband,domestic_average_wireless_lines_m=s['wireless'][i],wireless_monthly_service_arpu_usd=s['wireless_arpu'][i],wireless_service_revenue_m=wireless,wireless_device_revenue_m=device,international_connectivity_revenue_m=international,video_revenue_m=video,advertising_revenue_m=ads,other_residential_revenue_m=other,peacock_average_paid_subscribers_m=s['peacock_subs'][i],peacock_monthly_total_arpu_usd=s['peacock_arpu'][i],peacock_revenue_m=peacock,linear_media_revenue_m=linear,assumed_network_passings_m=passings,implied_comcast_broadband_penetration=s['bb'][i]/passings,network_usable_throughput='unavailable; passings are not throughput; no shortage claim',competitor_overlap_and_local_fwa_capacity='unavailable; cannot add national fiber targets to Comcast local capacity',value_capture='broadband/wireless bundle offsets price/subscriber pressure to scenario extent; no scarcity premium'))
 company['scenarios'][name]=dict(probability=s['p'],wacc=s['wacc'],terminal_growth=s['g'],terminal_roic=s['roic'],years=rows)
 drivers[name]=ds
company['accounting_notes']=company['accounting_notes'].replace('2160 (GBPUSD1.35 analyst assumption','2167.36 (Massive GBPUSD1.3546 September7 daily close')
company['status']='unconfirmed research candidate; valuation headroom is probability-sensitive and bundled broadband monetization remains unresolved'
final_quote=json.loads((P.parent.parent/'outputs'/'market_quotes.json').read_text())['CMCSA']
company['price']=final_quote['price']
company['price_timestamp']=final_quote['price_timestamp']
company['accounting_notes']+=' Corporatecosts include200m annual capitalizedSBC economic cost alongside expensedSBC already retained. Final stockquote uses synchronized outputs/market_quotes.json.'
company['recast_operating_history']=[dict(year=2024,revenue=115459,adjusted_ebitda=35118,media_adjusted_ebitda=-123,peacock_ebitda=-1796,residential_ebitda=27060,source_ids=['C11'],notes='pro forma removes Versant/Germany; not GAAP EBIT; SBC treatment follows company reconciliation'),dict(year=2025,revenue=115552,adjusted_ebitda=34454,media_adjusted_ebitda=164,peacock_ebitda=-1085,residential_ebitda=26364,source_ids=['C11'],notes='pro forma removes Versant/Germany; not GAAP EBIT')]
for sc in company['scenarios'].values():
 for row in sc['years']:
  row['notes']=row['notes'].replace('2160','2167.36')+' 2032-35 capex explicitly transitions to NOPAT*g/ROIC net reinvestment, avoiding a terminal cash-flow discontinuity.'
(P/'inputs.json').write_text(json.dumps([company],indent=2)+'\n')
(P/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
(P/'operating_drivers.json').write_text(json.dumps(dict(status='analyst scenarios, not measured national supply balance',units='USD millions, customer stocks in millions, monthly ARPU USD',sources=['C1','C2','C3','C5','C6','C7'],scenarios=drivers),indent=2)+'\n')
