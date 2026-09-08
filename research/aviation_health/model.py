"""AerCap equity DCF, annual cash bridge, reverse valuation and five-year XIRR.

Run: python research/aviation_health/model.py
Inputs: USD millions and millions of diluted shares in inputs.json.
Debt is operating funding for an aircraft lessor. Equity cash flow is net income
less the equity capital required for portfolio growth, discounted at equity cost.
Debt/deposits and both replacement/growth capex are in the explicit cash bridge.
No book-value multiple or temporary sale margin is capitalized forever.
"""
import copy
import csv
import datetime as dt
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def years(a, b):
    return (b-a).days/365.25


def xirr(flows):
    def npv(r):
        return sum(v/(1+r)**years(flows[0][0], d) for d,v in flows)
    lo,hi=-.999,10
    for _ in range(160):
        m=(lo+hi)/2
        if npv(m)>0: lo=m
        else: hi=m
    return (lo+hi)/2


def equity_cash(row):
    # Sale gains included in NI are removed from disposal proceeds to avoid
    # counting a gain twice. Replacement of impaired assets consumes cash.
    cash = (row['net_income']+row['da']+row['impairment']-row['capex']
            +row['disposal_cash']-row['gain_on_sale']
            +row['net_debt_issuance']+row['net_deposit_and_other_funding'])
    required_equity=row['end_book_equity']-row['begin_book_equity']
    assert abs(cash-(row['net_income']-required_equity))<1e-6
    return cash


def terminal(sc):
    last=sc['years'][-1]
    g=sc['terminal_growth']
    # FY2035 is normalized; assets, debt and equity grow at terminal g.
    # This deducts the common equity needed to fund sustainable future growth.
    next_fcfe=last['net_income']*(1+g)-last['end_book_equity']*g
    return max(0,next_fcfe/(sc['cost_of_equity']-g))


def value(sc, at):
    pv=0
    for row in sc['years']:
        end=dt.date(row['year'],12,31)
        start=dt.date(row['year']-1,12,31)
        if at>=end: continue
        f=min(1,(end-at).days/(end-start).days)
        pv+=equity_cash(row)*f/(1+sc['cost_of_equity'])**years(at,end)
    tvpv=terminal(sc)/(1+sc['cost_of_equity'])**years(at,dt.date(2035,12,31))
    return pv+tvpv,tvpv


def returns(c, sc):
    start=dt.date.fromisoformat(c['valuation_date'])
    end=start.replace(year=start.year+5)
    flows=[(start,-c['price'])]
    retained=0
    for row in sc['years']:
        pe=dt.date(row['year'],12,31)
        ps=dt.date(row['year']-1,12,31)
        overlap=max(0,(min(pe,end)-max(ps,start)).days)
        if not overlap: continue
        retained+=equity_cash(row)*overlap/(pe-ps).days
        if pe<=end:
            dividend=.4 if row['year']==2026 else row['dividend_per_share']
            retained-=dividend*c['shares_m']
            flows.append((pe,dividend))
    remaining,_=value(sc,end)
    future=(remaining+retained)/c['shares_m']
    flows.append((end,future))
    return dict(annualized_return=xirr(flows),future_equity_per_share=future,
                retained_excess_cash_m=retained,
                cashflows=[dict(date=d.isoformat(),per_share=v) for d,v in flows])


def shift_rental_yield(sc, delta):
    out=copy.deepcopy(sc)
    for row in out['years']:
        change=row['avg_lease_assets']*delta
        row['basic_lease']+=change
        row['revenue']+=change
        row['ebit']+=change
        row['net_income']+=change*(1-row['tax_rate'])
        row['fcfe']+=change*(1-row['tax_rate'])
    return out


