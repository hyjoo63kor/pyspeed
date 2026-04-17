from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


RESULTS_JSON = Path("results/accelerator_compare.json")
RESULTS_TEXT = Path("results/accelerator_compare.txt")
DEFAULT_DLL = Path("native/build/pyspeed_native.dll")
CASES = ["ctypes", "cdll", "numpy", "numba", "numba_cold"]


def run_case(python_exe: str, case_name: str) -> dict:
    env = os.environ.copy()
    if case_name == "cdll":
        env["PYSPEED_NATIVE_DLL"] = str(DEFAULT_DLL)

    proc = subprocess.run(
        [python_exe, "-m", "pyspeed", case_name, "--profile", "quick", "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return json.loads(proc.stdout)[0]


def render_text(payload: dict) -> str:
    lines = [
        f"generated_at  : {payload['generated_at']}",
        f"profile       : {payload['profile']}",
        "",
        "Accelerator comparison:",
        "",
    ]
    for item in payload["results"]:
        lines.append(f"[{item['case']}]")
        lines.append(f"description   : {item['description']}")
        lines.append(f"timer         : {item['timer']}")
        lines.append(f"baseline best : {item['baseline_best']:.6f}s")
        lines.append(f"optimized best: {item['optimized_best']:.6f}s")
        lines.append(f"speedup       : {item['speedup']:.2f}x")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    python_exe = argv[0] if argv else r".\.venv\Scripts\python.exe"

    results = [run_case(python_exe, case_name) for case_name in CASES]
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "profile": "quick",
        "results": results,
    }

    RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    RESULTS_TEXT.write_text(render_text(payload), encoding="utf-8")

    print(render_text(payload))
    print(f"Saved accelerator comparison to {RESULTS_TEXT}")
    print(f"Saved accelerator comparison JSON to {RESULTS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
