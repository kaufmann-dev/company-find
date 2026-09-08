"""Render synchronized investment report and numerical appendix from frozen inputs."""
import csv
from decimal import Decimal, ROUND_HALF_UP
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import model
ROOT=Path(__file__).resolve().parent
ORDER=['CMCSA','PYPL','MWA','AER','GSL','FISV','CF','POWL','IQV']
RISKS={'CMCSA':'bundle monetization, media rights, debt and separation','PYPL':'fee erosion, checkout mix and execution','MWA':'flat units, utility budgets and foundry investment','AER':'lease repricing, funding costs and residual values','GSL':'charter resets, vessel replacement and refinancing','FISV':'retention, financed software investment and debt','CF':'nitrogen normalization, gas spread and Blue Point','POWL':'capacity response and normalization of project margins','IQV':'sponsor budgets, labor costs and economic reinvestment'}
CASES={
 'CMCSA':('Broadband contraction can coexist with durable household connectivity spending. Wireless bundles, business connectivity and parks partly offset video decline; maintaining revenue per customer is the unresolved link.', 'Residential and business connectivity together generate more than all modeled2026 group EBIT before the losses and corporate costs elsewhere. Base broadband subscribers decline from28.5m to26.2m by2035, while wireless lines grow10.15m→20.5m. Monthly broadband revenue per subscriber dips to$72.50 in2027 then rises to$82 in2035. Media is valued on its post-Versant perimeter; no spin-off multiple uplift is assumed.', 'Cohort monetization and sustainable media economics are unresolved. July23 pro forma tables show2025 Media EBITDA of only$164m after the completed separation. Fiber and fixed-wireless competition remain funded alternatives.', 'research/connectivity/research.md'),
 'PYPL':('More transactions do not ensure more retained payment fees. I expect engagement growth but continuing yield compression and moderate margins.', 'Annual accounts × transactions per account × ticket × fee yield, plus value-added services. The base takes margin from16.3% in2026 to15.5% in2027 and16.5% later; fees per dollar of payment volume erode1.7% annually.', 'Q2 transaction-margin dollars excluding balance interest rose3%, versus10% total payment volume growth. Adyen is gaining volume with revenue growing more slowly than processing activity. Those facts favor a modest cash-capture forecast.', 'research/payments/research.md'),
 'MWA':('Water-network renewal creates recurring equipment purchases even when gallons consumed stagnate; affordability and installation crews constrain fulfilled work.', 'Both Water Flow Solutions and Water Management Solutions are modeled. Water Flow represented57.7% of2025 sales. Pricing and foundry productivity support margins, but the base normalizes group EBIT around21% rather than assuming every recent gain repeats.', 'The latest price/volume split, inventory/capex needs and softer housing constrain the volume thesis. Utility need estimates are not appropriated budgets.', 'research/power_water/research.md'),
 'GSL':('Ship time demanded equals goods moved times route length and service requirements. Restoring routes can release capacity without a fall in trade.', 'Existing charter cash is followed through expiry. Renewal investment includes the$1.33bn15-vessel newbuild program; debt refinancing and preferred claims are explicit. A finite2035 fleet residual replaces an eternal franchise value.', 'Contracts support near-term cash, but aging vessels and deliveries absorb it. The normalized small/midsized orderbook and usable-output assumptions remain conditional, not a verified global fleet census.', 'research/agri_transport/research.md'),
 'FISV':('Recurring bank and merchant processing is valuable only after retention costs, engineering investment and creditor claims.', 'Merchant GPV starts from the observed$4.6tr2025 base. Merchant and Financial segment margins mature at32%/40%, less corporate costs. Cash capex plus financed additions are deducted; acquisition amortization fades in both earnings and D&A.', 'Q2 GAAP margin fell sharply despite the long-run payment-activity trend. H1 financed asset additions outside cash capex were$595m. Customer retention and true normalized service cost remain unresolved.', 'research/payments/research.md'),
 'CF':('Crop production needs recurring nutrients, but fertilizer affordability and usable nitrogen additions determine the producer rent.', 'Attributable existing nitrogen output, price and gas economics are separated from the Blue Point investment. CHS distributions and BP minority ownership are reconciled. Temporary settlement cash and noncash sales amortization do not recur.', 'Low-cost US gas is a real advantage; announced nitrogen supply, buyer crop economics and very large project investment prevent extrapolation of current scarcity profits.', 'research/agri_transport/research.md'),
 'POWL':('Growing electricity load and more distributed projects require engineered electrical systems; supplier capacity, standardization and deployment labor respond to elevated returns.', 'Five end markets are forecast separately. Base commercial/industrial sales rise$250m→$850m in2026–30. Consolidated margins eventually normalize; undisclosed end-market margins are not invented.', 'The2023–25 EBIT margin history ranges from8.9% to19.7%. Eaton announced a$242m-plus investment to double Fibrebond enclosure capacity onSeptember2. That is competing project-delivery supply, with the qualification timetable uncertain.', 'research/power_water/research.md'),
 'IQV':('Funded trial starts, duration, outsourcing and complexity generate clinical-service work; automation and sponsor bargaining determine retained economics.', 'Commercial Solutions and R&D Solutions are separate. Backlog is a multi-year stock, not one year of sales. Base group revenue grows near6% early, moderating later; GAAP-like costs include SBC and recurring investment.', 'Revenue recovered while2025 andH12026 operating profit conversion was weak. Trial starts remain below the2021 peak; current aggregate qualified capacity and retention economics are unresolved.', 'research/aviation_health/research.md')}

