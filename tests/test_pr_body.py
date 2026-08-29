import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_pr_body.py"


class PullRequestBodyTests(unittest.TestCase):
    def run_validator(self, body: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "body.md"
            path.write_text(body, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_blank_template_is_rejected(self):
        body = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        self.assertNotEqual(self.run_validator(body).returncode, 0)

    def test_populated_template_is_accepted(self):
        lines = [
            f"- {field}: supplied" for field in (
                "Reference", "Requirements contract", "Design contract", "Delivery packet",
                "Summary", "Explicitly out of scope", "Acceptance criteria", "Checks run",
                "Independent review", "Residual risks", "Rollout", "Rollback", "Observability",
            )
        ]
        lines.append("- [x] Attested")
        self.assertEqual(self.run_validator("\n".join(lines)).returncode, 0)


if __name__ == "__main__":
    unittest.main()

