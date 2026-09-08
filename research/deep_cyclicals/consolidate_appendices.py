"""Consolidate all investigated company/source records; preserve raw provenance and deduplicate companies."""
import json,re,collections,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
old=json.load(open(ROOT/'outputs/screened_universe.json'))
oldmap={x['ticker']:x for x in old['companies']}
paths=sorted((ROOT/'research').glob('*/screened.json'),key=lambda p:(p.parent.name.startswith('deep_'),p.parent.name))
source_raw=[]
for p in sorted((ROOT/'research').glob('*/sources.json')):
 for s in json.load(open(p)):source_raw.append({'package':p.parent.name,**s})
byid={x.get('id',x.get('source_id')):x for x in source_raw}
# Source identity is URL+publication date. Market documents are observations by package, not independent economic evidence.
source_map={}
for s in source_raw:
 url=s.get('url',s.get('source_url',''));pub=s.get('publication_date',s.get('date','Unavailable'))
 ismarket=('massive.com' in url or s.get('type')=='market_data' or 'market' in str(s.get('source_type','')).lower())
 key=(url,pub,s['package'] if ismarket else '')
 if key not in source_map:
  source_map[key]=dict(id=s.get('id'),aliases=[],research_packages=[],title=s.get('title',s.get('supports','Source')),url=url,publication_date=pub,section=s.get('section','Section not captured'),supports=s.get('supports',''),source_type=s.get('source_type',s.get('type','Primary issuer / regulator / industry source; classification in research notes')),raw_records=[])
 out=source_map[key]
 if s.get('id')!=out['id'] and s.get('id') not in out['aliases']:out['aliases'].append(s.get('id'))
 if s['package'] not in out['research_packages']:out['research_packages'].append(s['package'])
 out['raw_records'].append(s)
 sources=list(source_map.values())
allrows={}
for p in paths:
 for r in json.load(open(p)):
  t=r['ticker'];allrows.setdefault(t,[]).append({'research_package':p.parent.name,**r})
quotes=json.load(open(ROOT/'outputs/market_quotes.json'))
models={}
for p in (ROOT/'research').glob('*/inputs.json'):
 d=json.load(open(p));d=d if isinstance(d,list) else d.get('companies',[d])
 for c in d:
  if c.get('ticker') and c.get('scenarios'):models[c['ticker']]={'company':c.get('company'), 'package':p.parent.name,'source_ids':[s['id'] for s in c.get('sources',[]) if isinstance(s,dict) and s.get('id')],'status':c.get('status','Detailed model completed')}
namefix={'DECK':'Deckers Outdoor','LULU':'lululemon athletica','CROX':'Crocs','PVH':'PVH Corp.'}
# These are geographic labels from captured coverage, not inferred economic risk concentrations.
countryfix={'DECK':'United States','LULU':'Canada','CROX':'United States','PVH':'United States','VTRS':'United States','OGN':'United States','PRGO':'Ireland','CRTO':'France','PERI':'Israel','OPRA':'Norway','GRSD':'Jersey','WU':'United States','AMN':'United States','MD':'United States','TEL':'Switzerland'}
def normalize_country(t,r):
 if t in oldmap:return oldmap[t]['jurisdiction_label']
 raw=r.get('country') or countryfix.get(t)
 if not raw:return 'Unresolved jurisdiction'
 if 'Cayman' in raw:return 'Cayman Islands / China operations'
 if 'Luxembourg' in raw:return 'Luxembourg'
 if 'Bermuda' in raw:return 'Bermuda' if not raw.startswith('Netherlands') else 'Netherlands / Bermuda'
 if 'UKissuer' in raw:return 'United Kingdom'
 return raw

