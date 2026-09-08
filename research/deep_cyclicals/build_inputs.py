"""All forecasts are analyst assumptions. Reproduce python research/deep_cyclicals/build_inputs.py.
Amounts originate in EUR millions for STLA, translated at a frozen Massive EURUSD rate.
Captive equity distributions = earnings - increase in required equity capital.
"""
from pathlib import Path
import json,datetime as dt,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]))
import model
FX=1.16276
START=dt.date(2026,9,8); HORIZON=dt.date(2031,9,8)
STUB=(dt.date(2026,12,31)-START).days/365
NAMES=['North America','Enlarged Europe','Middle East and Africa','South America','Asia Pacific']
# Thousand vehicles times thousand EUR per vehicle gives EUR millions.
# Net realization includes parts/other regional sales per shipped vehicle, not consumer sticker price.
CONFIG={
'downside':dict(p=.30,w=.13,g=.005,roic=.08,vol0=[1650,2690,460,955,55],vol30=[1450,2500,480,950,50],vol35=[1450,2450,510,960,45],price0=[40.8,21.5,21.2,16.8,29.5],pg=[-.005,0,.005,.005,0],m0=[.014,-.007,.10,.075,-.02],m30=[.025,.005,.075,.065,0],m35=[.025,.007,.075,.065,0],corp=[1700,1800,1700,1500,1400,1300,1200,1150,1100,1100],cap=[7900,8100,7800,7500,7300,7300,7350,7400,7450,7500],da=[6250,6100,6000,5950,5900,5900,5920,5940,5960,5980],legacy=[1100/STUB,2200,2000,1700,500,250,0,0,0,0],bankni=[250,-250,200,350,400,420,440,460,480,500],bankcap=[9700,10000,10000,10000,10000,10050,10100,10150,10200,10250],bankke=.145),
'base':dict(p=.50,w=.11,g=.015,roic=.10,vol0=[1690,2780,470,980,60],vol30=[1900,2850,510,1030,60],vol35=[1950,2880,540,1090,60],price0=[40.8,21.7,21.3,16.9,30],pg=[.006,.008,.012,.012,.005],m0=[.025,.001,.115,.085,0],m30=[.055,.030,.10,.09,.02],m35=[.055,.030,.10,.09,.02],corp=[1400,1300,1150,1050,1000,1020,1040,1060,1080,1100],cap=[7500,7600,7700,7800,7900,8000,8100,8200,8300,8400],da=[6300,6350,6400,6500,6600,6700,6800,6900,7000,7100],legacy=[1100/STUB,1750,1500,1250,0,0,0,0,0,0],bankni=[450,550,650,720,800,850,880,905,930,955],bankcap=[9500,9900,10200,10450,10650,10850,11015,11180,11350,11520],bankke=.125),
'upside':dict(p=.20,w=.10,g=.02,roic=.13,vol0=[1720,2820,480,990,65],vol30=[2100,3050,560,1100,80],vol35=[2220,3190,625,1210,90],price0=[41,21.8,21.4,17,30.5],pg=[.009,.011,.015,.015,.01],m0=[.033,.006,.12,.09,.02],m30=[.075,.043,.12,.10,.04],m35=[.070,.040,.115,.095,.04],corp=[1300,1150,1000,950,950,970,990,1010,1030,1050],cap=[7700,7950,8200,8400,8700,8900,9100,9300,9500,9700],da=[6300,6400,6500,6700,6900,7100,7300,7500,7700,7900],legacy=[1100/STUB,1750,1500,1250,0,0,0,0,0,0],bankni=[500,700,850,1000,1150,1230,1300,1370,1440,1510],bankcap=[9600,10050,10450,10800,11150,11500,11750,12000,12250,12500],bankke=.115)
}
# Audit correction: guidance uses cash expensed R&D (H126 EUR1669m), not GAAP R&D including amortization.
# Add EUR1bn annual investment in every scenario, including sustainable replacement beyond2030.
for cfg in CONFIG.values():
    cfg['cap']=[v+1000 for v in cfg['cap']]
def interp(a,b,c,i):return a+(b-a)*i/4 if i<=4 else b+(c-b)*(i-4)/5