def run(c):
    at=dt.date.fromisoformat(c['valuation_date'])
    result=dict(ticker=c['ticker'],price=c['price'],price_timestamp=c['price_timestamp'],
                currency='USD',current_equity_m=c['price']*c['basic_shares_m'],
                diluted_equity_m=c['price']*c['shares_m'],
                current_ev_m=c['price']*c['basic_shares_m']+c['debt_m']-c['cash_m'],
                ev_note='Descriptive equity plus debt less unrestrictedcash; maintenance/customer deposits included in equityDCF capital, no industrialEVcomparison',scenarios={})
    for name,sc in c['scenarios'].items():
        v,tv=value(sc,at)
        result['scenarios'][name]=dict(probability=sc['probability'],equity_value_m=v,
            fair_value_per_share=v/c['shares_m'],terminal_pv_m=tv,terminal_share_of_equity_value=tv/v,
            **returns(c,sc))
    weighted=sum(r['probability']*r['fair_value_per_share'] for r in result['scenarios'].values())
    result.update(probability_weighted_fair_value=weighted,upside=weighted/c['price']-1,
        margin_of_safety=1-c['price']/weighted,
        expected_scenario_annualized_return=sum(r['probability']*r['annualized_return'] for r in result['scenarios'].values()))
    ef={}
    for r in result['scenarios'].values():
        for event in r['cashflows']:
            ef[event['date']]=ef.get(event['date'],0)+r['probability']*event['per_share']
    result['expected_cashflow_annualized_return']=xirr([(dt.date.fromisoformat(d),v) for d,v in sorted(ef.items())])
    base=c['scenarios']['base']
    lo,hi=-.05,.05
    for _ in range(100):
        mid=(lo+hi)/2
        v,_=value(shift_rental_yield(base,mid),at)
        if v/c['shares_m']<c['price']: lo=mid
        else: hi=mid
    shift=(lo+hi)/2
    result['reverse_lease_yield']=dict(parallel_basis_point_change=shift*10000,
        normalized_2035_lease_yield=base['years'][-1]['lease_rent_yield']+shift,
        note='All rentalyields shift; capital,creditcosts,salesgains,fundingandterminalgrowthheldfixed. Onejustifyingpath,notuniqueimpliedconsensus.')
    result['sensitivity']=[]
    for ke in [.095,.105,.115]:
        for dy in [-.005,0,.005]:
            sc=shift_rental_yield(base,dy);sc['cost_of_equity']=ke
            v,_=value(sc,at)
            result['sensitivity'].append(dict(cost_of_equity=ke,rental_yield_change_bp=dy*10000,fair_value=v/c['shares_m']))
    d=result['scenarios']['downside']['fair_value_per_share'];u=result['scenarios']['upside']['fair_value_per_share']
    result['probability_sensitivity_shift_10pp_upside_to_downside']=weighted+.1*(d-u)
    # A combined test uses the full downside path, not isolated shocks.
    return result


