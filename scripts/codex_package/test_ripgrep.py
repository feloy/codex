import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codex_package.dotslash import artifact_for_target
from codex_package.ripgrep import RG_MANIFEST
from codex_package.targets import TARGET_SPECS


class RipgrepManifestTest(unittest.TestCase):
    def test_linux_packages_use_musl_ripgrep(self) -> None:
        # GNU and musl packages share each architecture's manifest entry. Use
        # musl builds so bundled ripgrep also runs on systems without glibc.
        for target, spec in TARGET_SPECS.items():
            if not spec.is_linux:
                continue
            with self.subTest(target=target):
                artifact = artifact_for_target(
                    spec, RG_MANIFEST, artifact_label="ripgrep"
                )
                self.assertIsNotNone(artifact)
                architecture = target.split("-", 1)[0]
                self.assertIn(
                    f"-{architecture}-unknown-linux-musl/", artifact.archive_member
                )
                self.assertTrue(
                    artifact.url.endswith(f"-{architecture}-unknown-linux-musl.tar.gz")
                )


if __name__ == "__main__":
    unittest.main()
