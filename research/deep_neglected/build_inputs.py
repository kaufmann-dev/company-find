"""New neglected-company research inputs, USD millions except shares and per-share prices.

Every forecast number is an analyst assumption. This generator writes only this
research directory. It does not fetch or overwrite the authoritative root quotes.
"""
import datetime as dt
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

SOURCES = [
 ('DN01','Opera 2025 Form 20-F','2026-03-27','https://opera.gcs-web.com/static-files/75f6e636-cfb9-4d76-a034-9219a8f1c930','pp.25–26,36–46; notes 1,3,4,9–13,16,19','2023–25 history; ADS ratio; search renewal; parent control; OPay; development and leases'),
 ('DN02','Opera Q2 2026 results','2026-08-19','https://investor.opera.com/news-releases/news-release-details/opera-reports-second-quarter-2026-results-beyond-high-end','Business highlights; consolidated statements; non-IFRS reconciliation','H1 financials; June balance; July dividend; repurchases; 288m MAUs; 2026 guidance'),
 ('DN03','Opera Q1 2026 results','2026-04-28','https://investor.opera.com/static-files/7df85f85-38b6-4d05-a90f-83580e7d06da','Business highlights and statements','Query/advertising growth and user mix corroboration within issuer, not independent evidence'),
 ('DN04','Gambling.com / Grandstand 2025 Form 20-F','2026-03-19','https://www.sec.gov/Archives/edgar/data/1839799/000183979926000048/gamb-20251231.htm','Items 3,5,15; notes 5,8,13–16,19–23','2023–25 history; control weaknesses; acquired growth; customers and capital commitments'),
 ('DN05','Grandstand Q2 2026 earnings release','2026-08-13','https://www.sec.gov/Archives/edgar/data/1839799/000183979926000138/gamb-q22026xpressrelease.htm','Highlights, outlook and financial statements','2026 revenue/EBITDA guidance; current operations'),
 ('DN06','Grandstand H1 2026 Form 6-K financial report','2026-08-13','https://grandstand.com/investors/media/document/e380013d-af9f-4fb0-aee0-e9204372f868/assets/d293d430-1bb9-4014-98c1-3cba4702ff92.pdf?disposition=inline','pp.2–6,12,18–29,32–39,58–64; notes 4–16,25','Principal debt, cash, awards, acquisition claims, contracts, tax, litigation and NDCs'),
 ('DN07','Grandstand Q2 2026 management call transcript','2026-08-13','https://grandstand.com/investors/media/document/f609d165-085f-481b-9e8e-39ab434073cc/assets/GRSD_Q2_2026_Transcript.pdf?disposition=inline','pp.2–5,7,11','Management statements: 67% non-SEO marketing, 25% workforce reduction, $13m annual savings'),
 ('DN08','OpticOdds API technical documentation',None,'https://developer.opticodds.com/docs/opticodds-for-prediction-market-makers','Prediction-market integrations, streams and order books','Observable product functionality; does not establish paid customer relationships or data rights'),
 ('DN09','Sportradar Q2 2026 results','2026-08-03','https://investors.sportradar.com/news-releases/news-release-details/sportradar-reports-second-quarter-2026-financial-results','Revenue and Business Highlights','Competitor demand and competitive supply; prediction-market contracts; growth partly acquired'),
 ('DN10','Viatris Q2 2026 results','2026-08-06','https://newsroom.viatris.com/2026-08-06-Viatris-Reports-Second-Quarter-2026-Financial-Results','Outlook; cash-flow reconciliation','Global medicines role, actual versus adjusted cash flow'),
 ('DN11','Organon definitive Sun Pharma acquisition agreement','2026-04-26','https://www.organon.com/news/sun-pharma-signs-definitive-agreement-to-acquire-organon/','Transaction terms and conditions','Medicines role; $14 cash acquisition; expected early 2027 close'),
 ('DN12','Organon shareholder vote Form 8-K','2026-07-23','https://www.sec.gov/Archives/edgar/data/1821825/000119312526314587/d128953d8k.htm','Item 5.07','Shareholder approval; transaction remains conditional'),
 ('DN13','Perrigo Q2 2026 results','2026-08-05','https://investor.perrigo.com/2026-08-05-Perrigo-Reports-Second-Quarter-2026-Financial-Results-From-Continuing-Operations','Core OTC operations; balance and cash-flow statements','Volumes/pricing falling, divestiture, debt and cash needs'),
 ('DN14','Criteo Q2 2026 results','2026-08-05','https://criteo.investorroom.com/2026-08-05-CRITEO-REPORTS-SECOND-QUARTER-2026-RESULTS','Business highlights; FY26 outlook; cash-flow statement','Ad-tech role; two client scope reductions; ex-TAC decline; capex'),
 ('DN15','Perion Q2 2026 results','2026-08-10','https://perion.com/investors/press/perion-reports-second-quarter-2026-results/','Results, liquidity and outlook','Ad-tech and search role; operating cash; acquisition-adjusted net cash'),
 ('DN16','Perion acquires PRN','2026-08-26','https://perion.com/investors/press/perion-acquires-prn-a-leading-in-store-retail-media-company-with-exclusive-multi-year-partnerships-across-some-of-north-americas/','Transaction terms','Up to $12m cash at closing; post-balance acquisition'),
 ('DN17','Western Union Q2 2026 results','2026-07-30','https://ir.westernunion.com/news/archived-press-releases/press-release-details/2026/Western-Union-Reports-Second-Quarter-2026-Results/default.aspx','Results, outlook, Intermex assumption','Remittance role; lower guidance and acquisition-alignment issue'),
 ('DN18','AMN Q2 2026 results','2026-08-06','https://ir.amnhealthcare.com/2026-08-06-AMN-HEALTHCARE-ANNOUNCES-SECOND-QUARTER-2026-RESULTS','Segment results; cash and Q3 outlook','Staffing role; temporary strike windfall; client deposits'),
 ('DN19','Pediatrix Q2 2026 results','2026-08-04','https://www.sec.gov/Archives/edgar/data/893949/000119312526331488/md-ex99_1.htm','Operating results; cash and outlook','Physician-services role; profitability, debt and cash'),
 ('DN20','TE Connectivity Q3 FY2026 results','2026-07-22','https://www.te.com/en/about-te/news-center/corporate-news/2026/2026-07-22-te-connectivity-delivers-results-above-guidance-with-14-sales-growth-and-19-eps-growth-in-third-quarter-of-fiscal-2026.html','Results and segment discussion','Connector role and strong current operating conditions'),
 ('DN21','ICON Q2 2026 results','2026-07-29','https://investor.iconplc.com/node/18466/pdf','Results and outlook','Clinical research outsourcing; current revenue and adjusted earnings'),
 ('DN22','US Treasury daily yield curve','2026-09-04','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026','2026-09-04 row','Five-year 4.54%, ten-year 4.78%; nominal USD discount-rate anchor'),
 ('DN23','OpticOdds litigation opposition update','2026-08-05','https://opticodds.com/blog/opticodds-litigation-update','Issuer statement and link to proposed counterclaims filed August 4','Issuer disputes allegations and seeks counterclaims; allegations are not adjudicated facts'),
]
sources=[dict(id=i,title=t,publication_date=d,url=u,section=s,supports=x,type='primary',accessed='2026-09-08') for i,t,d,u,s,x in SOURCES]

