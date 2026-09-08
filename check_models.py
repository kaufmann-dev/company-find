"""Financial conservation and evidence-coverage checks; standard library only."""
import copy
import datetime as dt
import importlib.util
import json
import math
from pathlib import Path
import model

ROOT=Path(__file__).resolve().parent


def main():
    inputs=[]
    screens=[]
    for p in (ROOT/"research").glob("*/inputs.json"):
        inputs.extend(json.loads(p.read_text()))
    for p in (ROOT/"research").glob("*/screened.json"):
        screens.extend(json.loads(p.read_text()))
    assert len({x["ticker"] for x in screens})>=30
    assert len({x["ticker"] for x in inputs})>=8
    assert len({x["ticker"] for x in inputs})==len(inputs)
    for s in screens:
        assert s.get("role") and s.get("decision")
        assert s.get("source_url") or s.get("source_id") or s.get("source_ids") or s.get("dated_role_source")
    # Pure cash business: finite forecast + continuation conserves perpetuity value.
    constant={"wacc":.10,"terminal_growth":0,"terminal_roic":.2,"years":[
        {"year":y,"segments":[{"revenue":1000,"ebit_margin":.10}],"tax_rate":0,"da":0,"capex":0,"delta_nwc":0}
        for y in range(2026,2036)]}
    value,_,_=model.operating_value(constant,dt.date(2025,12,31))
    assert abs(value-1000)<.25,(value,"perpetuity conservation")
    assert abs(model.xirr([(dt.date(2026,9,8),-100),(dt.date(2031,9,8),200)])-(2**.2-1))<.0001
    assert model.xirr([(dt.date(2026,9,8),-100),(dt.date(2031,9,8),0)])==-1
    count=0
    for c in inputs:
        assert c["sources"] and len(c["history"])>=3
        assert math.isclose(sum(s["probability"] for s in c["scenarios"].values()),1)
        for sc in c["scenarios"].values():
            assert len(sc["years"])>=10
            assert len({r["year"] for r in sc["years"]})==len(sc["years"])
            assert [r["year"] for r in sc["years"]]==sorted(r["year"] for r in sc["years"])
            count+=len(sc["years"])
        if c.get("valuation_method","fcff")!="fcff":continue
        base=c["scenarios"]["base"]
        for scenario in c['scenarios'].values():
            if 'terminal_value_override' not in scenario:
                final=model.forecast_years(scenario)[-1]
                next_cash=model.terminal(scenario)[1]
                assert math.isclose(next_cash,model.operating(final)['fcff']*(1+scenario['terminal_growth']),abs_tol=1e-6)
        v=model.equity_value(c,base)["fair_value_per_share"]
        # A split changes price/share and share count, not economic value or IRR.
        split=copy.deepcopy(c);split["shares_m"]*=3;split["basic_shares_m"]*=3;split["price"]/=3
        for sc in split["scenarios"].values():
            for r in sc["years"]:
                for k in ["dividend_per_share","stub_dividend_per_share"]:
                    if k in r:r[k]/=3
        assert abs(model.equity_value(split,split["scenarios"]["base"])["fair_value_per_share"]*3-v)<1e-7
        r1=model.shareholder_return(c,base)["annualized_return"]
        r2=model.shareholder_return(split,split["scenarios"]["base"])["annualized_return"]
        assert abs(r1-r2)<1e-9
        # Cash and equal debt issuance at valuation cannot manufacture equity.
        neutral=copy.deepcopy(c);neutral["cash_m"]+=100;neutral["debt_m"]+=100
        assert abs(model.equity_value(neutral,base)["fair_value_per_share"]-v)<1e-7
        # Increasing capex destroys exactly its after-discount cash contribution.
        costly=copy.deepcopy(base);costly["years"][2]["capex"]+=100
        assert model.equity_value(c,costly)["fair_value_per_share"]<v or v==0
    spec=importlib.util.spec_from_file_location("aer_model",ROOT/"research/aviation_health/model.py")
    aer=importlib.util.module_from_spec(spec);spec.loader.exec_module(aer)
    c=next(c for c in inputs if c["ticker"]=="AER")
    for sc in c["scenarios"].values():
        for row in sc["years"]:
            assert abs(aer.equity_cash(row)-row["fcfe"])<1e-5
    quotes=json.loads((ROOT/'outputs/market_quotes.json').read_text())
    for c in inputs:
        assert c['price']==quotes[c['ticker']]['price']
        assert c['price_timestamp']==quotes[c['ticker']]['price_timestamp']
    print(f"PASS: {len(screens)} investigated screens, {len(inputs)} companies, {count} annual scenario rows; cash, splits, IRR and lessor funding reconcile")


if __name__=="__main__":main()