def chain(t,r):
 if t in oldmap:
  orig=oldmap[t]['economic_chain']
  return 'Automotive manufacturing and propulsion' if orig=='Vehicle propulsion' else orig
 x=r.get('value_chain',r.get('chain','Other investigated chain')).lower()
 if 'insurance' in x or 'retirement' in x:return 'Insurance and reinsurance'
 if 'credit' in x or 'trade finance' in x:return 'Lending and credit platforms'
 if 'automotive' in x:return 'Automotive manufacturing and propulsion'
 if 'chemical' in x or 'nylon' in x or 'polyureth' in x or 'methanol' in x:return 'Industrial chemicals and polymers'
 if 'refin' in x or 'offshore oil' in x or 'integrated oil' in x:return 'Oil production, refining and transport'
 if 'mining' in x or 'metals' in x:return 'Mining and metals'
 if 'footwear' in x or 'apparel' in x:return 'Consumer apparel and footwear'
 if 'medicines' in x or 'consumer healthcare' in x:return 'Medicines and consumer healthcare'
 if 'healthcare' in x:return 'Healthcare delivery and staffing'
 if 'advert' in x or 'software' in x or 'marketing and sports' in x or 'search and cloud' in x:return 'Digital advertising and consumer software'
 if 'commerce' in x or 'retail' in x:return 'Commerce and retail distribution'
 if 'telecom' in x:return 'Connectivity and entertainment distribution'
 if 'tobacco' in x:return 'Tobacco and nicotine'
 if 'payment' in x:return 'Payments and bank processing'
 if 'industrial components' in x:return 'Electrical interconnects'
 return x.title()

def norm(t,r,history):
 ids=r.get('source_ids',[])
 if not ids:ids=[r.get('source_id',r.get('role_source_id'))]
 ids=[i for i in ids if i]
 nested=r.get('role_evidence',r.get('dated_role_source',{}))
 if not isinstance(nested,dict):nested={}
 if nested.get('id') and nested['id'] not in ids:ids.insert(0,nested['id'])
 src=byid.get(ids[0],{}) if ids else {}
 url=nested.get('url') or r.get('source_url') or r.get('role_source') or r.get('dated_primary_source') or src.get('url')
 if isinstance(url,dict):url=url.get('url')
 pub=nested.get('publication_date') or r.get('source_date') or r.get('role_source_date') or src.get('publication_date')
 sec=nested.get('section') or r.get('source_section') or src.get('section') or 'Company release / financial statements'
 role=r.get('role') or oldmap.get(t,{}).get('role')
 mech=r.get('mechanism') or r.get('financial_mechanism') or r.get('potential_financial_mechanism')
 decision=r.get('decision','')
 if r.get('reason'):decision+=' — '+r['reason']
 current_decision=decision
 if t in models:current_decision='Detailed intrinsic model completed. '+models[t]['status']+'. Current numerical comparison is in the report and inputs; original screening decision retained in JSON.'
 if not all([role,mech,url,pub]):raise ValueError((t,'Missing investigation fields',role,mech,url,pub))
 return dict(ticker=t,company=r.get('company') or namefix.get(t) or models.get(t,{}).get('company') or oldmap.get(t,{}).get('company') or t,economic_chain=chain(t,r),jurisdiction_label=normalize_country(t,r),listing=r.get('listing') or r.get('listing_exchange') or oldmap.get(t,{}).get('listing') or 'Listing identifier is ticker; exchange not captured',role=role,financial_mechanism=mech,role_source=dict(publication_date=pub,url=url,section=sec,source_ids=ids),decision=current_decision,screening_decision=decision,research_packages=list(dict.fromkeys(h['research_package'] for h in history)),latest_price_observation=quotes.get(t),investigation_history=history)
