"""Behavioral regressions for preservation, planning honesty and path safety."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills/scrum-skill/scripts/init_workspace.py"
spec = importlib.util.spec_from_file_location("scrum_workspace", SCRIPT)
workspace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workspace)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def plan(self, **changes):
        params = dict(root=self.root, name="inventory", goal="Staff can inspect stock",
                      roles=["engineering", "qa"], start=date(2026, 10, 19), sprint_days=14)
        params.update(changes)
        return workspace.plan(**params)

    def test_initial_records_are_proposed_and_no_events_claimed(self):
        workspace.apply(self.plan())
        state = json.loads((self.root / ".scrum/workspace.json").read_text())
        self.assertEqual(state["state"], "proposed")
        self.assertEqual(state["forecast_end"], "2026-11-01")
        self.assertEqual(state["specialists"], ["engineering", "qa"])
        self.assertEqual(state["skill_version"], "0.1.0")
        self.assertTrue((self.root / ".scrum/sprints/SPRINT-01-RETROSPECTIVE.md").is_file())
        self.assertTrue((self.root / ".scrum/handoffs/LATEST.md").is_file())

    def test_existing_instructions_preserved_byte_for_byte(self):
        original = b"# Existing policy\r\nDo not publish plans.\r\n"
        (self.root / "AGENTS.md").write_bytes(original)
        workspace.apply(self.plan())
        result = (self.root / "AGENTS.md").read_bytes()
        self.assertTrue(result.startswith(original))
        self.assertEqual(result.count(workspace.START.encode()), 1)

    def test_repeat_has_no_writes_and_keeps_working_decisions(self):
        workspace.apply(self.plan())
        record = self.root / ".scrum/DECISIONS.md"
        record.write_text("An actual user decision.\n", encoding="utf-8")
        self.assertEqual(self.plan(), {})
        self.assertEqual(record.read_text(), "An actual user decision.\n")

    def test_conflicting_project_identity_rejected(self):
        workspace.apply(self.plan())
        with self.assertRaisesRegex(ValueError, "different project"):
            self.plan(name="another-project")

    def test_repair_uses_current_project_decisions_not_bootstrap_defaults(self):
        workspace.apply(self.plan())
        manifest = self.root / ".scrum/workspace.json"
        state = json.loads(manifest.read_text())
        state.update(product_goal="Coordinate neighborhood planting", specialists=["horticulture"],
                     sprint_days=7, forecast_end="2026-10-25")
        manifest.write_text(json.dumps(state), encoding="utf-8")
        (self.root / ".scrum/TEAM.md").unlink()
        (self.root / ".scrum/sprints/SPRINT-01.md").unlink()
        workspace.apply(self.plan())
        self.assertEqual(json.loads(manifest.read_text()), state)
        self.assertIn("horticulture", (self.root / ".scrum/TEAM.md").read_text())
        self.assertIn("2026-10-25", (self.root / ".scrum/sprints/SPRINT-01.md").read_text())
        self.assertTrue((self.root / ".scrum/roles/horticulture.md").is_file())

    def test_generalist_and_custom_domain_do_not_require_counsel(self):
        workspace.apply(self.plan(roles=[]))
        state = json.loads((self.root / ".scrum/workspace.json").read_text())
        self.assertEqual(state["specialists"], [])
        self.assertFalse((self.root / ".scrum/roles").exists())
        self.assertEqual(workspace.specialists("research,qa"), ["research", "qa"])

    def test_invalid_roles_and_duplicates_fail(self):
        for raw in ("qa,qa", "../../outside", "research,", "Domain Expert"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                workspace.specialists(raw)

    def test_file_collision_is_detected_before_any_writes(self):
        (self.root / "CLAUDE.md").mkdir()
        with self.assertRaises(ValueError):
            self.plan()
        self.assertFalse((self.root / ".scrum").exists())

    def test_parent_collision_is_detected_before_writes(self):
        (self.root / ".scrum").mkdir()
        (self.root / ".scrum/sprints").write_text("not a directory")
        with self.assertRaises(ValueError):
            self.plan()
        self.assertFalse((self.root / ".scrum/workspace.json").exists())

    def test_malformed_markers_fail_without_overwriting(self):
        policy = self.root / "AGENTS.md"
        policy.write_text("Existing\n" + workspace.START)
        with self.assertRaisesRegex(ValueError, "malformed"):
            self.plan()
        self.assertFalse((self.root / ".scrum").exists())
        self.assertEqual(policy.read_text(), "Existing\n" + workspace.START)

    def test_symlink_escape_fails_before_writes(self):
        with tempfile.TemporaryDirectory() as outside:
            try:
                (self.root / ".scrum").symlink_to(outside, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symlink creation unsupported: {error}")
            with self.assertRaisesRegex(ValueError, "escape|symlink"):
                self.plan()
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_cadence_cannot_exceed_one_calendar_month(self):
        with self.assertRaisesRegex(ValueError, "calendar month"):
            self.plan(start=date(2027, 2, 1), sprint_days=31)
        with self.assertRaises(ValueError):
            self.plan(sprint_days=0)

    def test_dry_run_cli_never_writes(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root),
                                 "--name", "inventory", "--goal", "Track stock", "--dry-run"],
                                capture_output=True, text=True, check=True)
        self.assertIn("Would write", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
