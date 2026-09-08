"""Keep local comparison artifacts aligned with the consolidated frozen valuation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rs={r['ticker']:r for r in json.loads((ROOT/'outputs/all_valuations.json').read_text())}
for filename,tickers,as_list in [
 ('research/connectivity/valuation_results.json',['CMCSA'],True),
 ('research/power_water/valuation_results.json',['POWL','MWA'],True),
 ('research/aviation_health/iqv_valuation.json',['IQV'],False),
 ('research/deep_consumer/valuation_results.json',['DECK'],False)]:
 data=[rs[t] for t in tickers];(ROOT/filename).write_text(json.dumps(data if as_list else data[0],indent=2)+'\n')
