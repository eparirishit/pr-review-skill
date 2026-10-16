"""Report-only checks, not a review runtime or evidence of defect detection.

Each invalid mutation names the contract break this helper must reject.
Full nested type validation is owned by the schema and optional jsonschema.
"""
import copy
import json
from pathlib import Path
import unittest

try:
    import jsonschema
except ImportError:
    jsonschema = None

ROOT = Path(__file__).resolve().parent


def assert_report_integrity(report: dict) -> None:
    """Assert cross-field invariants; use the schema separately for nested types."""
    requirements, findings = report["requirements"], report["findings"]
    ids = [item["id"] for item in requirements + findings]
    assert len(ids) == len(set(ids)), "duplicate report ID"
    requirement_ids = {item["id"] for item in requirements}
    counts = {severity: 0 for severity in ("P0", "P1", "P2", "P3")}
    for finding in findings:
        counts[finding["severity"]] += 1
        links = finding.get("requirement_ids", [])
        assert len(links) == len(set(links)), "duplicate requirement link"
        assert set(links) <= requirement_ids, "unknown requirement link"
        location = finding.get("location")
        if location is not None:
            start, end = location["start_line"], location["end_line"]
            assert type(start) is int and type(end) is int, "non-integer line"
            assert 0 < start <= end, "invalid line bounds"
    summary = report["review"]["summary"]
    assert counts == summary["severity_counts"], "incorrect severity counts"
    scope = report["review"]["scope"]
    reviewed, total = scope["reviewed_files"], scope["total_changed_files"]
    assert type(reviewed) is int and reviewed >= 0, "invalid reviewed-file count"
    if total is not None:
        assert type(total) is int and reviewed <= total, "invalid total-file count"
    introduced = [f["severity"] for f in findings if f["introduced_by_change"] != "no"]
    if introduced:
        risk = {"P0": "critical", "P1": "high", "P2": "medium", "P3": "low"}[min(introduced)]
    else:
        risk = "incomplete" if scope["incomplete"] else "low"
    assert summary["risk"] == risk, "incorrect overall risk"
    validation = report["validation"]
    outcomes = [check["outcome"] for check in validation["checks"]]
    performed = any(outcome in ("passed", "failed") for outcome in outcomes)
    if "failed" in outcomes:
        status = "issues_found"
    elif validation["policy"] == "none" and not performed:
        status = "not_run"
    elif any(outcome in ("blocked", "not_run") for outcome in outcomes) or validation["evidence_incomplete"]:
        status = "incomplete"
    else:
        status = "passed" if performed else "not_run"
    assert validation["status"] == status, "incorrect validation derivation"
    assert summary["validation_status"] == status, "validation summaries disagree"
    by_id = {finding["id"]: finding for finding in findings}
    blockers = report["conclusion"]["blockers"]
    blocker_ids = [item["finding_id"] for item in blockers]
    assert len(blocker_ids) == len(set(blocker_ids)), "duplicate blocker"
    for blocker in blockers:
        assert blocker["finding_id"] in by_id, "unknown blocker"
        assert by_id[blocker["finding_id"]]["introduced_by_change"] != "no", "pre-existing blocker"
        assert blocker["rationale"].strip(), "missing blocker rationale"


class ReportIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / "reports/valid.json").read_text())

    def reject(self, report):
        with self.assertRaises(AssertionError):
            assert_report_integrity(report)

    def test_valid_report(self):
        assert_report_integrity(self.report)

    def test_invalid_example(self):
        self.reject(json.loads((ROOT / "reports/invalid-risk.json").read_text()))

    def test_unique_ids(self):
        self.report["findings"].append(copy.deepcopy(self.report["findings"][0]))
        self.reject(self.report)

    def test_severity_counts(self):
        self.report["review"]["summary"]["severity_counts"]["P2"] = 0
        self.reject(self.report)

    def test_requirement_links(self):
        self.report["findings"][0]["requirement_ids"] = ["missing"]
        self.reject(self.report)

    def test_location_bounds(self):
        for start, end in [(2, 1), (0, 2), (True, 2)]:
            with self.subTest(start=start, end=end):
                report = copy.deepcopy(self.report)
                report["findings"][0]["location"].update(start_line=start, end_line=end)
                self.reject(report)

    def test_reviewed_file_counts(self):
        self.report["review"]["scope"]["reviewed_files"] = 2
        self.reject(self.report)

    def test_risk_derivation(self):
        self.report["review"]["summary"]["risk"] = "low"
        self.reject(self.report)

    def test_risk_retained_with_incomplete_scope(self):
        self.report["review"]["scope"]["incomplete"] = True
        assert_report_integrity(self.report)

    def test_validation_derivation(self):
        self.report["validation"]["checks"][0]["outcome"] = "failed"
        self.reject(self.report)

    def test_mixed_failed_blocked_checks(self):
        self.report["validation"]["checks"][0]["outcome"] = "failed"
        self.report["validation"]["checks"].append({"name": "blocked", "kind": "runtime", "outcome": "blocked", "evidence": [], "reason": "unsafe"})
        self.set_validation("issues_found")
        assert_report_integrity(self.report)

    def set_validation(self, status):
        self.report["validation"]["status"] = status
        self.report["review"]["summary"]["validation_status"] = status

    def test_validation_summary_agrees(self):
        self.report["review"]["summary"]["validation_status"] = "not_run"
        self.reject(self.report)

    def test_disabled_zero_checks(self):
        self.report["validation"]["checks"] = []
        self.report["validation"]["evidence_incomplete"] = True
        self.set_validation("not_run")
        assert_report_integrity(self.report)
        self.set_validation("passed")
        self.reject(self.report)

    def test_auto_zero_checks(self):
        self.report["validation"].update(policy="auto", checks=[])
        self.set_validation("not_run")
        assert_report_integrity(self.report)

    def test_blocked_check_is_incomplete(self):
        self.report["validation"]["policy"] = "auto"
        self.report["validation"]["checks"][0].update(outcome="blocked", reason="unsafe")
        self.set_validation("incomplete")
        assert_report_integrity(self.report)

    def test_incomplete_evidence(self):
        self.report["validation"]["evidence_incomplete"] = True
        self.set_validation("incomplete")
        assert_report_integrity(self.report)

    def test_unknown_context(self):
        self.report["review"]["context"].update(story_source=None, requirements_available=False)
        self.report["review"]["scope"].update(base=None, head=None, total_changed_files=None)
        self.report["findings"][0].pop("location")
        assert_report_integrity(self.report)

    def test_preexisting_not_blocker(self):
        self.report["findings"][0]["introduced_by_change"] = "no"
        self.report["review"]["summary"]["risk"] = "low"
        self.reject(self.report)
        self.report["conclusion"]["blockers"] = []
        assert_report_integrity(self.report)

    def test_empty_findings_incomplete_scope(self):
        self.report["findings"] = []
        self.report["conclusion"]["blockers"] = []
        self.report["review"]["scope"]["incomplete"] = True
        self.report["review"]["summary"].update(risk="incomplete", severity_counts={"P0": 0, "P1": 0, "P2": 0, "P3": 0})
        assert_report_integrity(self.report)
        self.report["review"]["summary"]["risk"] = "low"
        self.reject(self.report)

    def test_blocker_reference(self):
        self.report["conclusion"]["blockers"][0]["finding_id"] = "missing"
        self.reject(self.report)

    def test_unique_blockers(self):
        self.report["conclusion"]["blockers"] *= 2
        self.reject(self.report)

    def test_negative_file_count(self):
        self.report["review"]["scope"]["reviewed_files"] = -1
        self.reject(self.report)

    @unittest.skipIf(jsonschema is None, "Optional jsonschema validator unavailable")
    def test_schema_contract(self):
        schema_path = ROOT.parent / "templates/review-report.schema.json"
        self.assertTrue(schema_path.is_file(), "JSON output contract not implemented")
        schema = json.loads(schema_path.read_text())
        validator = jsonschema.Draft202012Validator(schema)
        validator.check_schema(schema)
        validator.validate(self.report)
        mutations = [
            ("severity", "INFO"), ("confidence", "certain"),
            ("introduced_by_change", True), ("category", "style"),
        ]
        for key, value in mutations:
            with self.subTest(key=key):
                report = copy.deepcopy(self.report)
                report["findings"][0][key] = value
                self.assertFalse(validator.is_valid(report))
        report = copy.deepcopy(self.report)
        report["requirements"][0]["status"] = "done"
        self.assertFalse(validator.is_valid(report))
        report = copy.deepcopy(self.report)
        report["review"]["read_only"] = False
        self.assertFalse(validator.is_valid(report))
        report = copy.deepcopy(self.report)
        report["findings"][0]["location"] = None
        validator.validate(report)
        report["findings"][0].pop("title")
        self.assertFalse(validator.is_valid(report))


if __name__ == "__main__":
    unittest.main()
