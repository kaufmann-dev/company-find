from pathlib import Path
import json,sys,copy,csv
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]));import model
sources=[]
def add(i,title,date,url,section,supports):
 sources.append(dict(id=f'DC{i}',title=title,publication_date=date,url=url,section=section,supports=supports,source_type='Primary company disclosure' if i not in [1,22,23] else 'Primary market/industry data'))
add(1,'Massive synchronized cyclicals market capture','2026-09-08','https://massive.com/docs/rest/stocks/snapshots/unified-snapshot','GET /v3/snapshot, /v3/reference/tickers/STLA and ASIX; /stocks/v1/dividends and splits; C:EURUSD prior bar','11 intraday quotes; ordinary share classification; shares; no split records since2025; ASIX dividends; EURUSD close1.16276 Sept7. Raw response in market_capture.json.')
add(2,'Stellantis second-quarter 2026 results','2026-07-30','https://www.stellantis.com/en/news/press-releases/2026/july/second-quarter-2026-financial-results','Financial highlights and 2026 guidance','Q2/H1 operating results; Q2 industrialFCF1bn; 2026 capex+R&D6.5–7% revenue; positive industrialFCF2027 management expectation; tariffs and reset cash.')
add(3,'Stellantis June2026 interim report','2026-07-30','https://www.sec.gov/Archives/edgar/data/1605484/000160548426000064/stellantisnv20260630semi-a.htm','Results by segment pp22–39; liquidity pp40–46; notes10–13,18–19','Regional revenue/shipments/AOI; industrial net debt bridge; cash restrictions; pensions/OPEB; provisions; hybrid terms; basic/diluted shares and SBC.')
add(4,'Stellantis FY2025 annual report and20-F','2026-02-26','https://www.stellantis.com/content/dam/stellantis-corporate/investors/financial-reports/Stellantis-NV-20251231-Annual-Report.pdf','Results pp61–78; statements printedpp335–338; notes19–20,30–31','2023–25 financial history, 2024–25 regional margins; industrial cashflow; lease cashouts pp460; pensionliabilities and planassets pp413–414; SBCpp413.')
add(5,'Stellantis supplemental industrial and financial statements','2026-07-30','https://www.sec.gov/Archives/edgar/data/1605484/000160548426000066/stellantisnv20260630supple.htm','Income statement, financial position, cashflow by activity','H1 industrial revenue79141/EBIT1136/DA3142/CFO2557EURm; captive equity9340/NI206; industrial cash31217.')
add(6,'Stellantis FaSTLAne financial framework','2026-05-21','https://www.stellantis.com/en/news/press-releases/2026/may/stellantis-presents-fastlane-2030-financial-framework-and-targets-at-investor-day-2026','Financial targets; Financial Services','Management190bn revenue/7%AOI/6bnIFCF2030; 6bn cost reduction2028; financeAOI>1.5bn2030; managed85bn includes unconsolidated JVs, not company assets.')
add(7,'Stellantis FaSTLAne industrial footprint and regional targets','2026-05-21','https://www.stellantis.com/en/news/press-releases/2026/may/stellantis-unveils-60-billion-euro-strategic-plan-to-accelerate-growth-and-profit','Optimized Manufacturing Footprint; regional targets','Management Europe capacity reduction>800k, utilization60→80%; productprogram60bn includes R&D; Europe3–5%AOI/NA8–10%. Partnerships may require definitive agreements.')
add(8,'Stellantis strategic reset announcement','2026-02-06','https://www.stellantis.com/en/news/press-releases/2026/february/stellantis-resets-its-business-to-meet-customer-preferences-and-to-support-profitable-growth','Reset charges and dividend','22.2bnH225charges,6.5bn associatedcashoverfouryears; BEVprogram and supplychain cancellations; 2026commondividend suspended.')
add(9,'AdvanSix Q2 results','2026-08-07','https://www.sec.gov/Archives/edgar/data/1673985/000167398526000045/exhibit99q22026prearningsa.htm','Performance and outlook; product revenue','421.3mrevenue; volume−15%price+18%; EBITDA31.9; FYcapex75–95m; sulfur pressure; product sales split.')
add(10,'AdvanSix FY2025 Form10-K','2026-02-20','https://www.sec.gov/Archives/edgar/data/1673985/000167398526000008/asix-20251231.htm','Business; statements pp43–46; notes8–10','Integrated manufacturing role; companyestimates7.7Mtnylon6,56%utilization; carpet substitution;2023–25history; financeleases2.139mDec25; pensionoverfunded3.007m; securedrevolver.')
add(11,'AdvanSix June2026 Form10-Q','2026-08-07','https://www.sec.gov/Archives/edgar/data/1673985/000167398526000049/asix-20260630.htm','Statements pp3–6; EPSnote; segmentnote12; liquidity','Debt275/cash7.217/shares27.001186; dilutiveawards.555716; H1CFO−5.294; revolver48mexpiresOct2026/452mOct2027; supplierfinance12.2m.')
add(12,'HF Sinclair Q2 results','2026-07-28','https://www.hfsinclair.com/investor-relations/press-releases/Press-Release-Details/2026/HF-Sinclair-Reports-2026-Second-Quarter-Results-and-Announces-Increase-in-Regular-Cash-Dividend/default.aspx','Refining; lubricants; financial results','Q2adjusted refiningmargin25.95/barrel and639680bpdcharge; NI892m; lubricantsEBITDA207m; FIFO46mbenefit; cash2.262bn.')
add(13,'Huntsman Q2 results','2026-07-30','https://www.huntsman.com/investors/newsroom/news-releases/detail/629/huntsman-announces-second-quarter-2026-earnings','Highlights and segment analysis','Polyurethanes/performanceproducts/advancedmaterials; EBITDA120m; Q2FCF−90m; Olin allstockmerger signedJune16.')
add(14,'Celanese Q2 prepared management comments','2026-08-04','https://www.sec.gov/Archives/edgar/data/1306830/000130683026000114/q220268-kex991a.htm','Acetyl Chain; Engineered Materials; Q3 outlook','Scarcity benefits and subsequent normalization; higher materialcostlag; medical/electronics qualifications.')
add(15,'Celanese Q2 release','2026-08-04','https://investors.celanese.com/news/celanese-corporation-reports-second-quarter-earnings/4f485280-d86f-43f3-8068-de01ca04a02c','Balance and earnings','Debt12.007bn; EPSGAAP1.15/adjusted2.45; cash flow and productgroup economics.')
add(16,'Sibanye-Stillwater interim results','2026-09-01','https://www.sec.gov/Archives/edgar/data/1786909/000162828026059701/form6-kh137.htm','Operating results; liquidity pp12–14; all-in costs','PGM/gold role; higher metalprices explainearnings rebound; workingcapital9.361bnZAR benefit; netdebt9.718bnZAR excludesBurnstone; equity dilutionconvertible.')
add(17,'Vale Q2 performance','2026-07-30','https://www.sec.gov/Archives/edgar/data/917851/000129281426004002/valepr2q26_6k.htm','Financial highlights; Iron Ore Solutions and Base Metals','Ironore/copper/nickel production; SerraSul20Mtcapacity startsJuly; copperprice14062/t; expandednetdebt16.677bn andcapex5.4–5.7bnguide.')
add(18,'Ecopetrol first-half2026 results','2026-08-03','https://www.sec.gov/Archives/edgar/data/1444406/000129281426004040/ex99-1.htm','Financial/operational summary and keymessages','Upstream/refining/transport/transmission;706kboed;refiningmargin29.8/bbl;FEPC8trCOP; naturaldecline~18%requires reinvestment.')
add(19,'Petrobras Q2 financial performance','2026-08-06','https://www.sec.gov/Archives/edgar/data/1119639/000129281426004129/pbrrmf2q26usd_6k.htm','Results; liquidity; debt; financial statements','Pre-salt/refining; FPSOP79start180kbpd;reportedFCFexcludesleaseprincipal; netdebt60.388bn;Q2Brent104.52/barrel.')
add(20,'Methanex Q2 results','2026-07-28','https://www.methanex.com/news/release/methanex-reports-record-north-american-production-and-second-quarter-2026-earnings/','Operational data','AttributableQ2production2.213Mt andrealization529/t vs351Q1; OCIacquisitionincreasescapacity; equitystakesdifferentfromconsolidatedgross.')
add(21,'Mosaic Q2 results','2026-08-04','https://www.sec.gov/Archives/edgar/data/1285785/000128578526000109/pressreleaseq22026-ex991.htm','Results; production and third-quarteroutlook','Phosphate/potash/Brazildistribution; sulfur705/longtonQ3; operatingloss36m;replacement/capex1.2bn.')
add(22,'ACEA EU H1 registrations','2026-07-23','https://www.acea.auto/pc-registrations/new-car-registrations-5-7-in-h1-2026-battery-electric-20-7-market-share/','New EU car registrations by power source','EUcarregistrations+5.7%;BEV20.7%/hybrid37.3%; aggregateindustrygrowthdoesnotprotectStellantismargins.')
add(23,'Federal Reserve FRED BEA vehicle sales table','2026-09-02','https://fred.stlouisfed.org/release/tables?eid=44958&rid=93','August2026 total light vehicles','BEAsourced lightvehicleSAAR16.764m; annualizedmonthly pace, notactualannualsales.')
add(24,'GM Q2 shareholder letter','2026-07-21','https://news.gm.com/home.detail.html/Pages/news/us/en/2026/jul/0721-GM-letter-shareholders-Q2-2026.html','North America operatingmargin','8.6%Q2NAadjustedEBITmargin; contemporaneouscompetitivebenchmark, notSTLAforecast.')
add(25,'Renault H1 results','2026-07-29','https://media.renaultgroup.com/renault-group-delivers-robust-performance-confirms-its-2026-fy-guidance-and-rapidly-implements-futuready/?lang=eng','Automotive/finance results','Automotive3.0%operatingmargin,group5.2%;reinforcesneedto separatefinance;2.1monthsorderbook.')
add(26,'Volkswagen H1 results','2026-07-24','https://www.volkswagen-group.com/en/press-releases/volkswagen-group-stays-on-track-in-challenging-environment-and-expects-improved-margin-in-the-second-half-of-the-year-20542','Results and outlook','Group3.8%operatingmargin and4–5.5%FYguide;competitive urbanEV70korders; efficientrivals competeaway savings.')
add(27,'Methanex New Zealand operating update','2026-09-01','https://www.methanex.com/news/release/methanex-provides-update-on-new-zealand-operations/','Gas entitlement sale and production','GascontractentitlementssoldfromQ12027; plantindefiniteidling; inputbottleneck cantransfer valueawayfrommanufacturer.')
add(28,'Stellantis FY2025 financial presentation','2026-02-26','https://www.stellantis.com/content/dam/stellantis-corporate/investors/events-and-presentations/presentations/Stellantis-FY2025-Financial-Results-Presentation.pdf','Slide10 industrial AOI to cash flow','IndustrialAOI/DA2024–25; broadcapitalmetricincludesinvestmentssoseparatefromcashPP&Ecapex.')
lookup={s['id']:s for s in sources}
rows=[
('STLA','Stellantis','Netherlands','Automotive manufacturing and captive finance',5.41,'DC3','Five regional vehicle businesses; financial operations separately reported.','Replacement/newmodel demand, lower factory underutilization and ordinary regional margins could restore cashflow without returning to2023 recordprofits.','advance','Corrected DCF base $7.25 / weighted $7.72; serious turnaround risk. Fails extreme-gap hurdle after cash research spending and replacement investment are aligned. Combined stress is zero; hybrids, pension claims and operating cash reserve deducted.'),
('DINO','HF Sinclair','United States','Refined fuels and lubricants',109.132,'DC12','Refineries, renewablediesel, marketing, lubricants andmidstream.','Closed/high-cost supply andregionaldistribution create crackspread andbaseoilmargin opportunities.','not advanced','Q2refiningmargin25.95/barrel andlubricantFIFO benefit already exceptional; high currentprice cannot be justified using one-quarter annualization. No normalized DCF completed; rejection is research priority, not demonstrated overvaluation.'),
('HUN','Huntsman','United States','Polyurethanes and specialty materials',9.655,'DC13','Polyurethanes/performanceproducts/advancedmaterials manufacturer.','Construction/insulation recovery and rationalization raise fixed-cost absorption.','not advanced','Signed all-stock Olin merger changes security economics; standalonecashmodel misleading; Q2FCF−90m despiteEBITDA120m. Combined merger valuation unresolved.'),
('CE','Celanese','United States','Acetyl chemicals and engineering polymers',44.8291,'DC14','Acetyl chain supplier andqualified engineeredmaterial producer.','Low-cost Westernassets andmedical/electronics mix can improve margins; temporarycompetitor disruptions also benefitcash.','not advanced','Company itself anticipates supplyopportunitynormalization andrawmateriallag;12.007bndebt givescreditorsfirstclaim. Full cycle/restructuringnotresolved, not a proven short.'),
('ASIX','AdvanSix','United States','Integrated nylon and ammonium sulfate',17.44,'DC10','Integrated cumene→phenol/acetone→caprolactam/nylon withammoniumsulfate coproduct.','Growth capexrolloff andgranularnutrientmix could convert depressedearnings into morecash.','reject after model','Base12.04/weighted12.94; even6%normalizedEBITmarginabove2023–25fails. Globalnylon6utilization56%;capitalspendingdoesnotdisappear;Oct2027refinancing.'),
('SBSW','Sibanye-Stillwater','South Africa','PGM and gold mining',13.2515,'DC16','SouthAfricanPGM/gold andUSPGM producerwithrecycling.','Closures andcostdiscipline can strengthen basketprices;higherpricesprovide operatingleverage.','not advanced','H1rebound depends onhighermetalpricesand9.361bnZARworkingcapitalbenefit; cash/debtdefinitionsexcludeBurnstone. ADS/localshareandconvertiblebridge requiredbeforefinalDCF.'),
('VALE','Vale','Brazil','Iron ore and base metals',15.7283,'DC17','Ironore/copper/nickel mines andlogistics.','Low-costore volumesandcopperprojects canoffsetdecliningorepremiums.','not advanced','SerraSul+20addsitsownsupply; copperprice14062/talreadystrong;expandedclaims16.677bn. Needoreoversupplyandliabilitymodel;noextremegapestablishedatcurrentquote.'),
('EC','Ecopetrol','Colombia','Integrated oil and regulated infrastructure',17.695,'DC18','Upstream/refining/transport andISAtransmission.','Refineryutilization andregulatedassetscouldstabilizecashthrough oilcycle.','not advanced','Record29.8/barrelrefiningmargin is cyclical, upstreamdecline~18%requiresheavyreplacementinvestment,FEPCreceivable8trCOPlocks cash. Political/corporateacquisitionclaimbridge unresolved.'),
('PBR','Petrobras','Brazil','Offshore oil and refining',20.885,'DC19','Brazilpre-saltproducer andrefiner;newFPSOsramping.','Low liftingcostandnewplatformvolume maygeneratecash despitecommoditynormalization.','not advanced','Q2Brent104.52/barrelandreportedFCFexcludesleaseprincipal;60.388bnnetdebtincludesleasedFPSOs. Needfullcommodity/reserve/decommissioningDCF;ADRratio notusedtoinventcap.'),
('MEOH','Methanex','Canada','Methanol',58.785,'DC20','Globalmethanolproducerwithattributableownershipandtradingvolumes.','Gasconstrainedplantsclosewhilelow-costNorthAmericancapacitycaptures supplytightness.','not advanced','529/tQ2realization vs351Q1 alreadycapturesdisruption; Sept1announcementidlesNZin2027andsellsgasentitlements, showingvaluecanaccruetogasbuyers. Nojustificationforcapitalizingpeakspread.'),
('MOS','Mosaic','United States','Phosphate and potash fertilizers',26.5633,'DC21','Integratedphosphate/potashminingandBrazilfertilizerproduction/distribution.','Sulfur normalization couldrestorephosphate margins;lowcapitalgrowthallowscashrecovery.','not advanced','Scarcity presentlyhurts: sulfur705/longtonQ3,operatingloss36m;1.2bncapexandBrazilcurtailmentslimitimmediatecash;Maadenassetbridge requires separatevaluation.')]
screen=[]
for t,n,c,ch,price,src,role,mech,decision,reason in rows:
 ss=lookup[src]
 screen.append(dict(ticker=t,company=n,country=c,value_chain=ch,listing_exchange='Nasdaq' if t=='MEOH' else 'NYSE',price=price,price_timestamp='2026-09-08T15:34 UTC; exact nanosecond tick in market_capture.json',role=role,role_evidence={'publication_date':ss['publication_date'],'url':ss['url'],'section':ss['section']},financial_mechanism=mech,decision=decision,reason=reason,source_ids=[src,'DC1']))
