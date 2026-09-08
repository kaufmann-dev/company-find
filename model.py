"""Reproduce the research DCF, reverse valuations and dated five-year returns.

Run: python model.py. Python standard library only. Monetary amounts/shares: millions.
Each annual input is a full fiscal year. The first cash flow is prorated by days
remaining in its fiscal year; cash is assumed earned uniformly, paid at year end.
This is a disclosed approximation, not knowledge of quarterly seasonality.
"""
import copy
import csv
import datetime as dt
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def date(value):
    return dt.date.fromisoformat(value)


def years_between(a, b):
    return (b-a).days / 365.25


def period(row):
    end = date(row.get("period_end", f'{row["year"]}-12-31'))
    return end.replace(year=end.year-1), end


def operating(row):
    revenue = sum(s["revenue"] for s in row["segments"])
    ebit = sum(s["revenue"]*s["ebit_margin"] for s in row["segments"])-row.get("corporate_cost", 0)
    nopat = ebit*(1-row["tax_rate"])
    fcff = nopat+row["da"]-row["capex"]-row["delta_nwc"]
    return dict(revenue=revenue, ebit=ebit, ebit_margin=ebit/revenue,
                nopat=nopat, fcff=fcff)


def forecast_years(scenario):
    """Add five explicit years for convergence of investment to sustainable rates.

    Normalized nominal sales, costs and DA grow at g, with constant margins.
    Incremental capex transitions toward the greater of existing net investment
    and g/ROIC of NOPAT. Existing replacement spending is never released merely
    because the terminal formula assumes accounting DA equals maintenance capex.
    A finite fleet liquidation has no perpetuity and gets no transition.
    """
    rows=copy.deepcopy(scenario["years"])
    if "terminal_value_override" in scenario:
        return rows
    anchor=rows[-1]
    g=scenario["terminal_growth"]
    existing=anchor["capex"]-anchor["da"]+anchor["delta_nwc"]
    required=max(existing,operating(anchor)["nopat"]*g/scenario["terminal_roic"])
    for i in range(1,6):
        row=copy.deepcopy(anchor)
        growth=(1+g)**i
        row["year"]=anchor["year"]+i
        if "period_end" in row:
            end=date(anchor["period_end"])
            row["period_end"]=end.replace(year=end.year+i).isoformat()
        if 'dividend_date' in row:
            pay=date(anchor['dividend_date'])
            row['dividend_date']=pay.replace(year=pay.year+i).isoformat()
        for segment in row["segments"]:
            segment["revenue"]*=growth
            # Nominal normalization contains both inflation and physical growth;
            # do not pretend its components are independently observed volumes.
            segment.update(volume=None,price=None,volume_unit="normalized nominal growth; physical split unspecified")
        for key in ["corporate_cost","da","capex","delta_nwc","dividend_per_share"]:
            if key in row: row[key]*=growth
        row["capex"]+=(required-existing)*growth*i/5
        row["notes"]="Explicit analyst normalization: nominal growth at g, constant margins, five-year reinvestment convergence; replacement investment floor retained."
        row["normalization_transition"]=True
        rows.append(row)
    return rows


def terminal(scenario):
    final_row = forecast_years(scenario)[-1]
    last = operating(final_row)
    g = scenario["terminal_growth"]
    wacc = scenario["wacc"]
    assert wacc > g and scenario["terminal_roic"] > g
    # Sustainable new investment is g/ROIC of NOPAT, not zero capex forever.
    reinvestment=max(last["nopat"]*g/scenario["terminal_roic"],
                     final_row["capex"]-final_row["da"]+final_row["delta_nwc"])
    next_fcff = (last["nopat"]-reinvestment)*(1+g)
    return scenario.get("terminal_value_override", next_fcff/(wacc-g)), next_fcff


def operating_value(scenario, valuation_date):
    value = 0.0
    rows=forecast_years(scenario)
    for row in rows:
        start, end = period(row)
        if end <= valuation_date:
            continue
        fraction = min(1.0, (end-valuation_date).days/(end-start).days)
        cashflow=operating(row)["fcff"]*fraction
        if start < valuation_date and valuation_date.isoformat()==scenario.get('stub_adjustment_date', '2026-09-08'):
            cashflow+=row.get('stub_fcff_adjustment_m',0)
        value += cashflow/(1+scenario["wacc"])**years_between(valuation_date,end)
    tv, next_fcff = terminal(scenario)
    terminal_date = period(rows[-1])[1]
    terminal_pv = tv/(1+scenario["wacc"])**years_between(valuation_date,terminal_date)
    return value+terminal_pv, terminal_pv, next_fcff


def excess_cash(company):
    return company["cash_m"]-company.get("minimum_cash_m", 0)


