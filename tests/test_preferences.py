import unittest
from unittest.mock import patch

from config.preferences import (
    DEFAULT_PREFERENCES,
    load_preferences,
    save_preferences,
)


class FakeSettings:
    values = {}

    class Status:
        NoError = 0

    def __init__(self, _organization, _application):
        pass

    def value(self, key, default, type):
        return type(self.values.get(key, default))

    def setValue(self, key, value):
        self.values[key] = value

    def sync(self):
        pass

    def status(self):
        return self.Status.NoError


class TestPreferences(unittest.TestCase):
    def setUp(self):
        FakeSettings.values = {}
        self.settings_patch = patch("config.preferences.QSettings", FakeSettings)
        self.settings_patch.start()
        self.addCleanup(self.settings_patch.stop)

    def test_defaults_are_used_before_first_save(self):
        self.assertEqual(load_preferences(), DEFAULT_PREFERENCES)

    def test_saved_values_are_returned(self):
        save_preferences(sampling_rate=8000, amplitude=3.5, signal_frequency=75)

        self.assertEqual(
            load_preferences(),
            {
                "sampling_rate": 8000,
                "amplitude": 3.5,
                "signal_frequency": 75,
            },
        )

    def test_invalid_values_are_rejected(self):
        with self.assertRaises(ValueError):
            save_preferences(sampling_rate=1000, amplitude=2.0, signal_frequency=50)


if __name__ == "__main__":
    unittest.main()
