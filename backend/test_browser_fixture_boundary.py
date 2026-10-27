import os
import tempfile
import unittest
import types
import test_browser_ui as browser_fixtures

class MockBrowserTest:
    def __init__(self, methodName='runTest'):
        self.responses = []
        self.page_errors = []

    def setUp(self):
        # We only want to test the _start_playwright_with_canonical_temp method
        # without running the full server / playwright start.
        pass

    def tearDown(self):
        pass

    def mock_startup(self):
        self.callback_called = True
        self.captured_env = {k: os.environ.get(k) for k in ("TMP", "TEMP", "TMPDIR")}
        return "mock_playwright"

    def mock_startup_fail(self):
        self.callback_called = True
        self.captured_env = {k: os.environ.get(k) for k in ("TMP", "TEMP", "TMPDIR")}
        raise RuntimeError("Startup failed")


class BrowserFixtureBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.original_env = {k: os.environ.get(k) for k in ("TMP", "TEMP", "TMPDIR")}
        self.test_instance = MockBrowserTest("run")
        self.test_instance.setUp()
        self.temp_dir = tempfile.TemporaryDirectory(prefix="mock-browser-")
        self.fixture_ancestor = os.path.dirname(self.temp_dir.name)
        self.canonical_ancestor = self.fixture_ancestor
        if self.canonical_ancestor.startswith("\\\\?\\UNC\\"):
            self.canonical_ancestor = "\\\\" + self.canonical_ancestor[8:]
        elif self.canonical_ancestor.startswith("\\\\?\\"):
            self.canonical_ancestor = self.canonical_ancestor[4:]

        self.receiver = types.SimpleNamespace()
        self.receiver.temp_dir = types.SimpleNamespace(name=self.temp_dir.name)

        self.test_instance.callback_called = False
        self.test_instance.captured_env = None

    def tearDown(self):
        for k, v in self.original_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        name_before = self.temp_dir.name
        self.temp_dir.cleanup()
        self.assertEqual(self.temp_dir.name, name_before)
        self.assertFalse(os.path.exists(name_before))
        self.test_instance.tearDown()

    def test_canonicalizes_ancestor_on_success(self):
        os.environ["TMP"] = self.fixture_ancestor
        os.environ["TEMP"] = self.fixture_ancestor
        os.environ.pop("TMPDIR", None)

        result = browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(self.receiver, self.test_instance.mock_startup)

        self.assertEqual(result, "mock_playwright")
        self.assertTrue(self.test_instance.callback_called)
        self.assertEqual(self.test_instance.captured_env["TMP"], self.canonical_ancestor)
        self.assertEqual(self.test_instance.captured_env["TEMP"], self.canonical_ancestor)
        self.assertIsNone(self.test_instance.captured_env["TMPDIR"])

        # Verify restoration
        self.assertEqual(os.environ.get("TMP"), self.fixture_ancestor)
        self.assertEqual(os.environ.get("TEMP"), self.fixture_ancestor)
        self.assertNotIn("TMPDIR", os.environ)

    def test_canonicalizes_ancestor_on_failure(self):
        os.environ["TMP"] = self.fixture_ancestor
        os.environ["TEMP"] = self.fixture_ancestor
        os.environ.pop("TMPDIR", None)

        with self.assertRaisesRegex(RuntimeError, "Startup failed"):
            browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(self.receiver, self.test_instance.mock_startup_fail)

        self.assertTrue(self.test_instance.callback_called)
        self.assertEqual(self.test_instance.captured_env["TMP"], self.canonical_ancestor)
        self.assertEqual(self.test_instance.captured_env["TEMP"], self.canonical_ancestor)
        self.assertIsNone(self.test_instance.captured_env["TMPDIR"])

        # Verify restoration even on failure
        self.assertEqual(os.environ.get("TMP"), self.fixture_ancestor)
        self.assertEqual(os.environ.get("TEMP"), self.fixture_ancestor)
        self.assertNotIn("TMPDIR", os.environ)

    def test_does_not_modify_non_ancestor_paths(self):
        # A completely unrelated path
        unrelated_path = "C:\\Windows\\Temp" if os.name == 'nt' else "/tmp/other"
        os.environ["TMP"] = unrelated_path

        browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(self.receiver, self.test_instance.mock_startup)

        # Should remain the unrelated path without modification
        self.assertEqual(self.test_instance.captured_env["TMP"], unrelated_path)
        self.assertEqual(os.environ.get("TMP"), unrelated_path)

    def test_handles_absent_variables(self):
        for k in ("TMP", "TEMP", "TMPDIR"):
            os.environ.pop(k, None)

        browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(self.receiver, self.test_instance.mock_startup)

        for k in ("TMP", "TEMP", "TMPDIR"):
            self.assertIsNone(self.test_instance.captured_env[k])
            self.assertNotIn(k, os.environ)

    def test_handles_unc_paths(self):
        unc_path = "\\\\server\\share\\temp"
        os.environ["TMP"] = unc_path

        unc_receiver = types.SimpleNamespace()
        unc_receiver.temp_dir = types.SimpleNamespace(name="\\\\server\\share\\temp\\fixture")

        browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(unc_receiver, self.test_instance.mock_startup)

        self.assertEqual(self.test_instance.captured_env["TMP"], unc_path)
        self.assertEqual(os.environ.get("TMP"), unc_path)

    def test_handles_extended_unc_paths(self):
        extended_unc_path = "\\\\?\\UNC\\server\\share\\temp"
        standard_unc_path = "\\\\server\\share\\temp"
        os.environ["TMP"] = extended_unc_path

        unc_receiver = types.SimpleNamespace()
        unc_receiver.temp_dir = types.SimpleNamespace(name="\\\\?\\UNC\\server\\share\\temp\\fixture")

        browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(unc_receiver, self.test_instance.mock_startup)

        self.assertEqual(self.test_instance.captured_env["TMP"], standard_unc_path)
        self.assertEqual(os.environ.get("TMP"), extended_unc_path)

    def test_handles_extended_local_paths(self):
        extended_local_path = "\\\\?\\C:\\Temp"
        standard_local_path = "C:\\Temp"
        os.environ["TMP"] = extended_local_path

        local_receiver = types.SimpleNamespace()
        local_receiver.temp_dir = types.SimpleNamespace(name="\\\\?\\C:\\Temp\\fixture")

        browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(local_receiver, self.test_instance.mock_startup)

        self.assertEqual(self.test_instance.captured_env["TMP"], standard_local_path)
        self.assertEqual(os.environ.get("TMP"), extended_local_path)


    def test_plain_owned_ancestor_with_trailing_separator_preserved_at_startup_and_after_failure(self):
        plain_path = self.canonical_ancestor + os.sep
        os.environ["TMP"] = plain_path
        os.environ["TEMP"] = plain_path
        os.environ["TMPDIR"] = plain_path

        receiver = types.SimpleNamespace()
        receiver.temp_dir = types.SimpleNamespace(name=self.temp_dir.name)

        with self.assertRaisesRegex(RuntimeError, "Startup failed"):
            browser_fixtures.BrowserUiRegressionTests._start_playwright_with_canonical_temp(receiver, self.test_instance.mock_startup_fail)

        self.assertTrue(self.test_instance.callback_called)
        self.assertEqual(self.test_instance.captured_env["TMP"], plain_path)
        self.assertEqual(self.test_instance.captured_env["TEMP"], plain_path)
        self.assertEqual(self.test_instance.captured_env["TMPDIR"], plain_path)

        self.assertEqual(os.environ.get("TMP"), plain_path)
        self.assertEqual(os.environ.get("TEMP"), plain_path)
        self.assertEqual(os.environ.get("TMPDIR"), plain_path)

if __name__ == "__main__":
    unittest.main()
