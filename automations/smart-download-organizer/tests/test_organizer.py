
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from src.organizer import (
    create_organization_plan,
    organize_files,
    undo_organization,
    load_movement_history
)


class TestOrganizer(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        self.history_path = self.folder / "history.json"

        self.documents = self.folder / "Documents"
        self.documents.mkdir()

        self.source_file = self.folder / "report.pdf"

        self.source_file.write_text(
            "Sample report",
            encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_plan(self):

        file_stat = self.source_file.stat()

        files = [{
            "name": "report.pdf",
            "path": str(self.source_file),
            "category": "Documents",
            "size_bytes": file_stat.st_size,
            "modified_timestamp": file_stat.st_mtime
        }]

        return create_organization_plan(
            files,
            self.folder
        )

    def test_create_organization_plan(self):

        plan = self.create_plan()

        self.assertEqual(len(plan), 1)

        self.assertEqual(
            Path(plan[0]["destination"]).parent,
            self.documents
        )

        self.assertTrue(self.source_file.exists())

        self.assertIn("expected_size_bytes", plan[0])
        self.assertIn("expected_modified_timestamp", plan[0])

    def test_duplicate_filename_handling(self):

        existing_file = self.documents / "report.pdf"

        existing_file.write_text(
            "Existing report",
            encoding="utf-8"
        )

        plan = self.create_plan()

        destination = Path(plan[0]["destination"])

        self.assertEqual(
            destination.name,
            "report (1).pdf"
        )

    def test_organize_files(self):

        plan = self.create_plan()

        history = organize_files(
            plan,
            self.history_path
        )

        destination = self.documents / "report.pdf"

        self.assertTrue(destination.exists())
        self.assertFalse(self.source_file.exists())

        self.assertEqual(len(history), 1)

        self.assertEqual(
            plan[0]["status"],
            "Moved"
        )

    def test_persistent_history(self):

        plan = self.create_plan()

        organize_files(
            plan,
            self.history_path
        )

        # Simulate loading history after an application restart.
        loaded_history = load_movement_history(
            self.history_path
        )

        self.assertEqual(len(loaded_history), 1)

        self.assertEqual(
            loaded_history[0]["name"],
            "report.pdf"
        )

    def test_file_modified_after_scanning(self):

        plan = self.create_plan()

        # Modify the file after the plan has been generated.
        self.source_file.write_text(
            "Updated report with additional content",
            encoding="utf-8"
        )

        history = organize_files(
            plan,
            self.history_path
        )

        self.assertTrue(self.source_file.exists())

        self.assertFalse(
            (self.documents / "report.pdf").exists()
        )

        self.assertEqual(len(history), 0)

        self.assertEqual(
            plan[0]["status"],
            "Skipped: File changed since scan"
        )

    def test_deleted_file_after_scanning(self):

        plan = self.create_plan()

        # Delete the file after scanning.
        self.source_file.unlink()

        history = organize_files(
            plan,
            self.history_path
        )

        self.assertFalse(self.source_file.exists())

        self.assertFalse(
            (self.documents / "report.pdf").exists()
        )

        self.assertEqual(len(history), 0)

        self.assertEqual(
            plan[0]["status"],
            "Skipped: Source unavailable"
        )

    def test_destination_file_is_never_overwritten(self):

        plan = self.create_plan()

        destination = self.documents / "report.pdf"

        # Create a destination file after the plan was generated.
        destination.write_text(
            "Important existing file",
            encoding="utf-8"
        )

        history = organize_files(
            plan,
            self.history_path
        )

        duplicate_destination = self.documents / "report (1).pdf"

        self.assertTrue(destination.exists())
        self.assertTrue(duplicate_destination.exists())

        self.assertEqual(
            destination.read_text(encoding="utf-8"),
            "Important existing file"
        )

        self.assertEqual(
            duplicate_destination.read_text(encoding="utf-8"),
            "Sample report"
        )

        self.assertEqual(len(history), 1)

    def test_persistent_history_records_successful_movement(self):

        plan = self.create_plan()

        organize_files(
            plan,
            self.history_path
        )

        loaded_history = load_movement_history(
            self.history_path
        )

        self.assertEqual(len(loaded_history), 1)

        self.assertEqual(
            loaded_history[0]["source"],
            str(self.source_file)
        )

        self.assertEqual(
            loaded_history[0]["destination"],
            str(self.documents / "report.pdf")
        )

        self.assertIn("moved_at", loaded_history[0])

    def test_undo_organization(self):

        plan = self.create_plan()

        history = organize_files(
            plan,
            self.history_path
        )

        results = undo_organization(
            history,
            self.history_path
        )

        self.assertTrue(self.source_file.exists())

        self.assertFalse(
            (self.documents / "report.pdf").exists()
        )

        self.assertEqual(
            results[0]["status"],
            "Restored"
        )

    def test_undo_does_not_overwrite_original_file(self):

        plan = self.create_plan()

        history = organize_files(
            plan,
            self.history_path
        )

        # Create another file at the original location.
        self.source_file.write_text(
            "New important file",
            encoding="utf-8"
        )

        results = undo_organization(
            history,
            self.history_path
        )

        self.assertTrue(self.source_file.exists())

        self.assertEqual(
            self.source_file.read_text(encoding="utf-8"),
            "New important file"
        )

        self.assertTrue(
            (self.documents / "report.pdf").exists()
        )

        self.assertEqual(
            results[0]["status"],
            "Failed: Original location occupied"
        )

        # Failed undo should remain available in history.
        remaining_history = load_movement_history(
            self.history_path
        )

        self.assertEqual(len(remaining_history), 1)

    def test_history_cleared_after_undo(self):

        plan = self.create_plan()

        history = organize_files(
            plan,
            self.history_path
        )

        undo_organization(
            history,
            self.history_path
        )

        remaining_history = load_movement_history(
            self.history_path
        )

        self.assertEqual(remaining_history, [])

    def test_file_restored_when_history_save_fails(self):

        plan = self.create_plan()

        with patch(
            "src.organizer.save_movement_history",
            side_effect=OSError("Simulated history failure")
        ):

            history = organize_files(
                plan,
                self.history_path
            )

        self.assertTrue(self.source_file.exists())

        self.assertFalse(
            (self.documents / "report.pdf").exists()
        )

        self.assertEqual(len(history), 0)

        self.assertEqual(
            plan[0]["status"],
            "Failed: History save failed; file restored"
        )


if __name__ == "__main__":
    unittest.main()
