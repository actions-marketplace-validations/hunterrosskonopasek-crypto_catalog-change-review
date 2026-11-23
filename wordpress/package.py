"""Build the WordPress plugin from the existing, self-contained catalog checker."""

from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SLUG = "hwc-catalog-review"


def build():
    sources = {
        "hwc-catalog-review.php": HERE / "hwc-catalog-review.php",
        "catalog-review.html": ROOT / "free-tools/25-sku-diagnostic/HWC-Free-25-SKU-Diagnostic.html",
        "LICENSE": ROOT / "LICENSE",
    }
    with ZipFile(HERE / (SLUG + ".zip"), "w") as archive:
        for name, source in sources.items():
            entry = ZipInfo(f"{SLUG}/{name}", (2026, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            # Git may check out CRLF on Windows. Use the same bytes on every OS.
            archive.writestr(entry, source.read_text(encoding="utf-8").encode("utf-8"), ZIP_STORED)


if __name__ == "__main__":
    build()