RAW_QUOTES=[
 ('AMN',33.525,1788881661739710977),('CRTO',17.4848,1788881641267463061),
 ('ICLR',160.7,1788881658780144430),('MD',26.53,1788881661710719496),
 ('OGN',13.775,1788881662350363868),('OPRA',18.425,1788881656928986320),
 ('PERI',8.94,1788881660762627370),('PRGO',14.665,1788881658924422003),
 ('TEL',209.6,1788881660674366241),('VTRS',16.555,1788881662466657317),
 ('WU',7.135,1788881662357752897),('GRSD',1.91,1788881691495296460)]
quotes={t:dict(ticker=t,price=p,last_minute_last_updated_ns=ts,price_timestamp=dt.datetime.fromtimestamp(ts/1e9,dt.timezone.utc).isoformat(),source='Massive /v3/snapshot last_minute.close; delayed. Timestamp is vendor last_minute.last_updated, not an executable quote.',currency='USD') for t,p,ts in RAW_QUOTES}
# Later parent research freezes synchronized minute quotes for deep models.
authoritative=HERE.parents[1]/'outputs/market_quotes.json'
if authoritative.exists():
 for t,q in json.loads(authoritative.read_text()).items():
  if t in quotes: quotes[t].update(q)

def common(ticker,name,basic,diluted,cash,reserve,debt,claims,other=0):
 return dict(ticker=ticker,company=name,currency='USD',valuation_method='fcff',valuation_date='2026-09-08',price=quotes[ticker]['price'],price_timestamp=quotes[ticker]['price_timestamp'],basic_shares_m=basic,shares_m=diluted,balance_date='2026-06-30',cash_m=cash,minimum_cash_m=reserve,debt_m=debt,senior_claims_m=claims,other_assets_m=other,debt_interest_rate=.08,sources=[],history=[],scenarios={})

