import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_checks", ROOT / "scripts/validate_package.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class PackageTests(unittest.TestCase):
    def test_actual_package_is_consistent(self):
        self.assertEqual(len(checks.validate()), 3)

    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "package"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".eval-output", "node_modules"))
        return root

    def test_host_version_drift_is_detected(self):
        root = self.fixture()
        path = root / ".codex-plugin/plugin.json"
        manifest = json.loads(path.read_text())
        manifest["version"] = "9.9.9"
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "version drift"):
            checks.validate(root)

    def test_missing_skill_resource_is_detected(self):
        root = self.fixture()
        (root / "skills/scrum-skill/references/roles.md").unlink()
        with self.assertRaisesRegex(ValueError, "broken local reference"):
            checks.validate(root)

    def test_unsafe_manifest_path_is_rejected(self):
        with self.assertRaises(ValueError):
            checks.inside(ROOT, "./../outside")

    def test_source_pdf_in_package_is_rejected(self):
        root = self.fixture()
        (root / "reference.pdf").write_bytes(b"synthetic fixture")
        with self.assertRaisesRegex(ValueError, "local/source document"):
            checks.validate(root)


if __name__ == "__main__":
    unittest.main()
