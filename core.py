from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil

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

def unique_path(dest: Path) -> Path:
    """Return a unique path by adding a number if needed."""
    if not dest.exists():
        return dest
    i = 1
    while True:
        candidate = dest.with_name(f"{dest.stem}_{i}{dest.suffix}")
        if not candidate.exists():
            return candidate
        i += 1

def safe_move(src: Path, dest_dir: Path) -> Path:
    """Move 'src' to 'dest_dir', creating the folder if needed, and never overwriting."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = unique_path(dest_dir / src.name)
    shutil.move(src, target)
    return target

def process(path: Path, settings: Settings, dry_run: bool) -> Path | None:
    """Sort one file; Return where it went."""
    raise NotImplementedError

def sweep(settings: Settings, dry_run: bool) -> None:
    """One pass over every watched folder (top-level only)"""
    raise NotImplementedError