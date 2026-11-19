
import unittest

from src.categorizer import (
    load_rules,
    get_category,
    categorize_files,
    get_category_summary
)


class TestCategorizer(unittest.TestCase):

    def setUp(self):
        self.rules = load_rules()

    def test_load_rules(self):

        self.assertIsInstance(self.rules, dict)

        self.assertIn("categories", self.rules)
        self.assertIn("default_category", self.rules)

    def test_get_category_documents(self):

        category = get_category(".pdf", self.rules)

        self.assertEqual(category, "Documents")

    def test_get_category_images(self):

        category = get_category(".jpg", self.rules)

        self.assertEqual(category, "Images")

    def test_get_category_videos(self):

        category = get_category(".mp4", self.rules)

        self.assertEqual(category, "Videos")

    def test_get_category_audio(self):

        category = get_category(".mp3", self.rules)

        self.assertEqual(category, "Audio")

    def test_get_category_archives(self):

        category = get_category(".zip", self.rules)

        self.assertEqual(category, "Archives")

    def test_get_category_installers(self):

        category = get_category(".exe", self.rules)

        self.assertEqual(category, "Installers")

    def test_get_category_code(self):

        category = get_category(".py", self.rules)

        self.assertEqual(category, "Code")

    def test_unknown_extension(self):

        category = get_category(".unknown", self.rules)

        self.assertEqual(
            category,
            self.rules["default_category"]
        )

    def test_case_insensitive_extension(self):

        category = get_category(".PDF", self.rules)

        self.assertEqual(category, "Documents")

    def test_categorize_files(self):

        files = [
            {"name": "report.pdf", "extension": ".pdf"},
            {"name": "photo.jpg", "extension": ".jpg"},
            {"name": "script.py", "extension": ".py"}
        ]

        categorized_files = categorize_files(
            files,
            self.rules
        )

        self.assertEqual(
            categorized_files[0]["category"],
            "Documents"
        )

        self.assertEqual(
            categorized_files[1]["category"],
            "Images"
        )

        self.assertEqual(
            categorized_files[2]["category"],
            "Code"
        )

    def test_get_category_summary(self):

        files = [
            {"name": "report.pdf", "category": "Documents"},
            {"name": "notes.txt", "category": "Documents"},
            {"name": "photo.jpg", "category": "Images"},
            {"name": "script.py", "category": "Code"}
        ]

        summary = get_category_summary(files)

        self.assertEqual(summary["Documents"], 2)
        self.assertEqual(summary["Images"], 1)
        self.assertEqual(summary["Code"], 1)


if __name__ == "__main__":
    unittest.main()