def bank_model(cfg):
    rows=[];prev=8576
    for i,yr in enumerate(range(2026,2036)):
        capital=cfg['bankcap'][i];earn=cfg['bankni'][i];need=capital-prev;div=earn-need
        rows.append(dict(year=yr,earnings=earn*FX,required_equity=capital*FX,incremental_required_equity=need*FX,distribution=div*FX,stub_distribution=(((earn-206)-(capital-9340))*114/184*FX) if i==0 else None));prev=capital
    g=cfg['g'];ke=cfg['bankke']
    terminal_distribution=(rows[-1]['earnings']*(1+g)-rows[-1]['required_equity']*g)
    tv=terminal_distribution/(ke-g)
    def pv(at):
        v=0
        for r in rows:
            end=dt.date(r['year'],12,31);begin=dt.date(r['year']-1,12,31)
            if end>at:
                cf=r['stub_distribution'] if at==START and r['year']==2026 else r['distribution']*min(1,(end-at).days/(end-begin).days)
                v+=cf/(1+ke)**model.years_between(at,end)
        return v+tv/(1+ke)**model.years_between(at,dt.date(2035,12,31))
    return dict(method='Equity DDM: distribution=NI-increase in required equity; terminal distribution=NI_2035*(1+g)-equity_2035*g; no captive gross debt/cash enters industrial EV',cost_of_equity=ke,terminal_growth=g,terminal_value=tv,present_value=pv(START),horizon_value=pv(HORIZON),rows=rows)

stla=dict(ticker='STLA',company='Stellantis N.V.',currency='USD',valuation_date=START.isoformat(),price=5.41,price_timestamp='2026-09-08T15:34:18.471217Z',shares_m=2919.844252,basic_shares_m=2900.941252,balance_date='2026-06-30',cash_m=31217*FX,minimum_cash_m=12000*FX,debt_m=23656*FX,senior_claims_m=(4997+4243+458)*FX,other_assets_m=0,debt_interest_rate=.043,status='Conditional turnaround candidate; fails extreme-bargain hurdle after full reinvestment',accounting_notes='NYSE ordinary common share, 1:1 with Euronext ordinary share, no ADR multiplier. Current basic plus Q2 incremental dilutive 18.903m awards. IFRS EBIT retains SBC, no addback/future award accretion. Industrial debt includes 2567m EUR leases; forecast capex includes estimated 850m EUR/year new lease/replacement obligations, growing with scale. Pension/OPEB recognized liabilities 4243m EUR deducted; 2025 plan assets of 967m EUR are not separately credited as unavailable to common holders. NCI 458m EUR deducted at book, an approximation. Hybrid principal 4997m EUR deducted once; annual 343.5025m EUR coupon reduces shareholder cash, not FCFF; coupons assumed unchanged; future reset risk remains unresolved. Captive cash 2480m and debt 28406m third-party carrying debt excluded from industrial bridge, captive equity valued by separate DDM. Remaining reset-charge cash is delta NWC, not a duplicate EBIT charge. Price/financial figures translated at frozen EURUSD 1.16276, prior-day close Sept 7; constant FX is assumption.',scenarios={},sources=[],history=[])
extras={'valuation_date':str(START),'eurusd':FX,'fx_timestamp':'2026-09-07T23:59:59.999Z','fx_note':'Massive C:EURUSD previous daily bar close; source milliseconds 1788825599999; not synchronous intraday FX','STLA':{'balance_bridge_eur_m':{'industrial_cash':31217,'minimum_cash_assumption':12000,'third_party_industrial_debt_including_leases':23656,'leases_included_in_debt':2567,'hybrid_principal':4997,'pension_opeb_recognized_liabilities':4243,'minority_book_claim':458,'other_liquid_and_financial_claims':2474,'other_claim_components':{'intercompany_net_receivable':796,'JV_financial_current_receivables':993,'derivatives':77,'securities':604,'held_for_sale_cash':4}},'captive':{},'operating_assumptions_eur':CONFIG}}
for name,cfg in CONFIG.items():
    bank=bank_model(cfg);extras['STLA']['captive'][name]=bank
    rows=[];prevrev=0
    for i,yr in enumerate(range(2026,2036)):
        seg=[]
        for j,n in enumerate(NAMES):
            v=interp(cfg['vol0'][j],cfg['vol30'][j],cfg['vol35'][j],i)
            price=cfg['price0'][j]*(1+cfg['pg'][j])**i
            margin=interp(cfg['m0'][j],cfg['m30'][j],cfg['m35'][j],i)
            seg.append(dict(name=n,revenue=v*price*FX,ebit_margin=margin,volume=v,volume_unit='thousand wholesale vehicles',price=price*FX,price_unit='thousand USD industrial revenue per shipped vehicle, includes parts/mix'))
        # Difference between group regional sales and industrial supplemental sales is small; separately zero-profit other industry.
        seg.append(dict(name='Other industrial and eliminations',revenue=400*(1+cfg['g'])**i*FX,ebit_margin=0,volume=None,price=None))
        rev=sum(s['revenue'] for s in seg)/FX
        nwc=(500 if name=='downside' and i<3 else 300 if i==0 else max(0,rev-prevrev)*.075)+(2000 if i==0 else cfg['legacy'][i])
        dps=0 if i<2 or name=='downside' else (.20 if name=='base' else .35)*(1.06**max(0,i-2))*FX
        rows.append(dict(year=yr,period_end=f'{yr}-12-31',segments=seg,corporate_cost=cfg['corp'][i]*FX,tax_rate=.27 if name!='downside' else .29,da=cfg['da'][i]*FX,capex=cfg['cap'][i]*FX,delta_nwc=nwc*FX,shares_m=stla['shares_m'],dividend_per_share=dps,stub_dividend_per_share=0 if i==0 else dps,net_debt_issuance=0,new_equity_issuance=0,preferred_dividend_m=343.5025*FX,nonoperating_distributions_m=bank['rows'][i]['distribution'],notes='Analyst forecast. Regional margins before corporate/restructuring reserve; all expensed R&D and SBC retained. Capex includes cash PP&E/capitalized R&D plus new lease investment. Delta NWC separately includes remaining 2025 reset cash; FY2026 full-year legacy cash EUR2bn; separate first-stub adjustment ensures September-December deducts entire EUR1.1bn remaining at June, conservatively ignoring possible July-August payments. Other reserve covers recurring restructuring; no future scarcity margin.'))
        if i==0:
            rows[-1]['stub_fcff_adjustment_m']=-(1100-2000*STUB)*FX
            rows[-1]['stub_nonoperating_distributions_m']=bank['rows'][i]['stub_distribution']
        prevrev=rev
    other=2474*FX
    sc=dict(stub_adjustment_date=str(START),probability=cfg['p'],wacc=cfg['w'],terminal_growth=cfg['g'],terminal_roic=cfg['roic'],other_assets_m=bank['present_value']+other,horizon_other_assets_m=bank['horizon_value']+other,years=rows)
    stla['scenarios'][name]=sc
