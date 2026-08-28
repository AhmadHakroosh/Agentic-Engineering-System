import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_promotion.py"
SHA = "a" * 40
DIGEST = "sha256:" + "b" * 64


class PromotionVerificationTests(unittest.TestCase):
    def run_verifier(self, requested_sha=SHA, release_sha=SHA, requested_digest=DIGEST, release_digest=DIGEST):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--requested-sha", requested_sha, "--release-sha", release_sha,
             "--requested-digest", requested_digest, "--release-digest", release_digest],
            capture_output=True, text=True, check=False,
        )

    def test_accepts_exact_staged_identity(self):
        self.assertEqual(self.run_verifier().returncode, 0)

    def test_rejects_commit_substitution(self):
        self.assertNotEqual(self.run_verifier(release_sha="c" * 40).returncode, 0)

    def test_rejects_artifact_substitution(self):
        self.assertNotEqual(self.run_verifier(release_digest="sha256:" + "d" * 64).returncode, 0)

    def test_rejects_abbreviated_sha(self):
        self.assertNotEqual(self.run_verifier(requested_sha="a" * 7).returncode, 0)


if __name__ == "__main__":
    unittest.main()

