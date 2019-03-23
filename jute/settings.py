import jute.config

import wx


class SettingsBase(object):
    """
    Base class for storing settings.

    Settings are accessed via an attribute style interface and acceptable
    attributes and their defaults are given in _KEYS.
    """

    def __init__(self):
        self._wxConfig = wx.Config(jute.config.NAME).Get()
        self._wxConfigRead = {
            wx.ConfigBase.EntryType.Type_Boolean: self._wxConfig.ReadBool,
            wx.ConfigBase.EntryType.Type_Float: self._wxConfig.ReadFloat,
            wx.ConfigBase.EntryType.Type_Integer: self._wxConfig.ReadInt,
            wx.ConfigBase.EntryType.Type_String: self._wxConfig.Read,
            wx.ConfigBase.EntryType.Type_Unknown: self._wxConfig.Read,
        }
        self._wxConfigWrite = {
            bool: self._wxConfig.WriteBool,
            float: self._wxConfig.WriteFloat,
            int: self._wxConfig.WriteInt,
            str: self._wxConfig.Write,
        }

    def _add(self, name, path, default):
        self._KEYS[name] = (path, default)

    def __getattr__(self, name):
        if name[0] is '_':
            return self.__dict__[name]
        elif name in self._KEYS:
            key = self._KEYS[name][0]
            if self._wxConfig.Exists(key):
                entryType = self._wxConfig.GetEntryType(key)
                return self._wxConfigRead[entryType](key)
            else:
                return self._KEYS[name][1]
        else:
            raise KeyError()

    def __setattr__(self, name, value):
        if name[0] is '_':
            self.__dict__[name] = value
        elif name in self._KEYS:
            write = self._wxConfigWrite.get(
                type(value), self._wxConfig.Write)
            write(self._KEYS[name][0], value)
        else:
            raise KeyError()

    _KEYS = {}


class ApplicationSettings(SettingsBase):
    """
    Settings class for application-specific or unparented settings.
    """

    def __init__(self):
        super(ApplicationSettings, self).__init__()
        self._add('flat_style', '/application/style/flat', False)
