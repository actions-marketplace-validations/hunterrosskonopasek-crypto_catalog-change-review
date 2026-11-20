import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from review import compare, main


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.left = Path(tmp.name, "before.csv")
        self.right = Path(tmp.name, "after.csv")

    def files(self, a, b):
        for path, rows in ((self.left, a), (self.right, b)):
            path.write_text("sku,selling_unit,pack_qty\n" + rows, encoding="utf-8")

    def test_same_and_leading_zero(self):
        self.files("01,each,1\n1,case,2", "1,case,2\n01,each,1")
        self.assertEqual(compare(self.left, self.right)["counts"], {})

    def test_demo_snapshot(self):
        base = Path(__file__).parent / "examples"
        report = compare(base/"before.csv", base/"after.csv")
        self.assertEqual(report["counts"], {"added":1, "ambiguous_key":1, "changed":1, "removed":1})
        self.assertEqual(report["findings"][0]["changed_columns"], ["pack_qty"])
        self.assertEqual(report["findings"][1]["after_records"], [3, 4])
        self.assertNotIn("A-09", str(report))

    def test_blanks_and_embedded_newline(self):
        self.files(',"each\nunit",1\nK,each,1', 'K,each,1\n   ,each,1')
        self.assertEqual(compare(self.left, self.right)["counts"], {"missing_key":2})

    def test_multiple_changes_and_dynamic_fields(self):
        self.files("K,each,1", "K,case,5")
        self.assertEqual(compare(self.left, self.right)["findings"][0]["changed_columns"], ["selling_unit","pack_qty"])
        self.assertEqual(compare(self.left, self.right, fields=["pack_qty"])["findings"][0]["changed_columns"], ["pack_qty"])

    def test_bad_csv_is_error(self):
        self.files("K,case,6", "K,each")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([str(self.left), str(self.right)]), 2)

    def test_bad_headers_and_field_specs(self):
        self.files("K,case,6", "K,case,6")
        for fields in (["sku"], ["selling_unit","selling_unit"], ["unavailable"]):
            with self.assertRaises(ValueError):
                compare(self.left, self.right, fields=fields)
        self.left.write_text("sku,sku,pack_qty\nA,A,6", encoding="utf-8")
        with self.assertRaises(ValueError):
            compare(self.left, self.right)

    def test_exit_codes(self):
        self.files("K,case,6", "K,case,8")
        args = [str(self.left), str(self.right)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(args), 0)
            self.assertEqual(main(["--fail-on-change", "--", *args]), 1)
            self.files("K,case,6", "K,case,6")
            self.assertEqual(main(["--fail-on-change", "--", *args]), 0)


if __name__ == "__main__":
    unittest.main()
