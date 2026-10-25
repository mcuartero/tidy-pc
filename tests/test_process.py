import os
from datetime import datetime

import pytest

from config import Rule, Settings
from core import process, sweep


def make_settings(tmp_path):
    return Settings(
        watch=[tmp_path / "dl"],
        sorted_root=tmp_path / "root",
        review_root=tmp_path / "root" / "_Review",
        review_days=14,
        settle_seconds=5,
        rules=[
            Rule("Installers", [".exe"], "Downloads/Installers", 30),
            Rule("Pictures", [".png"], "Pictures/{year}"),
        ],
    )


def make_file(folder, name, year=2026):
    folder.mkdir(parents=True, exist_ok=True)
    f = folder / name
    f.write_text("x")
    ts = datetime(year, 6, 1).timestamp()
    os.utime(f, (ts, ts))
    return f


# ---------- process ----------

def test_process_moves_matching_file(tmp_path):
    s = make_settings(tmp_path)
    f = make_file(tmp_path / "dl", "a.png")
    dest = process(f, s, dry_run=False)
    assert dest == tmp_path / "root" / "Pictures" / "2026" / "a.png"
    assert dest.exists() and not f.exists()


def test_process_dry_run_changes_nothing(tmp_path):
    s = make_settings(tmp_path)
    f = make_file(tmp_path / "dl", "a.png")
    dest = process(f, s, dry_run=True)
    assert dest == tmp_path / "root" / "Pictures" / "2026" / "a.png"
    assert f.exists() and not dest.exists()


def test_process_leaves_unmatched_files(tmp_path):
    s = make_settings(tmp_path)
    f = make_file(tmp_path / "dl", "lecture3.pdf")
    assert process(f, s, dry_run=False) is None
    assert f.exists()


@pytest.mark.parametrize("name", ["shortcut.lnk", "desktop.ini", "~$report.docx", "movie.crdownload"])
def test_process_ignores_files_no_rule_matches(tmp_path, name):
    s = make_settings(tmp_path)
    f = make_file(tmp_path / "dl", name)
    assert process(f, s, dry_run=False) is None
    assert f.exists()


def test_process_ignores_directories(tmp_path):
    s = make_settings(tmp_path)
    folder = tmp_path / "dl" / "holiday.png"      # a folder whose name looks like a picture
    folder.mkdir(parents=True)
    assert process(folder, s, dry_run=False) is None
    assert folder.exists()


# ---------- sweep ----------

def test_sweep_only_touches_top_level(tmp_path):
    s = make_settings(tmp_path)
    make_file(tmp_path / "dl", "a.png")
    inner = make_file(tmp_path / "dl" / "Installers", "setup.exe")
    sweep(s, dry_run=False)
    assert (tmp_path / "root" / "Pictures" / "2026" / "a.png").exists()
    assert inner.exists()          # files in subfolders are left alone


def test_sweep_survives_missing_watch_folder(tmp_path):
    s = make_settings(tmp_path)    # tmp_path/"dl" was never created
    sweep(s, dry_run=False)