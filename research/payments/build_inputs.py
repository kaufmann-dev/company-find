"""Analyst assumptions; source-backed anchors are embedded in inputs.json."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
sources=[
 {"id":"PAY1","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000082/pypl-20260630.htm","publication_date":"2026-07-28","section":"cover; notes 2,3,8,9; MD&A pp48-54","supports":"current shares, revenue categories, operating drivers, lending and customer balances, competition"},
 {"id":"PAY2","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm","publication_date":"2026-02-03","section":"consolidated income/cash flows pp59-63; note 15 stock compensation","supports":"2023-2025 financial history; capitalized SBC"},
 {"id":"PAY3","url":"https://www.sec.gov/Archives/edgar/data/1633917/000163391726000080/pypl2q-26earningsrelease.htm","publication_date":"2026-07-28","section":"financial and operating results; cash flow; dividend program; balance sheet","supports":"interim results, guidance and September dividend record date"},
 {"id":"PAY4","url":"https://www.sec.gov/Archives/edgar/data/798354/000079835426000031/fisv-20260630.htm","publication_date":"2026-08-06","section":"cover; notes 1,3,8,10,11,12,16,18; MD&A","supports":"FISV shares, cash restrictions, debt, segment history, service cost deterioration"},
 {"id":"PAY5","url":"https://investors.fiserv.com/static-files/9e20ef73-0abc-4550-a6b3-95c26b30719f","publication_date":"2026-02-19","section":"10-K printed pp1-5,35-42,47,51,63","supports":"2023-2025 history; bank and merchant revenue mechanisms; contracts and financing"},
 {"id":"PAY6","url":"https://investors.fiserv.com/news-releases/news-release-details/fiserv-reports-second-quarter-2026-results","publication_date":"2026-08-06","section":"guidance; segment results; statements of cash flow and balance sheets","supports":"2026 interim and management outlook"},
 {"id":"PAY7","url":"https://www.census.gov/retail/ecommerce.html","publication_date":"2026-08-18","section":"second quarter 2026 retail e-commerce sales","supports":"customer spending and affordability cross-check; US e-commerce $340.2bn Q2 adjusted, 12.2% YoY"},
 {"id":"PAY8","url":"https://www.adyen.com/press-and-media/adyen-publishes-h1-2026-financial-results-3wjne","publication_date":"2026-08-13","section":"H1 key metrics and financial objectives","supports":"independent competitor volume24% and revenue19% growth; capex7% of net revenue guidance"},
 {"id":"PAY9","url":"https://www.sec.gov/Archives/edgar/data/1403161/000140316126000103/q32026earningsrelease.htm","publication_date":"2026-07-28","section":"volume and transaction operating metrics","supports":"network demand payments volume+10%; 71.7bn quarterly processed transactions"},
 {"id":"PAY10","url":"https://investors.fiserv.com/static-files/af17ec6f-4ca7-4261-804c-2fb24b9d2430","publication_date":"2026-05-15","section":"investor day transcript pp5-9","supports":"2025 merchant GPV4.6tr; SMB customer definitions; processing throughput test and medium-term management goals"},
 {"id":"PAY11","url":"https://www.frbservices.org/news/fed360/issues/060226/cash-2026-diary-of-consumer-payment-choice","publication_date":"2026-06-02","section":"survey summary and historical figure","supports":"2025 survey average47payments/month, instrument shares stable; publication year is not observation year"}
]
companies=[]
pypl={"ticker":"PYPL","company":"PayPal Holdings","currency":"USD","valuation_date":"2026-09-08",
 "price":53.445,"price_timestamp":"2026-09-08T14:35:00Z","quote_field":"Massive min.c; minute start min.t; delayed snapshot, not executable real-time quote",
 "shares_m":860.460874,"basic_shares_m":855.460874,"shares_date":"2026-07-22","balance_date":"2026-06-30",
 "cash_m":11256,"minimum_cash_m":5000,"debt_m":13400,"senior_claims_m":119.76452236,"other_assets_m":0,
 "debt_interest_rate":.046,"status":"modelled candidate pending comparative ranking",
 "accounting_notes":"Cash=8306+2950 short-term investments. Reserve3000 operating liquidity plus2000 matching customer-funds deficit; not customer cash. Exclude all4009 long-term investments conservatively, including strategic interests. Reserve119.765 for September dividend whose record date preceded purchase; paid to prior holders. July22 basic+Q2 5m incremental awards. GAAP operating margin includes SBC; do not add back. Capex includes assumed capitalized SBC cash equivalent. No future buybacks or extra dilution counted; financing remains flat. Loans remain operating assets; their incremental funding is NWC, never cash added to equity. Operating leases remain operating costs. Balance not rolled forward using invented cash flows; undisclosed July-Sep movements are sensitivity, not facts.",
 "history":[{"year":y,"revenue":r,"ebit":e,"da":d,"capex":k,"cfo":c,"sbc_cashflow_addback":s,"source_ids":["PAY2"]} for y,r,e,d,k,c,s in [(2023,29771,5028,1072,623,4843,1475),(2024,31797,5325,1032,683,7450,1230),(2025,33172,6065,963,852,6416,1002)]],
 "interim":{"period":"H1 2026","revenue":17035,"ebit":2915,"da":484,"sbc":534,"active_accounts_m":439,"transactions_m":13225,"tpv_m":950403,"transaction_revenue":15333,"ovas_revenue":1702,"source_ids":["PAY1","PAY3"]},
 "sources":sources[:3],"scenarios":{}}
# Rates below are explicit analyst judgments, not consensus or company targets.
assumptions={
 "downside":{"probability":.30,"wacc":.115,"terminal_growth":0,"terminal_roic":.12,
  "account_growth":[0,-.02,-.02,-.02,-.01,-.01,0,0,0,0],"intensity_growth":[0,.01,.01,.01,.01,.01,.01,.01,.01,.01],"ticket_growth":.015,
  "fee_decay":.035,"margin":[.163,.135,.12,.11,.105,.10,.10,.10,.10,.10],"ovas_growth":-.01,"capex_rate":.034},
 "base":{"probability":.50,"wacc":.10,"terminal_growth":.025,"terminal_roic":.20,
  "account_growth":[0,.005,.01,.01,.01,.005,.005,.005,.005,.005],"intensity_growth":[0,.04,.04,.035,.03,.03,.025,.025,.02,.02],"ticket_growth":.02,
  "fee_decay":.017,"margin":[.163,.155,.16,.163,.165,.165,.165,.165,.165,.165],"ovas_growth":.02,"capex_rate":.034},
 "upside":{"probability":.20,"wacc":.095,"terminal_growth":.03,"terminal_roic":.23,
  "account_growth":[0,.015,.02,.02,.015,.01,.01,.01,.01,.01],"intensity_growth":[0,.06,.06,.05,.05,.04,.035,.03,.03,.025],"ticket_growth":.02,
  "fee_decay":.01,"margin":[.163,.17,.18,.19,.195,.195,.19,.19,.19,.19],"ovas_growth":.05,"capex_rate":.035}}
demand=[]
for name,a in assumptions.items():
    sc={k:a[k] for k in ["probability","wacc","terminal_growth","terminal_roic"]};sc["years"]=[]
    accounts=440;intensity=62;ticket=72.5;take=.0159;ovas=3400;prior_rev=33172;prior_ovas=3374
    for i,y in enumerate(range(2026,2036)):
        if i:
            accounts*=1+a["account_growth"][i];intensity*=1+a["intensity_growth"][i];ticket*=1+a["ticket_growth"];take*=1-a["fee_decay"];ovas*=1+a["ovas_growth"]
        transactions=accounts*intensity;tpv=transactions*ticket;fees=tpv*take;revenue=fees+ovas
        # Retained lending expands with OVAS; 2.6 approximates $8.76bn loans/$3.4bn OVAS.
        nwc=.02*(revenue-prior_rev)+2.6*(ovas-prior_ovas)
        if name=="downside": nwc=max(nwc,100) # losses/precautionary liquidity prevent assumed release
        row={"year":y,"period_end":f"{y}-12-31","segments":[
          {"name":"Transaction fees","revenue":round(fees,6),"ebit_margin":a["margin"][i],"volume":round(tpv,6),"volume_unit":"USD million total payment volume","price":take},
          {"name":"Other value added services","revenue":round(ovas,6),"ebit_margin":a["margin"][i],"volume":None,"volume_unit":"not disclosed separately","price":None}],
          "tax_rate":.22,"da":round(revenue*.028,6),"capex":round(revenue*a["capex_rate"],6),"delta_nwc":round(nwc,6),"corporate_cost":0,
          "shares_m":pypl["shares_m"],"dividend_per_share":.56*(1.02**i),"net_debt_issuance":0,"new_equity_issuance":0,
          "notes":"Consolidated margin allocated proportionally across disclosed revenue categories; separate brand/product profitability is NOT disclosed or inferred. Capex includes maintenance,growth,capitalized SBC cash equivalent. Forecast computed from analyst driver paths."}
        if i==0:row["stub_dividend_per_share"]=.14
        sc["years"].append(row)
        demand.append({"ticker":"PYPL","scenario":name,"year":y,"active_accounts_m":accounts,"annual_transactions_per_account":intensity,"transactions_m":transactions,"average_ticket_usd":ticket,"tpv_usd_m":tpv,"fee_rate":take,"revenue_usd_m":revenue,"supply_constraint":"No measured physical processing shortage; supply expands with infrastructure spend. Competition and fees constrain cash capture."})
        prior_rev=revenue;prior_ovas=ovas
    pypl["scenarios"][name]=sc
companies.append(pypl)

fisv={"ticker":"FISV","company":"Fiserv","currency":"USD","valuation_date":"2026-09-08","price":51.39,"price_timestamp":"2026-09-08T14:35:00Z",
 "shares_m":538.566721,"basic_shares_m":531.766721,"shares_date":"2026-07-31","balance_date":"2026-06-30",
 "cash_m":627,"minimum_cash_m":500,"debt_m":28058,"senior_claims_m":100,"other_assets_m":0,"debt_interest_rate":.052,
 "status":"unconfirmed turnaround: retention and normalized service costs not observable",
 "accounting_notes":"Debt includes finance leases and172 of unamortized discounts/hedge adjustments restored to principal. July2bn maturity assumed paid with cash or refinanced: no invented net-debt reduction. Operating leases left in costs. Cash capex plus financed additions are both deducted; FY2026 additions1190=twice disclosed H1595 (126software+19hardware+450financeleases), an annualization assumption, normalizing to650 from2030; no new lease financing credited. Settlement cash1341 and restrictedcash35 excluded; only627 corporate cash less500 reserve. Senior claim100 is conservative NCI value assumption vs22 book; affiliate investments excluded, no nonoperating affiliate profit added. Shares July31 plus1.1m current dilution+5.7m antidilutive RSUs conservatively included; SBC retained in GAAP costs, no extra future dilution. Fading acquisition amortization reduces DA as well as corporate cost; no noncash amortization perpetual windfall. NWC includes merchant lending, contract acquisition payments and cash tax timing. No buyback accretion; no dividend.",
 "history":[{"year":y,"revenue":r,"ebit":e,"da":d,"capex":k,"cfo":c,"sbc":s,"source_ids":["PAY5"]} for y,r,e,d,k,c,s in [(2023,19093,5014,3121,1388,5162,342),(2024,20456,5879,3095,1569,6631,367),(2025,21193,5818,3161,1763,6062,357)]],
 "interim":{"period":"H1 2026","revenue":10319,"ebit":1933,"da":1676,"capex":956,"noncash_financed_additions":595,"cfo":2082,"sbc":235,"source_ids":["PAY4","PAY6"]},
 "sources":sources[3:6],"scenarios":{}}
fisv_assumptions={
 "downside":{"probability":.35,"wacc":.115,"terminal_growth":0,"terminal_roic":.10,"mg":[0,-.03,-.02,0,.01,.01,.01,.01,.01,.01],"fg":[0,-.06,-.04,-.02,0,0,0,0,0,0],"mm":[.285,.245,.235,.23,.23,.23,.23,.23,.23,.23],"fm":[.385,.32,.30,.30,.30,.30,.30,.30,.30,.30],"corp":[2600,2500,2400,2300,2200,2100,2000,1900,1900,1900],"capex":.10,"tax":.26},
 "base":{"probability":.45,"wacc":.10,"terminal_growth":.02,"terminal_roic":.15,"mg":[0,.03,.05,.05,.045,.04,.035,.03,.03,.03],"fg":[0,-.02,0,.02,.025,.025,.02,.02,.02,.02],"mm":[.285,.29,.30,.31,.315,.32,.32,.32,.32,.32],"fm":[.385,.38,.385,.39,.40,.40,.40,.40,.40,.40],"corp":[2600,2550,2450,2300,2150,2050,2000,2000,2000,2000],"capex":.095,"tax":.24},
 "upside":{"probability":.20,"wacc":.095,"terminal_growth":.025,"terminal_roic":.18,"mg":[0,.06,.08,.08,.07,.06,.05,.045,.04,.035],"fg":[0,.015,.035,.04,.04,.035,.03,.025,.025,.025],"mm":[.285,.315,.335,.345,.35,.35,.35,.35,.35,.35],"fm":[.385,.40,.42,.435,.445,.45,.45,.45,.45,.45],"corp":[2600,2450,2200,2050,1900,1850,1850,1850,1850,1850],"capex":.09,"tax":.23}}
for name,a in fisv_assumptions.items():
    sc={k:a[k] for k in ["probability","wacc","terminal_growth","terminal_roic"]};sc["years"]=[]
    merchant=10200;financial=9400;postage=1380;prior_rev=21193
    for i,y in enumerate(range(2026,2036)):
        if i:merchant*=1+a["mg"][i];financial*=1+a["fg"][i];postage*=1.01
        rev=merchant+financial+postage
        # DA components: operational software/property8.5% revenue + acquisition runoff.
        da=rev*.085+max(150,1250-i*140)
        # Annual client-acquisition and financing/cash-tax funding not ignored even without revenue growth.
        nwc=max(250,.07*(rev-prior_rev)+250)
        sc["years"].append({"year":y,"period_end":f"{y}-12-31","segments":[
          {"name":"Merchant Solutions","revenue":round(merchant,6),"ebit_margin":a["mm"][i],"volume":merchant/10200*100,"volume_unit":"2026 fee-equivalent activity index=100 (absolute volume undisclosed)","price":102},
          {"name":"Financial Solutions","revenue":round(financial,6),"ebit_margin":a["fm"][i],"volume":financial/9400*100,"volume_unit":"2026 fee-equivalent account/service index=100 (absolute count undisclosed)","price":94},
          {"name":"Postage pass-through","revenue":round(postage,6),"ebit_margin":0,"volume":None,"volume_unit":"not required for profit capture","price":None}],
          "corporate_cost":a["corp"][i],"tax_rate":a["tax"],"da":round(da,6),"capex":round(rev*a["capex"]+[1190,1000,850,750,650,650,650,650,650,650][i],6),"cash_capex":round(rev*a["capex"],6),"financed_capex":[1190,1000,850,750,650,650,650,650,650,650][i],"delta_nwc":round(nwc,6),"shares_m":fisv["shares_m"],"dividend_per_share":0,"net_debt_issuance":0,"new_equity_issuance":0,
          "notes":"Fee-equivalent indices are revenue sensitivities, NOT independently observed operational volumes. This evidence gap prevents a confirmed recommendation. Absolute throughput/utilization not disclosed. Revenue growth includes client retention, unit transactions and pricing jointly."})
        prior_rev=rev
    fisv["scenarios"][name]=sc
fisv["sources"].append(sources[9])
# Separate physical demand sensitivity from fee capture. GPV is an observed 2025
# anchor; future GPV growth is independent analyst judgment. Fee capture shown
# is an all-in revenue/GPV ratio, not a posted merchant card fee.
for name,sc in fisv["scenarios"].items():
    gpv=4_600_000*1.06
    for i,row in enumerate(sc["years"]):
        if i:gpv*=1+{"downside":.02,"base":.055,"upside":.08}[name]
        segment=row["segments"][0]
        segment.update(volume=round(gpv,6),volume_unit="USD million merchant gross payment volume",price=segment["revenue"]/gpv)
        row["notes"]="Merchant volume grows independently from2025primary4.6trGPV; all-in revenueyield explicitly includes software/services and is not a quotedprocessingfee. FinancialSolutionaccount/transactioncounts remainunresolved; its fee-equivalentindex is an operating sensitivity,not a physicalestimate. All forecast values are analyst assumptions."
        demand.append({"ticker":"FISV","scenario":name,"year":row["year"],"merchant_gpv_usd_m":gpv,"merchant_revenue_usd_m":segment["revenue"],"all_in_revenue_yield":segment["price"],"supply_constraint":"Managementreports10kTPSregular,over30kTPStested; benchmarknotannualqualifiedoutput. No physicalscarcityrent modeled. Servicequality/clientretention remain decisive uncertainties."})
companies.append(fisv)
(HERE/"inputs.json").write_text(json.dumps(companies,indent=2)+"\n")
(HERE/"sources.json").write_text(json.dumps(sources,indent=2)+"\n")
(HERE/"demand_supply.json").write_text(json.dumps(demand,indent=2)+"\n")
