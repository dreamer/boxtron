#!/usr/bin/python3

"""
X11 related classes and functions.
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

import collections

from ctypes import *


class Xlib:
    """Adapter to X11 library."""

    def __init__(self):
        self.lib = CDLL("libX11.so.6")
        self.lib.XOpenDisplay.argtypes = [c_char_p]
        self.lib.XOpenDisplay.restype = c_void_p
        self.lib.XDisplayString.argtypes = [c_void_p]
        self.lib.XDisplayString.restype = c_char_p
        self.lib.XCloseDisplay.argtypes = [c_void_p]
        self.lib.XFree.argtypes = [c_void_p]
        self.lib.XFree.restype = c_int
        self.dpy = None

    def open_display(self):
        """Adapts: Display *XOpenDisplay(char *display_name);

        See: man 3 xopendisplay
        """
        self.dpy = self.lib.XOpenDisplay(None)
        return self.dpy

    def close_display(self):
        """Adapts: int XCloseDisplay(Display *);

        See: man 3 xopendisplay
        """
        return self.lib.XCloseDisplay(self.dpy)

    def free(self, ptr):
        """Adapts XFree."""
        return self.lib.XFree(ptr)

    def display_string(self):
        """Adapts XDisplayString."""
        return self.lib.XDisplayString(self.dpy).decode('ascii')


class XineramaScreenInfo(Structure):
    """struct XineramaScreenInfo

    Definition in /usr/include/X11/extensions/Xinerama.h
    """

    # pylint: disable=too-few-public-methods

    _fields_ = [('screen_number', c_int),
                ('x_org', c_short),
                ('y_org', c_short),
                ('width', c_short),
                ('height', c_short)]  # yapf: disable


ScreenInfo = collections.namedtuple('ScreenInfo', 'number width height x y')


class Xinerama:
    """Adapter to Xinerama X extension."""

    def __init__(self, xlib):
        self.xlib = xlib
        self.lib = CDLL("libXinerama.so.1")
        self.lib.XineramaIsActive.argtypes = [c_void_p]
        self.lib.XineramaIsActive.restype = c_bool
        self.lib.XineramaQueryScreens.argtypes = [c_void_p, POINTER(c_int)]
        self.lib.XineramaQueryScreens.restype = POINTER(XineramaScreenInfo)

    def is_active(self):
        """Adapts: Bool XineramaIsActive(Display *);

        See: man 3 xinerama
        """
        assert self.xlib.dpy
        return self.lib.XineramaIsActive(self.xlib.dpy)

    def query_screens(self):
        """ Adapts: XineramaScreenInfo *XineramaQueryScreens(Display*, int*);

        See: man 3 xinerama
        """
        dpy = self.xlib.dpy
        assert dpy
        num = c_int(0)
        xscreens = self.lib.XineramaQueryScreens(dpy, byref(num))
        screens = [
            ScreenInfo(s.screen_number, s.width, s.height, s.x_org, s.y_org)
            for s in xscreens[:num.value]
        ]
        self.xlib.free(xscreens)
        return screens


def query_screens():
    """Return dict of ScreenInfo objects describing available screens."""
    xlib = Xlib()
    dpy_ptr = xlib.open_display()
    if dpy_ptr is None:
        return {}
    xinerama = Xinerama(xlib)
    all_screens = xinerama.query_screens() if xinerama.is_active() else []
    xlib.close_display()
    return {str(screen.number): screen for screen in all_screens}