def equity_value(company, scenario):
    ev,tvpv,next_fcff = operating_value(scenario,date(company["valuation_date"]))
    other_assets=scenario.get('other_assets_m',company.get('other_assets_m',0))
    equity = ev+excess_cash(company)+other_assets-company["debt_m"]-company.get("senior_claims_m",0)
    return {"enterprise_value_m":ev,"equity_value_m":max(0,equity),"residual_after_senior_claims_m":equity,
            "nonoperating_assets_value_m":other_assets,
            "fair_value_per_share":max(0,equity/company["shares_m"]),
            "terminal_pv_m":tvpv,"terminal_share_of_ev":tvpv/ev,
            "terminal_next_fcff_m":next_fcff}


def xirr(cashflows):
    origin=cashflows[0][0]
    if not any(v>0 for _,v in cashflows[1:]):
        return -1.0
    def npv(rate):
        return sum(v/(1+rate)**years_between(origin,d) for d,v in cashflows)
    lo,hi=-0.999,10.0
    if npv(lo)*npv(hi)>0:
        return None
    for _ in range(160):
        mid=(lo+hi)/2
        if npv(mid)>0: lo=mid
        else: hi=mid
    return (lo+hi)/2


def shareholder_return(company,scenario):
    """Forecast dividends plus retained FCFE and remaining operating EV at year 5.

    Repurchases are not added as dividends. Residual cash is retained at zero
    interest; no buyback accretion. SBC stays in operating expense, approximating
    cash remuneration/repurchase to offset future awards; existing awards enter
    the initial diluted share count. Capital structure is held unless an annual
    financing input explicitly changes it. This capital allocation convention is
    an assumption, not management's announced dividend/buyback policy.
    """
    start=date(company["valuation_date"])
    horizon=start.replace(year=start.year+5)
    cash=excess_cash(company)
    debt=company["debt_m"]
    shares=company["shares_m"]
    flows=[(start,-company["price"])]
    funding_shortfall=0.0
    for row in scenario["years"]:
        ps,pe=period(row)
        overlap=max(0,(min(pe,horizon)-max(ps,start)).days)
        if not overlap: continue
        fraction=overlap/(pe-ps).days
        interest=debt*company.get("debt_interest_rate",.05)*(1-row["tax_rate"])
        cash+=(operating(row)["fcff"]-interest-row.get("preferred_dividend_m",0)
               +row.get('nonoperating_distributions_m',0))*fraction
        if ps < start < pe:
            cash+=row.get('stub_fcff_adjustment_m',0)
            if 'stub_nonoperating_distributions_m' in row:
                cash+=row['stub_nonoperating_distributions_m']-row.get('nonoperating_distributions_m',0)*fraction
        pay_date=date(row.get('dividend_date',pe.isoformat()))
        if start < pay_date <= horizon:
            paid_fraction=min(1,(pe-start).days/(pe-ps).days)
            div=(row.get('dividend_per_share',0) if 'dividend_date' in row else
                 row.get("stub_dividend_per_share",row.get("dividend_per_share",0)*paid_fraction) if ps<start else row.get("dividend_per_share",0))
            cash-=div*shares
            if div: flows.append((pay_date,div))
        if start < pe <= horizon:
            paid_fraction=min(1,(pe-start).days/(pe-ps).days)
            issued_debt=row.get("net_debt_issuance",0)*paid_fraction
            debt+=issued_debt
            cash+=issued_debt
            issued_equity=row.get("new_equity_issuance",0)*paid_fraction
            if issued_equity:
                issue_price=row["new_equity_issue_price"]
                shares+=issued_equity/issue_price
                cash+=issued_equity
        funding_shortfall=max(funding_shortfall,-cash)
    horizon_ev,_,_=operating_value(scenario,horizon)
    other_assets=scenario.get('horizon_other_assets_m',company.get('other_assets_m',0))
    future_equity=max(0,horizon_ev+cash+other_assets-debt-company.get("senior_claims_m",0))
    future_price=future_equity/shares
    flows.append((horizon,future_price))
    return {"annualized_return":xirr(flows),"future_equity_per_share":future_price,
            "future_operating_ev_m":horizon_ev,"retained_excess_cash_m":cash,
            "future_nonoperating_assets_m":other_assets,
            "horizon_debt_m":debt,"unfunded_cash_shortfall_m":funding_shortfall,
            "cashflows":[{"date":d.isoformat(),"per_share":v} for d,v in flows]}


def reverse_margin(company):
    """Parallel percentage-point shift in all segment EBIT margins, all years.

    Keeps base volumes, price, explicit 2026-35 capex, DA, working capital,
    WACC and g unchanged. Later sustainable investment responds to NOPAT.
    It is one price-justifying combination, not inferred market consensus.
    """
    def valued(shift):
        sc=copy.deepcopy(company["scenarios"]["base"])
        for row in sc["years"]:
            for segment in row["segments"]:
                segment["ebit_margin"]+=shift
        return equity_value(company,sc)["fair_value_per_share"]
    lo,hi=-.5,.5
    if not valued(lo)<=company["price"]<=valued(hi): return None
    for _ in range(100):
        mid=(lo+hi)/2
        if valued(mid)<company["price"]: lo=mid
        else: hi=mid
    shift=(lo+hi)/2
    return {"parallel_margin_change_percentage_points":shift*100,
            "price_justifying_2030_margin":operating(next(r for r in company["scenarios"]["base"]["years"] if r["year"]==2030))["ebit_margin"]+shift,
            "fair_value_at_solution":valued(shift)}


