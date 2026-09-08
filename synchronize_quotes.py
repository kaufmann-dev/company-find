"""Apply the frozen authoritative Massive minute quotes to all completed models."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
q=json.loads((ROOT/'outputs/market_quotes.json').read_text())
for p in ROOT.glob('research/*/inputs.json'):
 data=json.loads(p.read_text())
 for c in data:
  c.update(price=q[c['ticker']]['price'],price_timestamp=q[c['ticker']]['price_timestamp'],quote_field='Massive min.c; minute start min.t; delayed snapshot captured2026-09-08T15:54:39Z')
 p.write_text(json.dumps(data,indent=2)+'\n')