stla['other_assets_m']=stla['scenarios']['base']['other_assets_m']
# Historical statements explicitly retain their actual reporting perimeter, not passed off as industrial model history.
for yr,rev,ebit,cfo,cap,sbc in [(2023,189544,22376,17954,9125,189),(2024,156878,3687,1535,10837,45),(2025,153508,-26254,-4650,9142,73)]:
    stla['history'].append(dict(year=yr,revenue=rev*FX,ebit=ebit*FX,cfo=cfo*FX,capex=cap*FX,sbc=sbc*FX,da={2023:7549,2024:7226,2025:6981}[yr]*FX,source_ids=['DC4'],perimeter='Consolidated group; not directly comparable to industrial forecast. Converted at frozen EURUSD for arithmetic only; source values in EUR.',reported_currency='EUR',reported_revenue=rev,reported_ebit=ebit,reported_cfo=cfo,reported_capex=cap))
stla['industrial_history_eur_m']=[dict(year=2024,adjusted_operating_income=8160,da=7180,cfo=6744,capex_including_payable_changes=10761,industrial_fcf=-6045),dict(year=2025,adjusted_operating_income=-782,da=6893,cfo=5050,capex_including_payable_changes=9090,industrial_fcf=-4525),dict(year='H1 2026',revenue=79141,ebit=1136,adjusted_operating_income=1482,da=3142,cfo=2557,capex_including_payable_changes=3066,industrial_fcf=-921)]
# ASIX: single integrated production system. Product revenue split is supplied separately; no unsupported product profit allocation.
asix=dict(ticker='ASIX',company='AdvanSix Inc.',currency='USD',valuation_date=str(START),price=17.44,price_timestamp='2026-09-08T15:34:10.939903Z',shares_m=27.556902,basic_shares_m=27.001186,balance_date='2026-06-30',cash_m=7.217,minimum_cash_m=10,debt_m=277.139,senior_claims_m=0,other_assets_m=0,debt_interest_rate=.065,status='Modelled rejection: cheap-looking assets, insufficient normalized cash after replacement spend',accounting_notes='Current basic shares plus Q2 dilutive awards 0.555716m. Keep GAAP SBC inside EBIT; no addback/additional future dilution. Revolver debt 275m June plus 2.139m finance lease liability last disclosed Dec25, conservatively not reduced for H126 principal; small stale input. Operating lease liability 148.941m excluded because rent remains expense. Capital spending includes 1m/year finance lease renewal. Defined benefit plan overfunded at December2025; no pension surplus credited to common holders. 12.2m supplier finance retained in working capital. Capitalized-interest share remains inside capex conservatively. Base annual 2026 dividend .64 but only .16 assumed after Sept8 (Sept1 already paid).',history=[],sources=[],scenarios={})
for yr,rev,ebit,da,cfo,cap,sbc in [(2023,1533.599,69.550,73.010,117.550,107.377,8.313),(2024,1517.557,58.913,76.176,135.413,133.722,7.854),(2025,1522.233,60.190,79.740,122.863,116.445,6.821)]:asix['history'].append(dict(year=yr,revenue=rev,ebit=ebit,da=da,cfo=cfo,capex=cap,sbc=sbc,source_ids=['DC10']))
AC={'downside':(.30,.13,.005,.08,[1610,1460,1480,1500,1520,1540,1560,1580,1600,1620],[.018,.02,.025,.03,.035,.035,.035,.035,.035,.035],[86,90,92,94,96,98,100,102,104,106]),'base':(.50,.115,.02,.12,[1640,1620,1650,1690,1730,1760,1790,1820,1850,1880],[.025,.04,.05,.057,.06,.06,.06,.06,.06,.06],[86,92,95,97,99,101,103,105,107,109]),'upside':(.20,.105,.025,.15,[1680,1710,1770,1820,1880,1930,1980,2030,2080,2130],[.035,.055,.075,.09,.10,.10,.10,.10,.10,.10],[90,97,103,108,112,115,118,121,124,127])}
for name,(prob,w,g,roic,revs,ms,caps) in AC.items():
    yrs=[]
    for i,y in enumerate(range(2026,2036)):
        yrs.append(dict(year=y,period_end=f'{y}-12-31',segments=[dict(name='Integrated nylon, caprolactam, plant nutrients and intermediates',revenue=revs[i],ebit_margin=ms[i],volume=None,price=None,volume_unit='Physical annual product volumes unavailable; product indices in extra_inputs.json')],corporate_cost=0,tax_rate=.25,da=84*(1.022)**i,capex=caps[i],delta_nwc=10 if i==0 else .08*(revs[i]-revs[i-1]),shares_m=asix['shares_m'],dividend_per_share=0 if name=='downside' else .64,stub_dividend_per_share=0 if name=='downside' else .16,net_debt_issuance=40 if i==0 else 0,new_equity_issuance=0,notes='Analyst scenario; volume versus price cannot be independently verified from missing product tonnage. No allocation of group margin to individual product economics. Downside requires revolver refinancing; availability assumed, not committed.'))
    asix['scenarios'][name]=dict(probability=prob,wacc=w,terminal_growth=g,terminal_roic=roic,years=yrs)