opra=common('OPRA','Opera Limited',88.917384,91.076,145.214-35.6,35,0,6,225.675)
opra.update(status='Modelled; moderate valuation gap, not extreme undervaluation',accounting_notes='One ADS equals one ordinary share. Starting cash deducts known July dividend of $35.6m from June cash; no invented July–September operating cash. $35m operating cash reserve is an assumption. $6m senior reserve=$1m repurchase payable+$5m remaining MiniPay commitments; no value assigned to MiniPay associates. Base OPay value is 75% of $300.9m carrying amount; downside zero, upside full carrying value, not an independent OPay valuation. Future EBIT retains SBC and cash rent; DA excludes ROU depreciation and leases are excluded from debt. No future award issuance or repurchase accretion: ongoing SBC is treated as cash-equivalent compensation, existing awards represented by Q2 diluted count. Capitalized development, equipment and allowance for noncash development additions are deducted in capex. Reported DA in history includes leases; forecast DA excludes them. No material defined-benefit pension or minority interest reported in reviewed statements.')
opra['history']=[dict(year=y,revenue=r,ebit=e,da=d,capex=c,cfo=f,sbc=s,lease_cash=l,advertising=a,query=q,source_ids=['DN01']) for y,r,e,d,c,f,s,l,a,q in [
 (2023,396.827,62.890,13.165,6.404,82.761,16.950,3.907,230.980,162.168),
 (2024,480.648,92.262,15.582,30.607,104.977,9.718,4.181,290.723,188.997),
 (2025,614.825,90.072,18.861,15.245,117.728,31.273,4.776,396.040,216.832)]]
