import tempfile
import unittest
from pathlib import Path
from flaky_test_detective.junit import analyze_files, normalize_identifier


XML1="""<testsuite name="suite"><testcase classname="A" name="flaky"><failure/></testcase><testcase classname="A" name="stable"/></testsuite>"""
XML2="""<testsuite name="suite"><testcase classname="A" name="flaky"/><testcase classname="A" name="stable"/><testcase classname="A" name="skip"><skipped/></testcase></testsuite>"""


class JUnitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.p1=Path(self.tmp.name)/"run1.xml"; self.p2=Path(self.tmp.name)/"run2.xml"
        self.p1.write_text(XML1,encoding="utf-8"); self.p2.write_text(XML2,encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_mixed_results_are_intermittent(self):
        result=analyze_files([self.p1,self.p2])
        flaky=[r for r in result["intermittent"] if r["test"]=="A.flaky"][0]
        self.assertEqual(flaky["pass"],1); self.assertEqual(flaky["fail"],1)
        self.assertEqual(flaky["flake_rate"],0.5)

    def test_no_flaky_for_consistent_status(self):
        result=analyze_files([self.p1,self.p2])
        stable=[r for r in result["totals"].items() if r[0]=="A.stable"][0][1]
        self.assertEqual(stable["pass"],2); self.assertEqual(stable["fail"],0)

    def test_normalize_retry_suffix(self):
        self.assertEqual(normalize_identifier(" pkg.Case "," test retry_2 "), "pkg.Case.test")

    def test_skip_excluded_from_observed_denominator(self):
        result=analyze_files([self.p1,self.p2])
        skip=result["totals"]["A.skip"]
        self.assertEqual(skip["skipped"],1); self.assertEqual(skip["runs"],1)

    def test_pass_and_fail_across_runs_not_within(self):
        result=analyze_files([self.p1,self.p2])
        self.assertIn("A.flaky", [r["test"] for r in result["intermittent"]])

if __name__=="__main__":
    unittest.main()