def table(headers,rows):
    def cell(x):return str(x).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(cell(x) for x in row)+' |' for row in rows])+'\n'
def money(v):return f"{Decimal(str(v)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP):,}"
def pct(v):return f'{v*100:+.1f}%'
def write(name,text):
    # Add readable spacing in compact analyst notes; preserve code and link targets.
    parts=re.split(r'(`[^`]*`|https?://[^\s)]+|\]\([^)]*\))',text)
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r'(?<=[a-z])(?=\d|\$)', ' ', parts[i])
        parts[i]=re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', parts[i])
        parts[i]=re.sub(r'(?<=[%;])(?=\d)', ' ', parts[i])
    text=''.join(parts)
    p=ROOT/name;p.write_text(text)
    formatter=Path('/code/.agents/skills/md-table-formatter/format-table.py')
    if formatter.exists():
        formatted=subprocess.check_output(['python',str(formatter),str(p)],text=True)
        # Formatting must preserve every non-whitespace table cell.
        def cells(value):
            return [[re.sub(r'^(:?)-+(:?)$',r'\1---\2',x.strip()) for x in line.split('|')]
                    for line in value.splitlines() if line.startswith('|')]
        before=cells(text)
        after=cells(formatted)
        assert before==after,name
        p.write_text(formatted)

