# tidy_pc

A small Python tool that keeps a PC tidy by sorting files out of Downloads and Desktop into the standard folders (Pictures, Videos, Music, and so on).

**Status:** early development. Sorting by file extension works, with a dry-run mode.

## How it works

1. `rules.toml` lists which file extensions go to which folder.
2. `decide()` picks a destination for a file. It's pure logic and never touches the disk.
3. `sweep` runs over the watched folders (top level only, no recursion) and moves matching files with `safe_move()`, which never overwrites an existing file.

Files that no rule matches (PDFs, documents, anything unknown) are left where they are.

## Setup

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

## Usage

```bash
# Preview what would move; nothing changes on disk
python main.py sweep --dry-run --config rules.test.toml

# Actually move the files
python main.py sweep --config rules.test.toml
```

## Testing with fake files

`make_mock_pc.py` builds a messy fake PC in `mock_pc/` (it is gitignored), so you never experiment on real files.

```bash
python make_mock_pc.py    # rebuild the mess
python main.py sweep --dry-run --config rules.test.toml
python -m pytest -v       # run the unit tests
```

## Rules

Rules live in the TOML config. Each one maps extensions to a destination, relative to `sorted_root`. `{year}` is replaced with the year the file was last modified.

| Rule | Extensions | Destination |
|---|---|---|
| Installers | `.exe` `.msi` `.msix` `.appx` | `Downloads/Installers` |
| Pictures | `.png` `.jpg` `.jpeg` `.gif` `.webp` `.heic` `.svg` | `Pictures/{year}` |
| Videos | `.mp4` `.mkv` `.mov` `.avi` `.webm` | `Videos/{year}` |
| Audio | `.mp3` `.wav` `.flac` `.m4a` | `Music` |
| Code | `.py` `.js` `.ts` `.java` `.c` `.cpp` `.rs` `.go` `.ipynb` | `Documents/Dev/Code` |

## Project layout

```
config.py          load the TOML config into dataclasses
core.py            decide(), safe_move(), process(), sweep()
main.py            command-line interface
make_mock_pc.py    builds the fake PC for testing
rules.test.toml    config pointing at mock_pc/
tests/             pytest tests
```

## Planned

- Move journal and `undo`
- Expire old installers (move to a review folder, then the Recycle Bin)
- Empty-file and duplicate detection
- Background watcher that sorts files as they arrive
- Smarter sorting for PDFs and documents (lecture slides, tutorials, and so on)
- A `rules.toml` with real Windows paths, run via Task Scheduler