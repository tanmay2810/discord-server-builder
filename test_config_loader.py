import unittest

from config import load_server_config


class ConfigLoaderTests(unittest.TestCase):
    def test_load_server_config_returns_dict(self):
        config = load_server_config()
        self.assertIsInstance(config, dict)
        self.assertIn("roles", config)
        self.assertIn("categories", config)

    def test_load_server_config_has_expected_keys(self):
        config = load_server_config()
        self.assertIn("staff", config["roles"])
        self.assertIn("levels", config["roles"])
        self.assertIn("bot_role", config["roles"])
        self.assertIsInstance(config["categories"], list)


if __name__ == "__main__":
    unittest.main()