def main():
    companies={}
    for p in ROOT.glob('research/*/inputs.json'):
        for c in json.loads(p.read_text()):companies[c['ticker']]=c
    results={r['ticker']:r for r in json.loads((ROOT/'outputs/valuations.json').read_text())}
    results['AER']=json.loads((ROOT/'research/aviation_health/aer_valuation.json').read_text())
    (ROOT/'outputs/all_valuations.json').write_text(json.dumps([results[t] for t in sorted(results)],indent=2)+'\n')
    comparison=[]
    for t in ORDER:
        r=results[t];s=r['scenarios']
        comparison.append([t,money(r['price']),'/'.join(money(s[n]['fair_value_per_share']) for n in ['downside','base','upside']),money(r['probability_weighted_fair_value']),pct(r['upside']),pct(r['margin_of_safety']),pct(r['expected_cashflow_annualized_return']),RISKS[t]])
    app=['**Initial comparison valuation appendix — 8 September 2026**\n',
    'Amounts are USD millions unless explicitly per share. Every2026–40 forecast is an analyst assumption or calculated consequence, not an observed fact. Annual source history and primary links are retained in each company input. Full annual segment volumes, prices and revenue are in [segment_forecasts.csv](outputs/segment_forecasts.csv); no revenue-calibrated index is presented as an observed physical count.\n',
    '`FCFF = EBIT × (1 − operating tax rate) + D&A − all-in capital expenditure − change in operating working capital`. Discount each remaining annual cash flow to8September2026 at its scenario nominal USD WACC. Equity equals operating EV plus excess corporate cash/nonoperating assets less debt and other claims; common value cannot be negative. Present fair value divides by current diluted shares.\n',
    'For conventional DCFs,2036–40 scales sales/costs/D&A with terminal growth and holds margins fixed. Reinvestment gradually approaches the greater of2035 net reinvestment and `NOPAT × g / terminal ROIC`. The larger existing replacement requirement is retained as a floor; it does not disappear because a terminal formula assumes accounting D&A equals maintenance investment. Terminal FCFF uses this mature investment burden. This explicit analytical transition avoids an unexplained cash-flow step; it remains a valuation assumption. GSL uses an explicit finite fleet residual instead. AerCap uses FCFE after required equity investment, described separately.\n',
    'Discount rates are judgmental required returns, not inferred market forecasts or fitted historical betas. The latest available official10-year Treasury observation was4.78% on4September2026;5-year was4.54%. Operating and financing risks justify the additional spread, with sensitivities shown. Terminal nominal growth generally1–3% is below early demand growth; ROIC assumptions require reinvestment. [US Treasury2026 daily curve,4September row](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026).\n',
    'Future shareholder return uses dated dividends and the8September2031 residual equity value. Residual FCFE is retained at zero interest and included once. No speculative buyback accretion is assumed. SBC remains an economic expense; existing awards enter current dilution and future remuneration is treated as a cash equivalent, avoiding an extra dilution deduction. Declared distributions to prior holders are excluded. A positive IRR can coexist with a zero present common residual if dividends precede loss of exit equity. Probabilities are reasoned scenario weights, not measured frequencies.\n']
    for t in ORDER:
        c=companies[t];r=results[t];ss=r['scenarios'];custom=t=='AER'
        app.append(f'**{t} — {c["company"]}**\n')
        app.append(f'Current price${r["price"]:.4f}; observation{r["price_timestamp"]}. Basic equity value${r["current_equity_m"]:,.0f}m; diluted equity capitalization${r["diluted_equity_m"]:,.0f}m; conventional current EV${r.get("conventional_ev_m",r["current_ev_m"]):,.0f}m; operating-reserve-adjusted current EV${r["current_ev_m"]:,.0f}m. '+('AER EV is descriptive only; debt finances earning assets and is already modeled in the equity cash bridge.' if custom else 'Basic capitalization is reported separately from the diluted valuation denominator.')+'\n')
        app.append(c.get('accounting_notes','See input accounting bridge.')+'\n')
        if t=='CF':app.append('CF operating EV is an attributable economic perimeter after the CHS/BP look-through adjustments, not full consolidated EV including a separately marked-to-market NCI claim.\n')
        app.append(table(['Year','Revenue','EBIT','D&A','Cash capex','Operating cash flow'],[[h['year'],money(h['revenue']) if 'revenue' in h else 'n/a',money(h.get('ebit',0)) if h.get('ebit') is not None else 'n/a',money(h['da']) if 'da' in h else 'n/a',money(h['capex']) if 'capex' in h else 'n/a',money(h['cfo']) if 'cfo' in h else 'n/a'] for h in c['history']]))
        app.append('Unavailable historical fields are displayed as n/a and must be checked in the primary statements. Machine-readable history retains actual keys. Cash capex history can exclude financed additions that are explicitly included in the forecasts.\n')
        app.append(table(['Case','Probability','Discount','Terminal g','Terminal ROIC','Fair/share today','EV today','Equity today','Terminal contribution','Five-year XIRR','2031 residual/share'],[[n,pct(ss[n]['probability']),f"{c['scenarios'][n].get('wacc',c['scenarios'][n].get('cost_of_equity',0))*100:.2f}%",pct(c['scenarios'][n].get('terminal_growth',0)),pct(c['scenarios'][n].get('terminal_roic',0)) if not custom else 'required equity',money(ss[n]['fair_value_per_share']),money(ss[n].get('enterprise_value_m',0)) if not custom else 'equity DCF',money(ss[n]['equity_value_m']),pct(ss[n].get('terminal_share_of_ev',ss[n].get('terminal_share_of_equity_value',0))),pct(ss[n]['annualized_return']),money(ss[n]['future_equity_per_share'])] for n in ['downside','base','upside']]))
        app.append(f'Weighted present value${r["probability_weighted_fair_value"]:.2f}; gap{pct(r["upside"])}; margin of safety{pct(r["margin_of_safety"])}. XIRR of expected dated cash flows{pct(r["expected_cashflow_annualized_return"])}; arithmetic weighted scenario XIRR{pct(r["expected_scenario_annualized_return"])}. Moving10percentage points from upside to downside gives${r["probability_sensitivity_shift_10pp_upside_to_downside"]:.2f}. All modeled5-year financing shortfalls are zero under the disclosed funding/dividend assumptions; this does not guarantee refinancing availability.\n')
        if custom:
            q=r['reverse_lease_yield'];app.append(f'“The current price can be justified if” average rental yield is{q["parallel_basis_point_change"]:.1f}basis points above the base path with funding, credit, fleet growth and sale gains held fixed. Normalized rental yield would be{q["normalized_2035_lease_yield"]*100:.2f}% versus10.60%. “My forecast differs because” manufacturer delivery ramps eventually relieve fleet tightness and existing leases delay repricing. “The evidence supporting that difference is” OEM capacity plans and the company’s own lower-rate extensions. “The resulting difference in value is”${r["price"]-ss["base"]["fair_value_per_share"]:.2f} above base value. See the [aviation case](research/aviation_health/research.md) for direct primary citations and the capital-equity identity. No aligned consensus was available.\n')
            app.append('Annual NI, fleet investment, disposal proceeds, funding and required equity are in [aer_annual.csv](research/aviation_health/aer_annual.csv), with all segment and asset drivers in [inputs.json](research/aviation_health/inputs.json). Terminal contribution above is a percentage of equity DCF, not operating EV.\n')
            app.append(table(['Equity discount rate','Rental yield change, bp','Fair/share'],[[pct(x['cost_of_equity']),x['rental_yield_change_bp'],money(x['fair_value'])] for x in r['sensitivity']]))
        else:
            thesis,forecast,evidence,path=CASES[t]
            rev=r['reverse_margin'];baseline=model.operating(next(x for x in c['scenarios']['base']['years'] if x['year']==2030))['ebit_margin']
            app.append(thesis+' '+forecast+'\n')
            app.append(f'“The current price can be justified if” base demand/pricing paths earn{rev["parallel_margin_change_percentage_points"]:+.2f}percentage points different EBIT margins across the forecast, producing{rev["price_justifying_2030_margin"]*100:.2f}% in2030. “My forecast differs because” {thesis[0].lower()+thesis[1:]} “The evidence supporting that difference is” {evidence} “The resulting difference in value is” base fair value${ss["base"]["fair_value_per_share"]:.2f} versus price${r["price"]:.2f}, a${ss["base"]["fair_value_per_share"]-r["price"]:+.2f}gap; base2030 margin is{baseline*100:.2f}%. Explicit2026–35 investment is fixed in this reverse calculation;2036–40 normalization and terminal required investment respond consistently to changed NOPAT. This one-dimensional reverse solution is a mathematical price-justifying combination; it does not identify unique market beliefs. No aligned broker consensus was obtained. [Substantive case, primary sources and falsification]({path}).\n')
            app.append(table(['Base WACC','Terminal g','Fair/share'],[[f"{x['wacc']*100:.2f}%",f"{x['g']*100:.2f}%",money(x['fair_value'])] for x in r['sensitivity']]))
            if t=='GSL':app.append('For GSL the g grid has no effect on the fixed fleet residual; only discounting changes. The finite residual sensitivity is in its substantive case. A g/ROIC perpetuity is never substituted for fleet liquidation.\n')
            for n in ['downside','base','upside']:
                app.append(f'Annual {n} operating model; both maintenance and growth investment deducted. '+('The fleet residual is realized in2035; there is no perpetuity.' if t=='GSL' else '2036–40 rows are explicit normalization.')+'\n')
                app.append(table(['FY','Revenue','EBIT margin','EBIT','Tax','D&A','All-in capex','Δ operating WC','FCFF','Net debt issued'],[[x['year'],money(model.operating(x)['revenue']),f"{model.operating(x)['ebit_margin']*100:.1f}%",money(model.operating(x)['ebit']),f"{x['tax_rate']*100:.1f}%",money(x['da']),money(x['capex']),money(x['delta_nwc']),money(model.operating(x)['fcff']),money(x.get('net_debt_issuance',0))] for x in model.forecast_years(c['scenarios'][n])]))
        app.append('Primary model sources: '+', '.join(f'[{s.get("id",t)} — {s.get("publication_date",s.get("date","date in register"))}, {s.get("section","sections in source register")}]({s["url"]})' for s in c['sources'] if 'url' in s)+'.\n')
    write('MODEL_APPENDIX.md','\n'.join(app))
    print('Rendered REPORT.md and MODEL_APPENDIX.md; source tables preserved by formatter')

if __name__=='__main__':main()