opra['latest_interim']=dict(period='H1 2026',revenue=353.839,ebit=55.672,da_including_leases=10.636,cfo=64.337,cash_capex=9.291,sbc_total_expense=14.242,noncash_awards=12.949,lease_principal=2.629,lease_interest=.225,opay_non_cash_gain=6.3,source_ids=['DN02'])
opra_configs={
 'downside':dict(probability=.30,wacc=.12,terminal_growth=.005,terminal_roic=.18,other_assets_m=0,adg=[0,-.12,-.06,0,.02,.03,.03,.02,.02,.01],qg=[0,-.35,-.10,-.05,-.03,0,0,0,0,0],adm=[.075,.035,.035,.04,.045,.05,.05,.05,.05,.05],qm=[.337,.20,.20,.21,.22,.23,.24,.24,.24,.24],userg=[0,-.08,-.04,-.02,0,0,0,0,0,0],reachg=[0,-.08,-.02,0,.01,.01,.01,.01,.01,.01],capratio=.035,daratio=.024),
 'base':dict(probability=.50,wacc=.105,terminal_growth=.025,terminal_roic=.25,other_assets_m=225.675,adg=[0,.18,.16,.14,.12,.10,.08,.07,.06,.05],qg=[0,.12,.10,.08,.07,.06,.05,.04,.03,.03],adm=[.075,.08,.085,.09,.095,.10,.105,.105,.105,.105],qm=[.337,.343,.349,.355,.36,.36,.36,.36,.36,.36],userg=[0,.025,.025,.025,.02,.02,.02,.02,.02,.015],reachg=[0,.08,.07,.06,.05,.04,.03,.03,.02,.02],capratio=.031,daratio=.024),
 'upside':dict(probability=.20,wacc=.10,terminal_growth=.03,terminal_roic=.28,other_assets_m=300.9,adg=[0,.25,.23,.20,.17,.14,.11,.09,.07,.06],qg=[0,.17,.15,.12,.10,.08,.06,.05,.04,.04],adm=[.075,.09,.10,.11,.12,.13,.13,.13,.13,.13],qm=[.337,.35,.36,.37,.38,.38,.38,.38,.38,.38],userg=[0,.05,.04,.035,.03,.03,.025,.02,.02,.02],reachg=[0,.12,.11,.10,.08,.06,.05,.04,.03,.03],capratio=.033,daratio=.025),
}
drivers=[]
for name,config in opra_configs.items():
 ad,query,other,users,reach=490.,246.,2.,288.,520.
 prior=614.825; rows=[]
 for i,year in enumerate(range(2026,2036)):
  if i:
   ad*=1+config['adg'][i];query*=1+config['qg'][i];other*=1.03;users*=1+config['userg'][i];reach*=1+config['reachg'][i]
  revenue=ad+query+other
  row=dict(year=year,period_end=f'{year}-12-31',segments=[dict(name='Advertising (issuer revenue category; allocated margin)',revenue=ad,ebit_margin=config['adm'][i],volume=reach,volume_unit='million average monthly reachable users, estimated; not unique inventory units',price=ad/reach),dict(name='Query (issuer revenue category; allocated margin)',revenue=query,ebit_margin=config['qm'][i],volume=users,volume_unit='million average monthly active users',price=query/users),dict(name='Other',revenue=other,ebit_margin=.20,volume=None,price=None,volume_unit='not material')],corporate_cost=0,tax_rate=.20,da=revenue*config['daratio'],capex=revenue*config['capratio'],delta_nwc=max(0,revenue-prior)*.07,shares_m=91.076,dividend_per_share=(.4 if name=='downside' and year>2026 else .8),stub_dividend_per_share=0,net_debt_issuance=0,new_equity_issuance=0,notes='All forecasts analyst assumptions. Allocated segment EBIT includes corporate overhead, SBC and cash rent. Price fields mean annual category revenue per monthly active/reachable user, combining intensity, mix and monetization, not an observed price. ARPU is full-year revenue/average users, not Q2 annualized ARPU. No MiniPay standalone revenue or AI scarcity premium.')
  rows.append(row);prior=revenue
  drivers.append(dict(ticker='OPRA',scenario=name,year=year,users_m=users,ad_reach_m=reach,query_revenue_per_user=query/users,ad_revenue_per_reachable_user=ad/reach,ad_inventory_capacity_units=None,qualified_capacity_units=None,supply_model='No physical scarcity assumed. Cloud and third-party ad inventory purchased at competitive prices in EBIT; reachable-user estimates are not a capacity census.'))
 opra['scenarios'][name]={k:config[k] for k in ['probability','wacc','terminal_growth','terminal_roic','other_assets_m']}|{'years':rows}
opra['sources']=[s for s in sources if s['id'] in ['DN01','DN02','DN03','DN22']]

