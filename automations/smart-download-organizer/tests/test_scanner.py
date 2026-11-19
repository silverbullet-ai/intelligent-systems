import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from src.scanner import (
    scan_folder,
    format_file_size
)

from src.config_manager import load_config


class TestScanner(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        # Create sample files.
        (self.folder / "report.pdf").write_text(
            "Sample report",
            encoding="utf-8"
        )

        (self.folder / "notes.txt").write_text(
            "Sample notes",
            encoding="utf-8"
        )

        # Create a subfolder with another file.
        self.subfolder = self.folder / "Projects"
        self.subfolder.mkdir()

        (self.subfolder / "script.py").write_text(
            "print('Hello World')",
            encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    # --------------------------------------------------
    # FILE SIZE FORMATTING TESTS
    # --------------------------------------------------

    def test_format_file_size(self):

        self.assertEqual(format_file_size(0), "0.00 B")
        self.assertEqual(format_file_size(1024), "1.00 KB")
        self.assertEqual(format_file_size(1048576), "1.00 MB")

    # --------------------------------------------------
    # BASIC SCANNING TESTS
    # --------------------------------------------------

    def test_scan_folder(self):

        files, summary = scan_folder(self.folder)

        self.assertEqual(len(files), 2)
        self.assertEqual(summary["total_files"], 2)

    def test_recursive_scan(self):

        files, summary = scan_folder(
            self.folder,
            recursive=True
        )

        self.assertEqual(len(files), 3)
        self.assertEqual(summary["total_files"], 3)

    def test_non_recursive_scan_excludes_subfolders(self):

        files, summary = scan_folder(
            self.folder,
            recursive=False
        )

        file_names = [file["name"] for file in files]

        self.assertNotIn("script.py", file_names)

    def test_recursive_scan_includes_subfolder_files(self):

        files, summary = scan_folder(
            self.folder,
            recursive=True
        )

        file_names = [file["name"] for file in files]

        self.assertIn("script.py", file_names)

    # --------------------------------------------------
    # FILE METADATA TESTS
    # --------------------------------------------------

    def test_file_metadata(self):

        files, summary = scan_folder(self.folder)

        report = next(
            file for file in files
            if file["name"] == "report.pdf"
        )

        self.assertEqual(report["extension"], ".pdf")
        self.assertEqual(report["category"], "Uncategorized")
        self.assertIn("size_bytes", report)
        self.assertIn("modified", report)
        self.assertIn("modified_timestamp", report)
        self.assertTrue(Path(report["path"]).exists())

    # --------------------------------------------------
    # SCAN SUMMARY TESTS
    # --------------------------------------------------

    def test_scan_summary(self):

        files, summary = scan_folder(self.folder)

        self.assertIn("folder", summary)
        self.assertIn("total_files", summary)
        self.assertIn("total_size_bytes", summary)
        self.assertIn("total_size", summary)
        self.assertIn("inaccessible_files", summary)

        self.assertEqual(summary["total_files"], 2)

    # --------------------------------------------------
    # ERROR HANDLING TESTS
    # --------------------------------------------------

    def test_missing_folder(self):

        missing_folder = self.folder / "does_not_exist"

        with self.assertRaises(FileNotFoundError):
            scan_folder(missing_folder)

    def test_path_is_a_file(self):

        file_path = self.folder / "report.pdf"

        with self.assertRaises(NotADirectoryError):
            scan_folder(file_path)

    # --------------------------------------------------
    # CUSTOM CATEGORY SCANNING TESTS
    # --------------------------------------------------

    def test_recursive_scan_skips_custom_categories(self):
        """Custom organizer categories should be skipped during recursive scans."""

        config = load_config()
        config["categories"]["Ebooks"] = [".epub"]

        ebooks_folder = self.folder / "Ebooks"
        ebooks_folder.mkdir()

        (ebooks_folder / "novel.epub").write_text(
            "Sample ebook",
            encoding="utf-8"
        )

        with patch("src.scanner.load_config", return_value=config):
            files, summary = scan_folder(
                self.folder,
                recursive=True
            )

        file_names = [file["name"] for file in files]

        self.assertNotIn("novel.epub", file_names)
        self.assertEqual(summary["total_files"], 3)

    def test_recursive_scan_skips_default_category(self):
        """The configured default category should also be skipped."""

        config = load_config()
        config["default_category"] = "Unsorted"

        unsorted_folder = self.folder / "Unsorted"
        unsorted_folder.mkdir()

        (unsorted_folder / "unknown.xyz").write_text(
            "Unknown file",
            encoding="utf-8"
        )

        with patch("src.scanner.load_config", return_value=config):
            files, summary = scan_folder(
                self.folder,
                recursive=True
            )

        file_names = [file["name"] for file in files]

        self.assertNotIn("unknown.xyz", file_names)
        self.assertEqual(summary["total_files"], 3)


if __name__ == "__main__":
    unittest.main()