extras['ASIX']={'forecast_limitation':'No quarterly annual tonnage/product realization series disclosed; not a confirmed investment. Revenue forecast anchored H126 825.468m, Q2 volume -15% price +18%; 2025 product mix shifts cannot be treated as physical demand.','reported_product_revenue_q2_2026_m':{'nylon':100.218,'caprolactam':62.644,'plant_nutrients':131.439,'chemical_intermediates':126.983},'industry_2025_company_estimates':{'world_nylon6_production_consumption_mt':7.7,'world_nylon6_utilization':.56,'world_caprolactam_utilization':.74},'refinancing':{'revolver_drawn_june_m':275,'commitments_maturing_2026_10_27':48,'commitments_maturing_2027_10_27':452,'maximum_leverage':3.75,'minimum_interest_coverage':3.0}}
for c in [stla,asix]:
    frozen=Path('outputs/market_quotes.json')
    if frozen.exists():
        q=json.loads(frozen.read_text())
        records=q.get('quotes',[{'ticker':k,**v} for k,v in q.items() if isinstance(v,dict)]) if isinstance(q,dict) else q
        if isinstance(records,dict): records=list(records.values())
        for x in records:
            if isinstance(x,dict) and x.get('ticker')==c['ticker']:
                c['price']=x.get('price',c['price']); c['price_timestamp']=x.get('price_timestamp',x.get('timestamp',c['price_timestamp']))
(P/'inputs.json').write_text(json.dumps([stla,asix],indent=2)+'\n')
(P/'extra_inputs.json').write_text(json.dumps(extras,indent=2)+'\n')
print('Wrote models')
for c in [stla,asix]:
    r=model.run_company(c)
    print(c['ticker'],r['probability_weighted_fair_value'],{k:round(v['fair_value_per_share'],2) for k,v in r['scenarios'].items()},r['reverse_margin'])
