import jute.settings

import unittest
import wx


class SettingsBaseTests(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

    def tearDown(self):
        self.app = None

    def test_when_getattr_should_raise(self):
        with self.assertRaises(KeyError):
            settings = jute.settings.SettingsBase()
            settings.no_such_setting = False


class ApplicationSettingsTests(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.settings = jute.settings.ApplicationSettings()

    def tearDown(self):
        self.settings._wxConfig.DeleteAll()
        self.app = None

    def test_when_getting_before_setting_should_return_default(self):
        self.assertEqual(
            self.settings.flat_style, self.settings._KEYS['flat_style'][1])
        self.assertEqual(
            self.settings.flat_style,
            wx.Config().Get().ReadBool(self.settings._KEYS['flat_style'][0])
            )

    def test_when_getting_after_setting_should_return_as_set(self):
        self.settings.flat_style = True

        self.assertTrue(self.settings.flat_style)
        self.assertEqual(
            self.settings.flat_style,
            wx.Config().Get().ReadBool(self.settings._KEYS['flat_style'][0])
            )


if __name__ == '__main__':
    unittest.main()
