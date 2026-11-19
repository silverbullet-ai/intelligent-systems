
import tempfile
import unittest

from pathlib import Path

from src.config_manager import (
    load_config,
    save_config,
    add_category,
    remove_category,
    add_extension,
    remove_extension,
    set_default_category,
    reset_config,
    validate_config
)


class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "rules.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_default_config(self):

        config = load_config(self.config_path)

        self.assertIn("Documents", config["categories"])
        self.assertEqual(
            config["default_category"],
            "Miscellaneous"
        )

    def test_save_and_load_config(self):

        config = load_config(self.config_path)

        save_config(config, self.config_path)

        loaded_config = load_config(self.config_path)

        self.assertEqual(config, loaded_config)

    def test_add_category(self):

        config = add_category(
            "Fonts",
            config_path=self.config_path
        )

        self.assertIn("Fonts", config["categories"])

    def test_remove_category(self):

        config = load_config(self.config_path)

        config = remove_category(
            "Images",
            config,
            self.config_path
        )

        self.assertNotIn("Images", config["categories"])

    def test_add_extension(self):

        config = add_extension(
            "Documents",
            ".epub",
            config_path=self.config_path
        )

        self.assertIn(
            ".epub",
            config["categories"]["Documents"]
        )

    def test_remove_extension(self):

        config = load_config(self.config_path)

        config = remove_extension(
            "Documents",
            ".pdf",
            config,
            self.config_path
        )

        self.assertNotIn(
            ".pdf",
            config["categories"]["Documents"]
        )

    def test_duplicate_extension_rejected(self):

        with self.assertRaises(ValueError):
            add_extension(
                "Images",
                ".pdf",
                config_path=self.config_path
            )

    def test_invalid_config_rejected(self):

        config = load_config(self.config_path)

        config["categories"]["Images"].append(".pdf")

        with self.assertRaises(ValueError):
            validate_config(config)

    def test_set_default_category(self):

        config = set_default_category(
            "Other Files",
            config_path=self.config_path
        )

        self.assertEqual(
            config["default_category"],
            "Other Files"
        )

    def test_reset_config(self):

        add_category(
            "Fonts",
            config_path=self.config_path
        )

        config = reset_config(self.config_path)

        self.assertNotIn("Fonts", config["categories"])

        self.assertEqual(
            config["default_category"],
            "Miscellaneous"
        )


if __name__ == "__main__":
    unittest.main()