reviewed=json.load(open(P/'screen_text.json')) if (P/'screen_text.json').exists() else {}
for row in screen:
    if row['ticker'] in reviewed: row.update(reviewed[row['ticker']])
frozen=json.load(open('outputs/market_quotes.json'))
for row in screen:
    if row['ticker'] in frozen:
        row['price']=frozen[row['ticker']]['price'];row['price_timestamp']=frozen[row['ticker']]['price_timestamp']
(P/'sources.json').write_text(json.dumps(sources,indent=2)+'\n');(P/'screened.json').write_text(json.dumps(screen,indent=2)+'\n')
cs=json.load(open(P/'inputs.json'))
for c in cs:c['sources']=[lookup[x] for x in (['DC1','DC2','DC3','DC4','DC5','DC6','DC7','DC8','DC22','DC23','DC24','DC25','DC26','DC28'] if c['ticker']=='STLA' else ['DC1','DC9','DC10','DC11'])]
(P/'inputs.json').write_text(json.dumps(cs,indent=2)+'\n')
res=[model.run_company(c) for c in cs]
(P/'valuations.json').write_text(json.dumps(res,indent=2)+'\n')
# Demand versus actual shipment-equivalent usable capacity: no second yield/utilization haircut.
supply=[];stla=cs[0]
for name,s in stla['scenarios'].items():
 for i,r in enumerate(s['years']):
  eu=r['segments'][1]['volume']/1000;na=r['segments'][0]['volume']/1000
  # Approximate effective 2026 capacity is inferred from 2.78m shipment-equivalent /reported60%utilization, not observed factory capacity.
  cap=[4.65,4.58,4.48,4.38,4.25,4.15,4.05,3.98,3.92,3.88][i] if name=='downside' else [4.65,4.50,4.25,4.05,3.85,3.85,3.85,3.85,3.85,3.85][i] if name=='base' else [4.65,4.42,4.18,3.98,3.85,3.87,3.89,3.92,3.95,3.98][i]
  eu_market=14.6*((.988 if name=='downside' else 1.012 if name=='base' else 1.02)**i)
  us_market=16.5*((.993 if name=='downside' else 1.004 if name=='base' else 1.008)**i)
  # Captures European passenger-car retail test separately: plant shipments include LCVs, exports, and inventories; not market-share denominator.
  retail_share=.16+((-0.0015 if name=='downside' else -.0003 if name=='base' else .0002)*i)
  supply.append(dict(year=r['year'],scenario=name,eu30_passenger_car_market_m=eu_market,stellantis_eu30_assumed_retail_share=retail_share,eu30_retail_demand_m=eu_market*retail_share,us_light_vehicle_market_m=us_market,stellantis_na_wholesale_m=na,stellantis_enlarged_europe_wholesale_m=eu,stellantis_europe_effective_shipment_equivalent_capacity_m=cap,shipment_equivalent_utilization=eu/cap,supply_basis='Analyst capacity proxy calibrated to management60% utilization. Actual factory output/nameplate byplant unavailable. Includes LCV/export/mix; not interchangeable with EU30 passengerretails. No additional yield factor. Exactcapacity not decisive because DCF directlystressesmargins.',path='continued oversupply and slow plant rationalization' if name=='downside' else 'orderly normalization with incompleteutilizationrecovery' if name=='base' else 'successful recovery and faster capacity rationalization'))
