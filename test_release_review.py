import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from review import compare, main


class ReleaseReviewTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.before = self.directory / "approved.csv"
        self.after = self.directory / "proposal.csv"

    def snapshot(self, path, pairs):
        with path.open("w", newline="", encoding="utf-8") as dest:
            writer = csv.writer(dest)
            writer.writerow(["sku", "value"])
            writer.writerows(pairs)

    def run_review(self, name, prior=None):
        path = self.directory / (name + ".json")
        compare(self.before, self.after, fields=["value"], review_out=path, prior_review=prior)
        return path, json.loads(path.read_text())

    def test_exact_keys_order_values_and_decisions(self):
        rows = [("01", "a"), ("1", "a"), (" 01", "a"), ("01 ", "a")]
        self.snapshot(self.before, rows)
        self.snapshot(self.after, [(sku, "b") for sku, _ in rows] + [("new", "x")])
        first, saved = self.run_review("first")
        for item in saved["items"]:
            item["decision"] = "note " + item["identifier"]
        first.write_text(json.dumps(saved))
        self.snapshot(self.before, rows[::-1])
        self.snapshot(self.after, [("01 ", "a"), (" 01", "different\nvalue"), ("1", "b"), ("01", "b")])
        second, current = self.run_review("second", first)
        by_key = {x["identifier"]: x for x in current["items"]}
        self.assertEqual((by_key["01"]["decision"], by_key["01"]["after_records"]), ("note 01", [4]))
        self.assertEqual(by_key["1"]["decision"], "note 1")
        self.assertEqual((by_key[" 01"]["status"], by_key[" 01"]["decision"]), ("changed", ""))
        self.assertEqual(by_key[" 01"]["previous_decision"], "note  01")
        self.assertEqual(by_key["01 "]["reason"], "matches_approved")
        self.assertEqual(by_key["new"]["reason"], "absent_from_both")
        self.snapshot(self.after, [("01 ", "b"), *rows[:-1]])
        _, third = self.run_review("third", second)
        reopened = next(x for x in third["items"] if x["identifier"] == "01 ")
        self.assertEqual((reopened["status"], reopened["decision"]), ("reopened", ""))

    def test_ambiguous_or_missing_identity(self):
        self.snapshot(self.before, [("A", "a"), ("B", "b")])
        self.snapshot(self.after, [("A", "x"), ("B", "y"), ("EXTRA", "z")])
        first, prior = self.run_review("first")
        for item in prior["items"]:
            item["decision"] = "previous note"
        first.write_text(json.dumps(prior))
        self.snapshot(self.after, [("A", "a"), ("A", "x"), ("  ", "y")])
        second, report = self.run_review("second", first)
        cases = {item["identifier"]: item for item in report["items"]}
        self.assertEqual((cases["A"]["reason"], cases["A"]["after_records"]), ("ambiguous_key", [1, 2]))
        self.assertEqual((cases["B"]["status"], cases["B"]["reason"]), ("changed", "removed"))
        self.assertEqual((cases["EXTRA"]["status"], cases["EXTRA"]["reason"]), ("identity_unresolved", "identity_not_confirmed"))
        self.assertTrue(all(not x["decision"] for x in cases.values()))
        self.assertEqual(report["unidentified_rows"][0]["after_records"], [3])
        self.snapshot(self.after, [("A", "x"), ("B", "b")])
        _, report = self.run_review("third", second)
        cases = {item["identifier"]: item for item in report["items"]}
        self.assertEqual((cases["A"]["status"], cases["A"]["decision"]), ("new", ""))
        self.assertEqual(cases["EXTRA"]["reason"], "absent_from_both")

    def test_scope_validation_and_safe_output(self):
        self.snapshot(self.before, [("A", "x")])
        self.snapshot(self.after, [("A", "z")])
        first, original = self.run_review("first")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_review("first", first)
        self.assertEqual(original, json.loads(first.read_text()))
        self.snapshot(self.before, [("A", "y")])
        with self.assertRaisesRegex(ValueError, "same format"):
            self.run_review("other", first)
        self.snapshot(self.before, [("A", "x")])
        original["items"].append(original["items"][0])
        first.write_text(json.dumps(original))
        with self.assertRaisesRegex(ValueError, "repeated"):
            self.run_review("other", first)
        self.assertFalse((self.directory / "other.json").exists())

    def test_documented_oro_sequence_and_cli_privacy(self):
        sample = Path(__file__).parent / "examples" / "orocommerce-product-units"
        fields = ["primaryUnitPrecision.sell", "additionalUnitPrecisions:0:precision",
                  "additionalUnitPrecisions:0:conversionRate", "additionalUnitPrecisions:0:sell"]
        args = [str(sample / "approved-units.csv")]
        options = [arg for name in fields for arg in ("--field", name)]
        previous = None
        for i, (proposal, expected) in enumerate([
            ("proposed-units.csv", {"new": 4}),
            ("reviewed-units.csv", {"unchanged": 1, "closed": 3}),
            ("next-proposal-units.csv", {"changed": 1, "new": 1, "reopened": 1, "still_closed": 2}),
        ]):
            out = self.directory / (str(i) + ".json")
            prior = ["--prior-review", str(previous)] if previous else []
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main([*args, str(sample / proposal), *options, "--review-out", str(out),
                             "--fail-on-change", *prior])
            self.assertEqual(code, 1)
            self.assertNotIn("RING-08", stdout.getvalue())
            saved = json.loads(out.read_text())
            self.assertEqual(saved["counts"], expected)
            ring = next(item for item in saved["items"] if item["identifier"] == "RING-08")
            if i == 0:
                ring["decision"] = "Keep ten per set per packing revision A"
                out.write_text(json.dumps(saved))
            elif i == 1:
                self.assertEqual(ring["decision"], "Keep ten per set per packing revision A")
            else:
                self.assertEqual((ring["decision"], ring["previous_decision"]), ("", "Keep ten per set per packing revision A"))
            previous = out
