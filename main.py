import argparse
from email import parser
from pathlib import Path

from config import load_settings
from core import sweep

def main():
    parser = argparse.ArgumentParser(prog="tidy_pc")
    parser.add_argument("command", choices=["sweep"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--config", type=Path, default="rules.toml")
    args = parser.parse_args()

    if args.command == "sweep":
        settings = load_settings(args.config)
        sweep(settings, dry_run=args.dry_run)

if __name__ == "__main__":
    main()

