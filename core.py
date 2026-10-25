from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from config import Rule, Settings

@dataclass(frozen=True)
class Decision:
    rule: Rule
    dest_dir: Path

def decide(path: Path, mtime: datetime, settings: Settings) -> Decision | None:
    """Decide where 'path' shoudl go"""
    ext = path.suffix.lower()
    for rule in settings.rules:
        if ext in rule.extensions:
            dest = rule.dest.format(year=mtime.year, month=f"{mtime.month:02d}")
            return Decision(rule=rule, dest_dir=settings.sorted_root / dest)
    return None