(P/'demand_supply.json').write_text(json.dumps(supply,indent=2)+'\n')
with open(P/'annual_forecasts.csv','w') as f:
 out=csv.DictWriter(f,fieldnames=['ticker','scenario','year','revenue','ebit','fcff','tax_rate','da','capex','delta_nwc','dividend_per_share','preferred_dividend_m','nonoperating_distributions_m','stub_fcff_adjustment_m','stub_nonoperating_distributions_m']);out.writeheader()
 for c in cs:
  for n,s in c['scenarios'].items():
   for r in model.forecast_years(s):
    o=model.operating(r);out.writerow(dict(ticker=c['ticker'],scenario=n,year=r['year'],**{k:o[k] for k in ['revenue','ebit','fcff']},**{k:r.get(k,0) for k in out.fieldnames if k not in ['ticker','scenario','year','revenue','ebit','fcff']}))
# Reproducible single-variable and combined stress valuation.
c=cs[0];base=c['scenarios']['base'];stress={}
for label in ['margin_minus_100bp','capex_plus_eur1bn','combined_adverse','captive_zero','operating_cash_eur15bn','full_award_dilution']:
 cc=copy.deepcopy(c);sc=copy.deepcopy(base)
 if label in ['margin_minus_100bp','combined_adverse']:
  for r in sc['years']:
   for seg in r['segments']:seg['ebit_margin']-=.01 if label=='margin_minus_100bp' else .0075
 if label in ['capex_plus_eur1bn','combined_adverse']:
  for r in sc['years']:r['capex']+=1162.76
 if label=='combined_adverse':sc.update(wacc=.125,terminal_growth=.005,other_assets_m=(sc['other_assets_m']-2474*1.16276)*.75+2474*1.16276)
 if label=='captive_zero':sc['other_assets_m']=2474*1.16276
 if label=='operating_cash_eur15bn':cc['minimum_cash_m']=15000*1.16276
 if label=='full_award_dilution':cc['shares_m']=2900.941252+63.7
 stress[label]=model.equity_value(cc,sc)['fair_value_per_share']
(P/'stress_results.json').write_text(json.dumps(stress,indent=2)+'\n')
print('Wrote',len(sources),'sources',len(screen),'screens; stress',stress)