# Debt principal, not amortized book debt. Acquired-company earnouts are nonoperating claims.
grsd=common('GRSD','Grandstand Limited (formerly Gambling.com Group)',35.597464,38.200398,8.809,5,126.438,26.479+.126+.5,0)
grsd.update(status='Unconfirmed research candidate: potential large gap; data-rights litigation, refinancing and controls unresolved',debt_interest_rate=.08,accounting_notes='June principal debt $126.438m exceeds balance-sheet amortized-cost borrowings $122.325m. $26.479m deferred purchase consideration and $0.126m contingent consideration are senior claims; a further $0.5m analyst reserve covers separately undisclosed accrued interest, not a reported balance. Face amounts $27.966m due April 2027 and $0.149m April 2028 enter separate dated financing stress, not FCFF. Existing 2.602934m RSUs included fully in initial shares; options at $2.47–14.71 excluded from base and tested separately in upside. Future EBIT retains recurring SBC cash-equivalent cost; no future buyback accretion. Cash rent is in operating margins; DA excludes ROU amortization; leases excluded from debt. Development additions include noncash additions (H1 book addition $2.600m versus cash $2.489m), so potential capitalized awards are not silently omitted. Acquired amortization declines as current customer/software assets expire; replacement development, sales, content and legal expense remain. $2.5m FY27 working-capital settlement allowance covers acquired-employee bonuses/accrued costs; it is not another purchase earnout. Deferred tax assets not valued separately: operating tax forecasts incorporate normalization. Swish litigation exposure is unquantified; downside models business destruction, with separate damages sensitivities. No material minority interest reported.')
grsd['history']=[dict(year=y,revenue=r,ebit=e,da=d,capex=c,cfo=f,sbc=s,marketing=m,data=dat,acquisition_cash_in_cfo=acq,source_ids=['DN04']) for y,r,e,d,c,f,s,m,dat,acq in [
 (2023,108.652,21.778,2.088,9.243,17.910,3.6,101.000,7.652,7.497),
 (2024,127.182,35.675,5.802,24.286,37.638,5.0,118.815,8.367,7.156),
 (2025,165.447,-31.788,14.419,4.756,19.104,6.9,124.320,41.127,18.590)]]
