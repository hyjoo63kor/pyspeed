from __future__ import annotations

import json
import sys
from pathlib import Path


def categorize(speedup: float) -> str:
    if speedup >= 10.0:
        return "big win"
    if speedup >= 2.0:
        return "solid win"
    if speedup >= 1.1:
        return "small win"
    if speedup >= 0.9:
        return "mixed"
    return "loss"


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    path = Path(argv[0]) if argv else Path("results/latest.json")

    if not path.exists():
        print(f"Result file not found: {path}")
        return 1

    data = json.loads(path.read_text(encoding="utf-8"))
    if not data:
        print("No benchmark results found.")
        return 1

    ranked = sorted(data, key=lambda item: item["speedup"], reverse=True)
    print(f"Summary for {path}")
    print("")

    for item in ranked:
        print(f"{item['case']:12} {item['speedup']:8.2f}x  {categorize(item['speedup'])}")

    wins = [item for item in ranked if item["speedup"] > 1.0]
    losses = [item for item in ranked if item["speedup"] < 1.0]
    mixed = [item for item in ranked if item["speedup"] == 1.0]

    print("")
    print(f"wins   : {len(wins)}")
    print(f"losses : {len(losses)}")
    print(f"flat   : {len(mixed)}")

    if ranked:
        print("")
        print(f"top    : {ranked[0]['case']} ({ranked[0]['speedup']:.2f}x)")
        print(f"bottom : {ranked[-1]['case']} ({ranked[-1]['speedup']:.2f}x)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