def run_company(company):
    assert math.isclose(sum(s["probability"] for s in company["scenarios"].values()),1)
    result={"ticker":company["ticker"],"company":company["company"],"currency":company["currency"],
            "price":company["price"],"price_timestamp":company["price_timestamp"],
            "current_equity_m":company["price"]*company.get("basic_shares_m",company["shares_m"]),
            "diluted_equity_m":company["price"]*company["shares_m"],"scenarios":{}}
    result["current_ev_m"]=result["current_equity_m"]+company["debt_m"]+company.get("senior_claims_m",0)-excess_cash(company)-company.get("other_assets_m",0)
    result["conventional_ev_m"]=result["current_equity_m"]+company["debt_m"]+company.get("senior_claims_m",0)-company["cash_m"]-company.get("other_assets_m",0)
    for name,sc in company["scenarios"].items():
        assert len(sc["years"])>=10
        assert len({r["year"] for r in sc["years"]})==len(sc["years"])
        for row in sc["years"]:
            assert 0<=row["tax_rate"]<1 and row["capex"]>=0
        result["scenarios"][name]={"probability":sc["probability"],**equity_value(company,sc),**shareholder_return(company,sc)}
    weighted=sum(r["probability"]*r["fair_value_per_share"] for r in result["scenarios"].values())
    result.update(probability_weighted_fair_value=weighted,upside=weighted/company["price"]-1,
                  margin_of_safety=1-company["price"]/weighted,
                  expected_scenario_annualized_return=sum(r["probability"]*r["annualized_return"] for r in result["scenarios"].values()))
    expected_flows={}
    for scenario in result["scenarios"].values():
        for event in scenario["cashflows"]:
            expected_flows[event["date"]]=expected_flows.get(event["date"],0)+scenario["probability"]*event["per_share"]
    result["expected_cashflow_annualized_return"]=xirr([(date(d),v) for d,v in sorted(expected_flows.items())])
    result["reverse_margin"]=reverse_margin(company)
    result["sensitivity"]=[]
    for w_shift in [-.01,0,.01]:
        for g_shift in [-.01,0,.01]:
            sc=copy.deepcopy(company["scenarios"]["base"])
            sc["wacc"]+=w_shift
            sc["terminal_growth"]+=g_shift
            result["sensitivity"].append({"wacc":sc["wacc"],"g":sc["terminal_growth"],
                                          "fair_value":equity_value(company,sc)["fair_value_per_share"]})
    downside=result["scenarios"]["downside"]["fair_value_per_share"]
    upside=result["scenarios"]["upside"]["fair_value_per_share"]
    result["probability_sensitivity_shift_10pp_upside_to_downside"]=weighted+.1*(downside-upside)
    return result


def main():
    companies=[]
    for path in sorted((ROOT/"research").glob("*/inputs.json")):
        data=json.loads(path.read_text())
        if isinstance(data,dict): data=data.get("companies",[data])
        companies.extend(c for c in data if c.get("valuation_method","fcff")=="fcff")
    assert len({c["ticker"] for c in companies})==len(companies)
    results=[run_company(c) for c in companies]
    out=ROOT/"outputs"
    out.mkdir(exist_ok=True)
    (out/"valuations.json").write_text(json.dumps(results,indent=2)+"\n")
    annual=[]
    segments=[]
    for c in companies:
        for name,sc in c["scenarios"].items():
            for row in forecast_years(sc):
                annual.append({"ticker":c["ticker"],"scenario":name,"year":row["year"],**operating(row),
                    **{k:row.get(k,0) for k in ["tax_rate","da","capex","delta_nwc","corporate_cost","dividend_per_share","net_debt_issuance","new_equity_issuance","nonoperating_distributions_m","stub_fcff_adjustment_m","stub_nonoperating_distributions_m"]},
                    "shares_m":row.get("shares_m",c["shares_m"]),"wacc":sc["wacc"],"terminal_growth":sc["terminal_growth"],"terminal_roic":sc["terminal_roic"]})
                annual[-1]['dividend_date']=row.get('dividend_date','fiscal year end')
                for seg in row["segments"]:
                    segments.append({"ticker":c["ticker"],"scenario":name,"year":row["year"],
                        **{k:seg.get(k,"") for k in ["name","revenue","ebit_margin","volume","volume_unit","price"]}})
    for filename,rows in [("annual_forecasts.csv",annual),("segment_forecasts.csv",segments)]:
        if rows:
            with (out/filename).open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for r in results:
        print(r["ticker"],"price",round(r["price"],2),"fair",round(r["probability_weighted_fair_value"],2),
              "scenarios",[round(s["fair_value_per_share"],2) for s in r["scenarios"].values()],
              "expected cash-flow IRR",round(r["expected_cashflow_annualized_return"]*100,1))


if __name__=="__main__":
    main()
