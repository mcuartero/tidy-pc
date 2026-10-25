from datetime import datetime
from pathlib import Path

from config import Rule, Settings
from core import decide

NOW = datetime(2026, 10, 25)

SETTINGS = Settings(
    watch=[],
    sorted_root=Path("/root"),
    review_root=Path("/root/_Review"),
    review_days=14,
    settle_seconds=5,
    rules=[
        Rule("Installers", [".exe", ".msi"], "Downloads/Installers", 30),
        Rule("Pictures", [".png", ".jpg"], "Pictures/{year}"),
    ],
)


def test_png_goes_to_pictures_by_year():
    d = decide(Path("photo.png"), NOW, SETTINGS)
    assert d.dest_dir == Path("/root/Pictures/2026")


def test_extension_match_ignores_case():
    assert decide(Path("PHOTO.PNG"), NOW, SETTINGS) is not None


def test_installer_keeps_its_expiry():
    d = decide(Path("setup.exe"), NOW, SETTINGS)
    assert d.rule.expire_days == 30


def test_unknown_extension_returns_none():
    assert decide(Path("lecture3.pdf"), NOW, SETTINGS) is None


def test_no_extension_returns_none():
    assert decide(Path("README"), NOW, SETTINGS) is None