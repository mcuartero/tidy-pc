"""Load the TOML config into immutable dataclasses."""
import sys
import tomllib
from dataclasses import dataclass, fields, is_dataclass
from pathlib import Path
from pprint import pprint

# with open("rules.test.toml", "rb") as f:
#     raw = tomllib.load(f)
# print(raw)

@dataclass(frozen=True)
class Rule:
    """A single rule in the config."""
    name: str
    extensions: list[str]
    dest: str
    expire_days: int | None = None

@dataclass(frozen=True)
class Settings:
    """The settings in the config."""
    watch: list[Path]
    sorted_root: Path
    review_root: Path
    review_days: int
    settle_seconds: int
    rules: list[Rule]

def load_settings(path):
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    s = raw["settings"]
    return Settings(
        watch=[Path(p) for p in s["watch"]],
        sorted_root=Path(s["sorted_root"]),
        review_root=Path(s["review_root"]),
        review_days=s["review_days"],
        settle_seconds=s["settle_seconds"],
        rules=[Rule(r["name"], r["extensions"], r["dest"], r.get("expire_days")) for r in raw["rules"]]
    )

def show(obj, indent=0):
    pad = "  " * indent
    if is_dataclass(obj):
        print(f"{pad}{type(obj).__name__}")
        for f in fields(obj):
            value = getattr(obj, f.name)
            if is_dataclass(value) or (isinstance(value, list) and value and is_dataclass(value[0])):
                print(f"{pad}  {f.name}:")
                show(value, indent + 2) if is_dataclass(value) else [show(v, indent + 2) for v in value]
            else:
                print(f"{pad}  {f.name}: {value}")
    else:
        print(f"{pad}{obj}")

if __name__ == "__main__":
    show(load_settings(Path("rules.test.toml")))
