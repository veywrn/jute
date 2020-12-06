#!/usr/bin/env python

import assets
import config
import i18n

import os
import pickle
import re
import sys
import traceback

import wx
import wx.adv

import metrics
from header import Header
from prefframe import PreferenceFrame
from storyframe import StoryFrame


class App(wx.App):
    """This bootstraps our application and keeps track of preferences, etc."""

    RECENT_FILES = 10

    def __init__(self, *args, **kwargs):
        """Initializes the application."""

        wx.App.__init__(self, *args, **kwargs)

        self.stories = []
        self.loadPrefs()
        self.determinePaths()
        self.loadTargetHeaders()

        if not len(self.headers):
            self.displayError(
                "starting up: there are no story formats available!\n\n"
                + 'The "targets" directory could have been removed or emptied.\n\nYou may have to reinstall Twine',
                False,
            )
            self.Exit()

        # try to load our app icon
        # if it doesn't work, we continue anyway

        self.icon = wx.Icon()

        try:
            self.icon = wx.Icon(self.iconsPath + "app.ico", wx.BITMAP_TYPE_ICO)
        except:
            pass

        # restore save location

        try:
            os.chdir(self.config.Read("savePath"))
        except:
            os.chdir(os.path.expanduser("~"))

        if not self.openOnStartup():
            if self.config.HasEntry("LastFile") and os.path.exists(
                self.config.Read("LastFile")
            ):
                self.open(self.config.Read("LastFile"))
            else:
                self.newStory()

    def InitLocale(self):
        # BUG wxPython 4.1 has issue with Windows returning en-US instead of
        #     expected en_US. Workaround from Robin in wxPython discussion:
        #
        #     https://discuss.wxpython.org/t/34606
        #
        #     Order of calls here is significant.
        #
        self.ResetLocale()
        import locale
        language, encoding = locale.getdefaultlocale()
        wx.Locale.AddCatalogLookupPathPrefix(i18n.locale_dir)
        self._initial_locale = wx.Locale(language, language[:2], language)
        locale.setlocale(locale.LC_ALL, language)
        self._initial_locale.AddCatalog(config.APP_NAME)

    def newStory(self, event=None):
        """Opens a new, blank story."""
        s = StoryFrame(parent=None, app=self)
        self.stories.append(s)
        s.Show(True)

    def removeStory(self, story, byMenu=False):
        """Removes a story from our collection. Should be called when it closes."""
        try:
            self.stories.remove(story)
            if byMenu:
                counter = 0
                for s in self.stories:
                    if isinstance(s, StoryFrame):
                        counter = counter + 1
                if counter == 0:
                    self.newStory()

        except ValueError:
            pass

    def openDialog(self, event=None):
        """Opens a story file of the user's choice."""
        dialog = wx.FileDialog(
            None,
            "Open Story",
            os.getcwd(),
            "",
            "Twine Story (*.tws)|*.tws",
            wx.FD_OPEN | wx.FD_CHANGE_DIR,
        )

        if dialog.ShowModal() == wx.ID_OK:
            self.config.Write("savePath", os.getcwd())
            self.addRecentFile(dialog.GetPath())
            self.open(dialog.GetPath())

        dialog.Destroy()

    def openRecent(self, story, index):
        """Opens a recently-opened file."""
        filename = story.recentFiles.GetHistoryFile(index)
        if not os.path.exists(filename):
            self.removeRecentFile(story, index)
        else:
            self.open(filename)
            self.addRecentFile(filename)

    def MacOpenFile(self, path):
        """OS X support"""
        self.open(path)

    def open(self, path):
        """Opens a specific story file."""
        try:
            openedFile = open(path, "rb")
            newStory = StoryFrame(None, app=self, state=pickle.load(openedFile))
            newStory.saveDestination = path
            self.stories.append(newStory)
            newStory.Show(True)
            self.addRecentFile(path)
            self.config.Write("LastFile", path)
            openedFile.close()

            # weird special case:
            # if we only had one story opened before
            # and it's pristine (e.g. no changes ever made to it),
            # then we close it after opening the file successfully

            if (len(self.stories) == 2) and (self.stories[0].pristine):
                self.stories[0].Destroy()

        except:
            self.displayError("opening your story")

    def openOnStartup(self):
        """
        Opens any files that were passed via argv[1:]. Returns
        whether anything was opened.
        """
        if len(sys.argv) is 1:
            return False

        for file in sys.argv[1:]:
            self.open(file)

        return True

    def exit(self, event=None):
        """Closes all open stories, implicitly quitting."""
        # need to make a copy of our stories list since
        # stories removing themselves will alter the list midstream
        for s in list(self.stories):
            if isinstance(s, StoryFrame):
                s.Close()

    def showPrefs(self, event=None):
        """Shows the preferences dialog."""
        if not hasattr(self, "prefFrame"):
            self.prefFrame = PreferenceFrame(self)
        else:
            try:
                self.prefFrame.Raise()
            except RuntimeError:
                # user closed the frame, so we need to recreate it
                delattr(self, "prefFrame")
                self.showPrefs(event)

    def addRecentFile(self, path):
        """Adds a path to the recent files history and updates the menus."""
        for s in self.stories:
            if isinstance(s, StoryFrame):
                s.recentFiles.AddFileToHistory(path)
                s.recentFiles.Save(self.config)

    def removeRecentFile(self, story, index):
        """Remove all missing files from the recent files history and update the menus."""

        def removeRecentFile_do(story, index, showdialog=True):
            filename = story.recentFiles.GetHistoryFile(index)
            story.recentFiles.RemoveFileFromHistory(index)
            story.recentFiles.Save(self.config)
            if showdialog:
                text = (
                    "The file "
                    + filename
                    + " no longer exists.\n"
                    + "This file has been removed from the Recent Files list."
                )
                dlg = wx.MessageDialog(
                    None, text, "Information", wx.OK | wx.ICON_INFORMATION
                )
                dlg.ShowModal()
                dlg.Destroy()
                return True
            else:
                return False

        showdialog = True
        for s in self.stories:
            if s != story and isinstance(s, StoryFrame):
                removeRecentFile_do(s, index, showdialog)
                showdialog = False
        removeRecentFile_do(story, index, showdialog)

    def verifyRecentFiles(self, story):
        done = False
        while done == False:
            for index in range(story.recentFiles.GetCount()):
                if not os.path.exists(story.recentFiles.GetHistoryFile(index)):
                    self.removeRecentFile(story, index)
                    done = False
                    break
            else:
                done = True

    def about(self, event=None):
        """Shows the about dialog."""
        info = wx.adv.AboutDialogInfo()
        info.SetName(config.APP_NAME)
        info.SetDescription(config.APP_DESCRIPTION)
        info.SetVersion(
            f"{config.APP_VERSION_STRING} on {config.APP_SYSTEM_STRING}"
        )
        info.SetIcon(self.icon)
        info.SetDevelopers(["".join([
            config.APP_NAME,
            ":\n",
            config.APP_AUTHORS,
            "\n",
            config.APP_ORIGIN_NAME,
            ":\n",
            config.APP_ORIGIN_AUTHORS
            ])
        ])
        info.SetWebSite(config.URL_TWINE)
        info.SetLicense(
            "{} and {} {} are licensed under {}. Derivative work of TiddlyWiki"
            " by Jeremy Ruston is licensed under the MIT license.".format(
                config.APP_ORIGIN_NAME,
                config.APP_NAME,
                config.APP_VERSION_STRING,
                config.APP_LICENSE
            )
        )
        wx.adv.AboutBox(info)

    def storyFormatHelp(self, event=None):
        """Opens the online manual to the section on story formats."""
        wx.LaunchDefaultBrowser(config.URL_TWINE_HELP_STORIES)

    def openForum(self, event=None):
        """Opens the forum."""
        wx.LaunchDefaultBrowser(config.URL_TWINE_FORUM)

    def openDocs(self, event=None):
        """Opens the online manual."""
        wx.LaunchDefaultBrowser(config.URL_TWINE_HELP)

    def openGitHub(self, event=None):
        """Opens the GitHub page."""
        wx.LaunchDefaultBrowser(config.URL_TWINE_GITHUB)

    def loadPrefs(self):
        """Loads user preferences into self.config, setting up defaults if none are set."""
        sc = self.config = wx.Config("Twine")

        for k, v in {
            "savePath": os.path.expanduser("~"),
            "fsTextColor": "#afcdff",
            "fsBgColor": "#100088",
            "fsFontFace": metrics.face("mono"),
            "fsFontSize": metrics.size("fsEditorBody"),
            "fsLineHeight": 120,
            "windowedFontFace": metrics.face("mono"),
            "monospaceFontFace": metrics.face("mono2"),
            "windowedFontSize": metrics.size("editorBody"),
            "monospaceFontSize": metrics.size("editorBody"),
            "flatDesign": False,
            "storyFrameToolbar": True,
            "storyPanelSnap": False,
            "fastStoryPanel": False,
            "imageArrows": True,
            "displayArrows": True,
            "createPassagePrompt": True,
            "importImagePrompt": True,
            "passageWarnings": True,
        }.items():
            if not sc.HasEntry(k):
                if type(v) == str:
                    sc.Write(k, v)
                elif type(v) == int:
                    sc.WriteInt(k, v)
                elif type(v) == bool:
                    sc.WriteBool(k, v)

    def applyPrefs(self):
        """Asks all of our stories to update themselves based on a preference change."""
        for story in self.stories:
            story.applyPrefs()

    def displayError(self, activity, stacktrace=True):
        """
        Displays an error dialog with diagnostic info. Call with what you were doing
        when the error occurred (e.g. 'saving your story', 'building your story'.)
        """
        text = "An error occurred while " + activity + ".\n\n"
        if stacktrace:
            text += "".join(traceback.format_exc(5))
        else:
            text += "(" + str(sys.exc_info()[1]) + ")."
        error = wx.MessageDialog(None, text, "Error", wx.OK | wx.ICON_ERROR)
        error.ShowModal()

    def MacReopenApp(self):
        """OS X support"""
        self.GetTopWindow().Raise()

    def determinePaths(self):
        """Determine the paths to relevant files used by application"""
        scriptPath = assets.DIRECTORY
        if sys.platform == "win32":
            # Windows py2exe'd apps add an extraneous library.zip at the end
            scriptPath = re.sub("\\\\\w*.zip", "", scriptPath)
        elif sys.platform == "darwin":
            scriptPath = re.sub("MacOS\/.*", "", scriptPath)

        scriptPath += os.sep
        self.iconsPath = scriptPath + "icons" + os.sep
        self.builtinTargetsPath = scriptPath + "targets" + os.sep

        if sys.platform == "darwin":
            self.externalTargetsPath = re.sub(
                "[^/]+.app/.*", "targets" + os.sep, self.builtinTargetsPath
            )
            if not os.path.isdir(self.externalTargetsPath):
                self.externalTargetsPath = ""
        else:
            self.externalTargetsPath = ""

    def loadTargetHeaders(self):
        """Load the target headers and populate the self.headers dictionary"""
        self.headers = {}
        # Get paths to built-in targets
        if not os.path.isdir(self.builtinTargetsPath):
            return
        paths = [
            (t, self.builtinTargetsPath + t + os.sep)
            for t in os.listdir(self.builtinTargetsPath)
        ]
        if self.externalTargetsPath:
            # Get paths to external targets
            paths += [
                (t, self.externalTargetsPath + t + os.sep)
                for t in os.listdir(self.externalTargetsPath)
            ]
        # Look in subdirectories only for the header file
        for path in paths:
            try:
                if not os.path.isfile(path[1]) and os.access(
                    path[1] + "header.html", os.R_OK
                ):
                    header = Header.factory(*path, builtinPath=self.builtinTargetsPath)
                    self.headers[header.id] = header
            except:
                pass


# start things up if we were called directly
if __name__ == "__main__":
    app = App()
    app.MainLoop()