companies=[norm(t,hs[-1],hs) for t,hs in allrows.items()]
companies.sort(key=lambda r:(r['economic_chain'],r['company']))
counts=dict(sorted(collections.Counter(r['economic_chain'] for r in companies).items()));geo=dict(sorted(collections.Counter(r['jurisdiction_label'] for r in companies).items()))
meta=dict(research_date='2026-09-08',investigated_company_count=len(companies),investigation_record_count=sum(map(len,allrows.values())),conservative_economic_chain_count=len(counts),jurisdiction_label_count=len(geo),detailed_model_count=len(models),economic_chains=counts,jurisdictions=geo,geographic_caveat='Labels mix incorporation, headquarters and captured primary listing jurisdictions. Cayman/China and other combinations are composite labels, not independent countries or revenue exposures. AerCap label is headquarters. New missing-country cases are resolved from captured company identity/context and explicit countryfix; no currency or ADR valuation bridge is inferred.',coverage_caveats=['Investigated breadth, not a globally exhaustive cheap-stock screen.','Repeated companies counted once; earlier role evidence preserved in investigation_history.','Most screens are research-priority decisions without a full intrinsic valuation; those are not proven overvaluation claims.','Native non-US quote/share bridges remain incomplete where identified; no prices invented.','See final report for confirmed versus conditional candidates.'])
(ROOT/'outputs/screened_universe.json').write_text(json.dumps({'metadata':meta,'companies':companies},indent=2)+'\n')
sm=dict(research_date='2026-09-08',unique_source_records=len(sources),raw_source_records=len(source_raw),research_packages=sorted(set(s['package'] for s in source_raw)),modeled_companies=models,deduplication='Same non-market URL/publication date collapsed; aliases and raw records retained. Market captures sharing a documentation URL remain dated observations, never independent economic corroboration.')
(ROOT/'outputs/source_register.json').write_text(json.dumps({'metadata':sm,'sources':sources},indent=2)+'\n')
# Small summary tables; detailed investigations and sources are parallel prose entries.
text=f'Investigated universe as of September 8, 2026: **{len(companies)} distinct public companies**, across **{len(counts)} conservatively grouped economic chains**. **{len(models)} detailed intrinsic models** were completed. The {sum(map(len,allrows.values()))} investigation records include repeat investigations, retained in JSON and counted once here. There are {len(geo)} geographic labels, mixing incorporation, headquarters and listing jurisdictions; composite labels do not represent independent countries or diversified revenue exposures.\n\nEach entry includes an investigated role, dated primary source, financial mechanism and decision. Final model prices use the frozen [Massive capture](outputs/market_quotes.json); intermediate screening quotes embedded in historical decisions are dated research observations. For modeled companies, the final report and current input files supersede earlier narrative numbers.\n\n| Economic chain | Distinct companies |\n| --- | ---: |\n'
text+=''.join(f'| {k} | {v} |\n' for k,v in counts.items())
text+='\nGeographic labels: '+', '.join(f'{k} ({v})' for k,v in geo.items())+'.\n\n'
for i,c in enumerate(companies,1):
 s=c['role_source'];text+=f"{i}. **{c['company']} ({c['ticker']})** — {c['economic_chain']}; {c['jurisdiction_label']}. Role: {c['role']}. Source: [{s['publication_date']}; {s['section']}]({s['url']}). Mechanism: {c['financial_mechanism']}. Decision: {c['decision']}"
 if len(c['investigation_history'])>1:text+=' Earlier investigations retained: '+', '.join(c['research_packages'])+'.'
 text+='\n\n'
(ROOT/'SCREENED_UNIVERSE.md').write_text(text)
text=f'Source register as of September 8, 2026. **{len(sources)} source records** consolidate **{len(sm["research_packages"])} research packages** from {len(source_raw)} raw records, deduplicating matching documents by URL and publication date. Alias identifiers and original records are retained in [outputs/source_register.json](outputs/source_register.json). Repeated reporting is one underlying claim, not independent evidence. Dates refer to publication or filing where captured; month-only or undated pages remain explicitly incomplete.\n\nThe {len(models)} models have the following source coverage. Price observations, share counts, currency and balance dates are separate inputs; see the research packet for corporate-action and claim bridges.\n\n| Company | Source identifiers (full direct links below) | Research packet |\n| --- | --- | --- |\n'
for t,m in sorted(models.items()):text+=f'| {t} | '+', '.join(m['source_ids'])+f" | {m['package']} |\n"
text+='\nObserved facts, issuer forecasts, industry estimates and analyst assumptions are distinguished in model notes. Treasury September 4 official nominal rates are the AH29 source (an anchor, not a mechanical WACC). Company-authored demand reports and capacity targets are not independent customer evidence. Sources reproduced on mirrors are identified in their raw records.\n\n'
for s in sources:
 title=re.sub(r'\s+',' ',str(s['title']));aliases='; aliases '+', '.join(map(str,s['aliases'])) if s['aliases'] else ''
 text+=f"- **{s['id']}{aliases} — {s['publication_date']}.** [{title}]({s['url']}). Section: {s['section']}. {s['supports']}\n\n"
(ROOT/'SOURCE_REGISTER.md').write_text(text)
formatter='/code/.agents/skills/md-table-formatter/format-table.py'
for name in ['SCREENED_UNIVERSE.md','SOURCE_REGISTER.md']:
 p=ROOT/name;out=subprocess.check_output(['python',formatter,str(p)],text=True);p.write_text(out)
print(json.dumps({'companies':len(companies),'investigations':sum(map(len,allrows.values())),'chains':len(counts),'geographic_labels':len(geo),'models':len(models),'source_records':len(sources),'raw_sources':len(source_raw)},indent=2))
