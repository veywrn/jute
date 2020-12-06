import unittest
from unittest.mock import patch

import os
import wx

import src.jute.assets as assets
import src.jute.app
import src.jute.storyframe


class TwineCompatibilityTests(unittest.TestCase):
    def setUp(self):
        # Twine changes dir without restoring, only lets first test pass.
        self.dir = os.path.abspath(os.curdir)

        assets_dir = os.path.abspath(assets._find_assets_dir(self.dir))
        test_dir = os.path.join(assets_dir, 'tests')
        test_files = os.listdir(test_dir)
        self.test_assets = {f: os.path.join(test_dir, f) for f in test_files}
        self.test_assets_dir = test_dir

    def tearDown(self):
        # Assert to notify when cruft not needed.
        self.assertNotEqual(os.curdir, self.dir)
        os.chdir(self.dir)

    @patch.object(wx.Frame, 'Show', new=lambda *a, **kw: None)
    @patch.object(src.jute.app.App, 'openOnStartup', new=lambda *a, **kw: True)
    def load_story(self, path):
        app = src.jute.app.App()
        try:
            app.open(path)
            panel = app.stories[-1].storyPanel
            widgets = panel.widgetDict
            passages = {k: widgets[k].passage for k in widgets}
        except Exception as ex:
            self.fail(ex)
        finally:
            app.exit()

        return widgets, passages

    def test_can_load_default_story(self):
        story = self.test_assets['default_t14.tws']
        widgets, passages = self.load_story(story)

        self.assertEqual(3, len(widgets))
        self.assertEqual(3, len(passages))

        self.assertEqual([10, 150], widgets['StoryTitle'].pos)
        self.assertEqual(10, len(passages['StoryTitle'].title))
        self.assertEqual(14, len(passages['StoryTitle'].text))

        self.assertEqual([10, 290], widgets['StoryAuthor'].pos)
        self.assertEqual(11, len(passages['StoryAuthor'].title))
        self.assertEqual(9, len(passages['StoryAuthor'].text))

        self.assertEqual([10, 10], widgets['Start'].pos)
        self.assertEqual(5, len(passages['Start'].title))
        self.assertEqual(74, len(passages['Start'].text))

    def test_can_load_modified_story(self):
        story = self.test_assets['modified_t14.tws']
        widgets, passages = self.load_story(story)

        self.assertEqual(7, len(widgets))
        self.assertEqual(7, len(passages))

        self.assertEqual([10, 10], widgets['StoryTitle'].pos)
        self.assertEqual(10, len(passages['StoryTitle'].title))
        self.assertEqual(17, len(passages['StoryTitle'].text))

        self.assertEqual([150, 10], widgets['StoryAuthor'].pos)
        self.assertEqual(11, len(passages['StoryAuthor'].title))
        self.assertEqual(15, len(passages['StoryAuthor'].text))

        self.assertEqual([430, 10], widgets['EmbeddedFont'].pos)
        self.assertEqual(12, len(passages['EmbeddedFont'].title))
        self.assertEqual(27986, len(passages['EmbeddedFont'].text))

        self.assertEqual([290, 10], widgets['EmbeddedImage'].pos)
        self.assertEqual(13, len(passages['EmbeddedImage'].title))
        self.assertEqual(1490, len(passages['EmbeddedImage'].text))

        self.assertEqual([150, 290], widgets['Start'].pos)
        self.assertEqual(5, len(passages['Start'].title))
        self.assertEqual(92, len(passages['Start'].text))

        self.assertEqual([570, 150], widgets['Hidden'].pos)
        self.assertEqual(6, len(passages['Hidden'].title))
        self.assertEqual(29, len(passages['Hidden'].text))

        self.assertEqual([570, 290], widgets['End'].pos)
        self.assertEqual(3, len(passages['End'].title))
        self.assertEqual(43, len(passages['End'].text))


if __name__ == '__main__':
    unittest.main()
