#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

class ColorCode:
    """
        Reads color for torrent's state from a file. Colorize a string depending on the status of a torrent.
    """

    def __init__(self, color_filename):
        self.color_code = {}
        if color_filename:
            self._read_colorcode(color_filename)

    def _read_colorcode(self, color_filename):
        try:
            f = open(color_filename, 'r')
        except IOError, ioe:
            print "Missing color code file:"
            print ioe
            sys.exit(1)

        colorcode_string = f.read()
        f.close()

        lines = colorcode_string.split('\n')
        del lines[-1]
        for l in lines:
            if "=" in l:
                pair = l.split('=')
                self.color_code[pair[0]] = pair[1]

    def colorize(self, torrent, string):
        """
            Colorizes a string depending on the state of the torrent
        """
        t_status = torrent['t_status']
        if t_status in self.color_code:
            color = self.color_code[t_status]
            return "${color "+color+"}"+string
        else:
            return string



