"""Rebuild mock_pc/ with a realistic mess. Run: python make_mock_pc.py"""
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "mock_pc"
JUNE_2025 = datetime(2025, 6, 1).timestamp()


def make(rel, content="x", mtime=None):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def days_ago(n):
    return time.time() - n * 86400


def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    for d in ("Downloads", "Desktop", "Documents", "Pictures", "Videos", "Music"):
        (ROOT / d).mkdir(parents=True)

    # --- sortable by extension ---
    make("Downloads/photo.jpg", "new", JUNE_2025)
    make("Pictures/2025/photo.jpg", "already here", JUNE_2025)   # name collision
    make("Downloads/Screenshot 2026-10-25.png")
    make("Downloads/clip.mp4")
    make("Downloads/song.mp3")
    make("Downloads/script.py")
    make("Downloads/setup.exe")
    make("Desktop/meme.png")
    make("Desktop/Untitled.jpg")

    # --- left for the smart stage ---
    make("Downloads/lecture3.pdf")
    make("Downloads/09.pdf")
    make("Downloads/notes.txt")
    make("Downloads/report.docx")
    make("Downloads/mystery.xyz")
    make("Downloads/README")

    # --- no rule matches these, so they must stay put ---
    make("Desktop/shortcut.lnk")
    make("Desktop/desktop.ini")
    make("Downloads/movie.crdownload")
    make("Downloads/~$report.docx")

    # --- later steps (expiry, review) ---
    make("Downloads/Installers/old_installer.exe", mtime=days_ago(40))
    make("Downloads/empty.txt", content="")

    # --- subfolder contents must stay untouched ---
    make("Downloads/Some Folder/inner.png")

    print(f"Rebuilt {ROOT}")


if __name__ == "__main__":
    main()