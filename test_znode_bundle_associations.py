import csv
from io import StringIO
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

EXAMPLE = Path(__file__).parent / "examples" / "znode-bundle-associations"


def run(*args):
    return subprocess.run([sys.executable, str(EXAMPLE / "preflight.py"), *map(str, args)],
                          capture_output=True, text=True)


class BundleReviewTests(unittest.TestCase):
    def test_public_worksheet_is_reproducible(self):
        result = run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (EXAMPLE / "expected-review.csv").read_text())
        rows = list(csv.DictReader(StringIO(result.stdout)))
        self.assertEqual([r["record"] for r in rows if r["decision"] == "MATCH"], ["1", "3"])
        self.assertEqual(rows[2]["ChildSKU"], "00017")

    def test_exact_quantity_and_reference_coverage(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "proposal.csv"
            path.write_text("ParentSku,ChildSKU,DisplayOrder,IsDefault,Quantity\n"
                            "KIT-710,GSK-004,2,0,4.0\n"
                            "UNKNOWN,GSK-004,1,0,\n"
                            "KIT-710,=BAD,1,0,1_0\n", encoding="utf-8")
            result = run("--proposed", path)
            self.assertEqual(result.returncode, 0, result.stderr)
            corrected, unknown, malformed = csv.DictReader(StringIO(result.stdout))
            self.assertEqual(corrected["decision"], "MATCH")
            self.assertIn("Parent SKU absent", unknown["reason"])
            self.assertNotIn("Missing bundle component quantity", unknown["reason"])
            self.assertEqual(malformed["ChildSKU"], "'=BAD")
            self.assertIn("Review component quantity", malformed["reason"])

    def test_reference_ambiguity_stops_the_report(self):
        with TemporaryDirectory() as temp:
            bill = Path(temp) / "bill.csv"
            bill.write_text("ParentSku,ChildSKU,ApprovedQuantity\n"
                            "KIT-710,GSK-004,4\nKIT-710,GSK-004,6\n", encoding="utf-8")
            result = run("--bom", bill)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("repeated reference key", result.stderr)
