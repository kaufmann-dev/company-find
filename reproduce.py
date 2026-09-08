"""Recalculate the frozen September8 research; Python standard library only."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
for script in ['synchronize_quotes.py','model.py','research/aviation_health/model.py','research/connectivity/additional_checks.py','research/deep_global/additional_checks.py','research/deep_global/finalize.py','research/deep_cyclicals/write_research.py','research/deep_neglected/extra_model.py','research/deep_cyclicals/consolidate_appendices.py','check_models.py','render_report.py','render_deep_report.py','refresh_comparison_outputs.py','research/deep_global/finv_floor.py']:
    result=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:
        print(result.stdout+result.stderr)
        raise SystemExit(result.returncode)
    print('PASS',script)
