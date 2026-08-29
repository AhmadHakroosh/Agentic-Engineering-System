import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_instance.py"
SCHEMA = ROOT / "contracts" / "schemas" / "requirements.schema.json"
EXAMPLE = ROOT / "contracts" / "examples" / "requirements.example.json"


class ContractInstanceTests(unittest.TestCase):
    def run_validator(self, instance: Path):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(SCHEMA), str(instance)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_requirements_example(self):
        self.assertEqual(self.run_validator(EXAMPLE).returncode, 0)

    def test_missing_required_property_is_rejected(self):
        data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        del data["objective"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_validator(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("objective", result.stderr)

    def test_relative_ticket_uri_is_rejected(self):
        data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        data["ticket"]["url"] = "examples/ticket.md"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_validator(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("absolute URI", result.stderr)


if __name__ == "__main__":
    unittest.main()