grsd['latest_interim']=dict(period='H1 2026',revenue=78.204,marketing=55.743,data=22.461,ebit=2.095,da_including_leases=7.152,lease_da=.639,cfo=2.702,cash_capex=2.812,noncash_development_difference=.111,sbc=3.447,acquisition_cash_in_cfo=9.784,acquired_employee_bonus_cash=2.813,source_ids=['DN05','DN06'])
grsd_configs={
 'downside':dict(probability=.40,wacc=.16,terminal_growth=0,terminal_roic=.12,mg=[0,-.25,-.20,-.15,-.10,-.06,-.05,-.05,-.05,-.05],dg=[0,-.25,-.15,-.05,0,0,0,0,0,0],mm=[.225,.12,.10,.10,.10,.10,.10,.10,.10,.10],dm=[.27,.12,.13,.15,.17,.18,.18,.18,.18,.18],ndcg=[0,-.15,-.15,-.10,-.06,-.03,-.03,-.03,-.03,-.03],capratio=.04),
 'base':dict(probability=.45,wacc=.12,terminal_growth=.02,terminal_roic=.22,mg=[0,-.08,-.04,-.02,0,.01,.02,.02,.02,.02],dg=[0,.18,.16,.14,.12,.10,.08,.07,.06,.05],mm=[.225,.25,.25,.25,.25,.25,.25,.25,.25,.25],dm=[.27,.29,.30,.31,.32,.32,.32,.32,.32,.32],ndcg=[0,.02,.02,.02,.02,.02,.02,.02,.02,.02],capratio=.04),
 'upside':dict(probability=.15,wacc=.11,terminal_growth=.025,terminal_roic=.25,mg=[0,.03,.05,.06,.06,.05,.04,.04,.03,.03],dg=[0,.28,.25,.22,.18,.15,.12,.10,.08,.06],mm=[.225,.27,.28,.28,.28,.28,.28,.28,.28,.28],dm=[.27,.32,.34,.35,.36,.36,.36,.36,.36,.36],ndcg=[0,.07,.08,.08,.07,.06,.05,.05,.04,.04],capratio=.045),
}
for name,config in grsd_configs.items():
 marketing,data,ndc=121.,46.5,.520
 prior=165.447;rows=[]
 for i,year in enumerate(range(2026,2036)):
  if i:marketing*=1+config['mg'][i];data*=1+config['dg'][i];ndc*=1+config['ndcg'][i]
  revenue=marketing+data
  # Purchased software/customer amortization runs off; new development is capitalized
  # and amortized continuously. No requirement to reacquire the same business annually.
  recurring_da=revenue*.021
  acquired_da=max(0,9.5*(1-i/7))
  da=recurring_da+acquired_da
  corporate=(4.3 if i==0 else 3.0*(1.025**i))+(6 if name=='downside' and i in [1,2] else 0)
  nwc=max(0,revenue-prior)*.08+(2.5 if i==1 else 0)
  rows.append(dict(year=year,period_end=f'{year}-12-31',segments=[dict(name='Marketing (issuer category; allocated margin)',revenue=marketing,ebit_margin=config['mm'][i]-da/revenue,volume=ndc,volume_unit='million annual NDC referrals; revenue also includes retained-cohort share and ticket/other',price=marketing/ndc),dict(name='Sports data subscriptions (issuer category; allocated margin)',revenue=data,ebit_margin=config['dm'][i]-da/revenue,volume=None,price=None,volume_unit='paying seat/client counts undisclosed; see indexed driver decomposition')],corporate_cost=corporate,tax_rate=.20 if i<5 else .23,da=da,capex=revenue*config['capratio'],delta_nwc=nwc,shares_m=38.200398,dividend_per_share=0,net_debt_issuance=0,new_equity_issuance=0,notes='All forecasts analyst assumptions. Marketing/data contribution margins are after recurring SBC, cash rent, sales/content/R&D and cloud expense, before allocated DA and explicit corporate/legal costs. 2026 anchor adopts $167.5m issuer-guidance midpoint, but forecast cash economics are independent of adjusted EBITDA. No acquisitions or Rollcard revenue are assumed. Marketing revenue per NDC is a blended diagnostic, not a CPA price. NDCs do not count retained revenue-share cohorts twice. Financing stress separately settles old acquisition claims and tests 2028 refinancing.'))
  drivers.append(dict(ticker='GRSD',scenario=name,year=year,annual_ndc_m=ndc,marketing_revenue_per_ndc=marketing/ndc,data_subscription_revenue=data,data_revenue_index_2026_100=data/46.5*100,paying_data_customers=None,physical_capacity=None,supply_model='Data subscriptions require licensed/legally obtainable source data, engineers and cloud delivery. Customer counts, renewal rates and rights costs by product are undisclosed; no capacity shortage premium assumed.'))
  prior=revenue
 grsd['scenarios'][name]={k:config[k] for k in ['probability','wacc','terminal_growth','terminal_roic']}|{'years':rows}
grsd['sources']=[s for s in sources if s['id'] in ['DN04','DN05','DN06','DN07','DN08','DN09','DN22','DN23']]

for company in [opra,grsd]:
 for scenario in company['scenarios'].values():
  for row in scenario['years']:
   revenue=sum(s['revenue'] for s in row['segments'])
   row['forecast_sbc_m']=revenue*.04
   row['sbc_note']='Analyst recurring compensation allowance of 4% revenue included in segment margins; do not subtract again. Existing awards included in initial diluted shares.'
   row['forecast_cash_rent_m']=revenue*(.0075 if company['ticker']=='OPRA' else .009)
   row['lease_note']='Cash rent allowance is included in segment margins; DA excludes leases and lease liabilities are excluded from debt.'

def main():
 HERE.mkdir(exist_ok=True)
 for filename,data in [('sources.json',sources),('market_quotes.json',quotes),('inputs.json',[opra,grsd]),('operating_drivers.json',drivers)]:
  (HERE/filename).write_text(json.dumps(data,indent=2)+'\n')

if __name__=='__main__':main()