def main():
    companies=json.loads((HERE/'inputs.json').read_text())
    c=next(c for c in companies if c['ticker']=='AER')
    result=run(c)
    (HERE/'aer_valuation.json').write_text(json.dumps(result,indent=2)+'\n')
    rows=[]
    for name,sc in c['scenarios'].items():
        for r in sc['years']:
            keep={k:v for k,v in r.items() if isinstance(v,(float,int,str)) and k!='notes'}
            rows.append(dict(scenario=name,**keep,fcfe_cash_bridge=equity_cash(r),cost_of_equity=sc['cost_of_equity']))
    with (HERE/'aer_annual.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_demand_supply()
    print(json.dumps(result,indent=2))


def write_demand_supply():
    """Illustrative annual operational scenarios; all future inputs assumptions.

    Aviation starts from IATA's May2026 active fleet, not a false Jan1 stock.
    2026 therefore applies seven months of fleet additions and traffic growth.
    Feasible deliveries already incorporate ramp/qualification: no second haircut.
    CRO annual trial cohorts are not installed assets or annual trial starts added
    directly to revenue. Cohort weights represent annual active service-years.
    """
    paths={
        'persistent_scarcity':dict(traffic=[.03]+[.055]*4+[.045]*5,
            nameplate=[1900,2200,2400,2550,2650,2700,2700,2700,2700,2700],
            usable=[1650,1850,2050,2200,2300,2375,2400,2400,2400,2400],
            retire=[700,800,900,1000,1100,1200,1250,1300,1350,1400],
            return_from_storage=[50,50,25,25,0,0,0,0,0,0]),
        'orderly_normalization':dict(traffic=[.021]+[.04]*9,
            nameplate=[1950,2450,2700,2850,2850,2850,2850,2800,2750,2750],
            usable=[1794,2200,2450,2600,2650,2650,2650,2600,2550,2550],
            retire=[650,700,800,900,1000,1100,1150,1200,1250,1300],
            return_from_storage=[100,100,75,50,25,0,0,0,0,0]),
        'oversupply_or_demand_disappointment':dict(traffic=[.01,0,.02,.025,.025,.03,.03,.03,.03,.03],
            nameplate=[2000,2600,2900,3050,3050,2950,2850,2800,2750,2750],
            usable=[1850,2350,2650,2850,2850,2750,2650,2600,2550,2550],
            retire=[800,1000,1300,1500,1600,1600,1550,1550,1550,1550],
            return_from_storage=[175,175,100,50,0,0,0,0,0,0])}
    aviation=[]
    for name,p in paths.items():
        active=30407.0;required=33577.0
        for i,y in enumerate(range(2026,2036)):
            f=7/12 if y==2026 else 1
            before=required
            # 1% seats-per-aircraft productivity; no repeated load-factor credit.
            required*=((1+p['traffic'][i])/1.01)**f
            retire=p['retire'][i]*f
            delivered=p['usable'][i]*f
            reactivated=p['return_from_storage'][i]*f
            active+=delivered+reactivated-retire
            aviation.append(dict(scenario=name,year=y,period_start='2026-05-31' if y==2026 else f'{y}-01-01',
                period_fraction=f,traffic_growth=p['traffic'][i],seats_per_aircraft_growth=.01,
                required_normal_fleet=required,usable_active_fleet=active,
                annual_delivery_nameplate=p['nameplate'][i],annual_usable_deliveries=p['usable'][i],
                realization_fraction=p['usable'][i]/p['nameplate'][i],period_deliveries=delivered,
                retirements=retire,storage_reactivations=reactivated,
                annual_new_aircraft_demand_for_growth_and_replacement=(required-before+retire-reactivated)/f,
                effective_aircraft_gap=required-active,
                spare_equivalent_aircraft=max(0,active-required),
                active_fleet_per_normal_need=active/required))
    with (HERE/'aviation_demand_supply.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(aviation[0]));w.writeheader();w.writerows(aviation)
    cro=[]
    # 2023/2024 starts source: IQVIA March2025 report Exhibit11.
    # 2025 5200 is an analyst calibration consistent with directional2026summary,
    # not a disclosed industry total. Outsource shares/unit fees are assumptions.
    for name,startgrowth,complexity,efficiency,sharegain,supplygrowth in [
        ('persistent_scarcity',.045,.025,.01,.008,.035),
        ('orderly_normalization',.03,.02,.01,.005,.03),
        ('oversupply_or_demand_disappointment',.005,.01,.025,0,.025)]:
        starts={2023:5302,2024:5318,2025:5200};supply=8000
        for i,y in enumerate(range(2026,2036)):
            starts[y]=starts[y-1]*(1+startgrowth)
            active=.5*starts[y]+starts[y-1]+.75*starts[y-2]+.25*starts[y-3]
            outsourcing=.58+min(i,8)*sharegain
            intensity=((1+complexity)/(1+efficiency))**i
            demand=active*outsourcing*intensity
            supply*=1+supplygrowth
            fee=5*(1.02**i)
            cro.append(dict(scenario=name,year=y,annual_trial_starts=starts[y],annual_active_trial_service_years=active,
                outsourcing_share=outsourcing,net_work_per_trial_index=intensity,
                outsourced_standard_trial_service_year_demand=demand,
                usable_standard_trial_service_year_supply=supply,
                implied_utilization=demand/supply,fee_m_usd_per_standard_service_year=fee,
                annual_scenario_service_budget_m_usd=demand*fee,
                supply_status='assumed scenario envelope; aggregate qualified capacity not publicly measured'))
    with (HERE/'clinical_demand_supply.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(cro[0]));w.writeheader();w.writerows(cro)


if __name__=='__main__': main()
