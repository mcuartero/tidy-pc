from core import safe_move, unique_path


# ---------- unique_path ----------

def test_unique_path_unchanged_when_free(tmp_path):
    p = tmp_path / "a.txt"
    assert unique_path(p) == p


def test_unique_path_adds_number_when_taken(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("x")
    assert unique_path(p) == tmp_path / "a_1.txt"


def test_unique_path_skips_numbers_already_taken(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "a_1.txt").write_text("x")
    assert unique_path(tmp_path / "a.txt") == tmp_path / "a_2.txt"


def test_unique_path_without_extension(tmp_path):
    (tmp_path / "README").write_text("x")
    assert unique_path(tmp_path / "README") == tmp_path / "README_1"


# ---------- safe_move ----------

def test_safe_move_creates_missing_folder(tmp_path):
    src = tmp_path / "photo.png"
    src.write_text("pixels")
    dest_dir = tmp_path / "Pictures" / "2026"

    final = safe_move(src, dest_dir)

    assert final == dest_dir / "photo.png"
    assert final.read_text() == "pixels"


def test_safe_move_removes_source(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("x")
    safe_move(src, tmp_path / "out")
    assert not src.exists()


def test_safe_move_never_overwrites(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "a.txt").write_text("original")
    src = tmp_path / "a.txt"
    src.write_text("newcomer")

    final = safe_move(src, out)

    assert (out / "a.txt").read_text() == "original"
    assert final == out / "a_1.txt"
    assert final.read_text() == "newcomer"