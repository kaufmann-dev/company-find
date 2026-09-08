"""Recalculate the frozen September8 research; Python standard library only."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
for script in ['model.py','research/aviation_health/model.py','research/connectivity/additional_checks.py','check_models.py','render_report.py']:
    result=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:
        print(result.stdout+result.stderr)
        raise SystemExit(result.returncode)
    print('PASS',script)
