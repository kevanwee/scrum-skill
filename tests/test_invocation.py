import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "skills/scrum-skill/scripts/route_invocation.py"
spec = importlib.util.spec_from_file_location("invocation", path)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


def run_cli(*arguments: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *arguments],
        input=input_text,
        capture_output=True,
        text=True,
    )


class InvocationTests(unittest.TestCase):
    def test_bare_call_is_wizard_without_actions(self):
        result = router.resolve("")
        self.assertEqual(result["mode"], "wizard")
        self.assertFalse(result["executes_actions"])

    def test_dashboard_preserves_explicit_input_without_exporting(self):
        result = router.resolve('dashboard --target ".scrum/metrics.json"')
        self.assertEqual(result["mode"], "dashboard")
        self.assertEqual(result["options"]["target"], ".scrum/metrics.json")
        self.assertFalse(result["executes_actions"])

    def test_role_review_and_alias_preserve_target(self):
        result = router.resolve('role legal review --target "docs/platform choices"')
        self.assertEqual((result["role"], result["mode"]), ("legal-counsel", "review"))
        self.assertEqual(result["options"]["target"], "docs/platform choices")
        self.assertEqual(router.resolve("role ux plan")["role"], "design")

    def test_goal_roles_and_shell_text_remain_data(self):
        result = router.resolve('setup --goal "$(whoami); harmless text" --roles engineering,qa')
        self.assertEqual(result["options"]["goal"], "$(whoami); harmless text")
        self.assertEqual(result["options"]["roles"], ["engineering", "qa"])

    def test_bad_explicit_requests_fail(self):
        for request in ["role", "role enginer review", "role design deploy", "plna",
                        "plan --unknown x", "setup --roles qa,qa", "setup --roles ../private",
                        'setup --goal "unterminated']:
            with self.subTest(request=request), self.assertRaises(ValueError):
                router.resolve(request)

    def test_role_only_opens_scoped_wizard(self):
        self.assertEqual(router.resolve("role security")["mode"], "wizard")

    def test_natural_language_and_custom_profile(self):
        self.assertTrue(router.resolve("Resume from the latest handoff")["intent_resolution_required"])
        self.assertEqual(router.resolve("role domain-reviewer plan --profile roles/garden.md")["options"]["profile"], "roles/garden.md")

    def test_windows_paths_are_literal_with_or_without_grouping_quotes(self):
        for request in [r'plan --target C:\work\garden\ci.yml',
                        r'plan --target "C:\work\my garden\ci.yml"']:
            result = router.resolve(request)
            expected = r"C:\work\my garden\ci.yml" if '"' in request else r"C:\work\garden\ci.yml"
            self.assertEqual(result["options"]["target"], expected)

    def test_explicit_typos_abbreviations_and_empty_roles_fail(self):
        for request in ["plna --target US-7", "plan --goa garden", 'setup --roles ""']:
            with self.subTest(request=request), self.assertRaises(ValueError):
                router.resolve(request)

    def test_plain_language_after_a_mode_keeps_its_scope(self):
        result = router.resolve("role legal review the platform design choices")
        self.assertEqual((result["role"], result["mode"]), ("legal-counsel", "review"))
        self.assertTrue(result["intent_resolution_required"])

    def test_possessive_apostrophes_are_literal_in_natural_language(self):
        request = "Resume from the project's latest handoff and reconcile the actual state."
        self.assertEqual(router.resolve(request)["request"], request)
        result = router.resolve("role legal review the platform's design choices")
        self.assertEqual((result["role"], result["mode"]), ("legal-counsel", "review"))

    def test_cli_stdin_preserves_quoted_windows_target(self):
        request = r'role legal review --target "C:\work\my garden\ci.yml"'
        result = run_cli("--stdin", input_text=request)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["options"]["target"], r"C:\work\my garden\ci.yml")

    def test_cli_empty_request_returns_parseable_wizard_intent(self):
        result = run_cli("")

        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["mode"], "wizard")
        self.assertFalse(data["executes_actions"])

    def test_cli_preserves_quoted_goal_target_and_shell_looking_data(self):
        request = r'setup --goal "$(whoami); harmless text" --target "C:\work\my garden\ci.yml"'

        result = run_cli(request)

        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["options"]["goal"], "$(whoami); harmless text")
        self.assertEqual(data["options"]["target"], r"C:\work\my garden\ci.yml")
        self.assertNotIn("whoami", result.stderr)

    def test_cli_rejects_invalid_role_mode_and_flag_without_traceback(self):
        requests = ["role enginer review", "role design deploy", "plan --unknown x"]

        for request in requests:
            with self.subTest(request=request):
                result = run_cli(request)

                self.assertEqual(result.returncode, 2)
                self.assertIn("scrum-skill routing:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_cli_rejects_multiple_argument_strings(self):
        result = run_cli("plan", "--goal", "one")

        self.assertEqual(result.returncode, 2)
        self.assertIn("one quoted invocation argument string", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
