#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import string
import sys
from string import Template as StdTemplate

class Template():
    """
        First read_template_file is used to load the template from a file. The method calls parse_template_string, which reads all the tags, saves the align values and removes the alignment tags from the template. set_template_string is then called and the string.Template object is created.
        set_data is used to give the values that will be used by the template for replacement. set_data goes over each value in the dict and applies the correct alignment according to the aligns dict.
        get_string invokes safe_substitute on the template.
    """

    def __init__(self, filename, short_status=False):
        # Holds alignment information
        self.aligns = {}
        # The template string
        self.template_string = ""
        # Holds the formatted values
        self.replace_dict = {}

        self.template = None

        # Boolean telling if short status strings should be displayed
        self.short_status = short_status

        self._read_template_file(filename)


    def _read_template_file(self, filename):
        try:
            f = open(filename, 'r')
        except IOError, ioe:
            print "Missing template file:"
            print ioe
            sys.exit(1)

        t_string = f.read()
        f.close()
        # :-1 is there to remove the new line at the end of the file
        self._parse_template_string(t_string[:-1])

    def _parse_template_string(self, template_string):
        """
            Parses a template string. First all tags are extracted using regular expressions. Then the alignment values are stored. Alignment information is removed from the template string.
        """
        tags = re.findall("\$\{[^}]*\}", template_string)

        self.aligns = {}
        for tag in tags:
            t = tag[2:-1].split(' ')
            # Check if there is any alignment info
            if len(t)==2:
                self.aligns[t[0]] = t[1]
                # removes the alignment info from the template:
                # For ex: replace "t_status l5" with "t_status"
                template_string = template_string.replace(tag[2:-1], t[0])

        #~ print "New template string:", template_string
        self._set_template_string(template_string)
        #~ print "Aligns:", self.aligns

    def _set_template_string(self, string):
        self.template_string = string
        self.template = StdTemplate(self.template_string)

    def set_data(self, data):
        """
            The data is saved and the alignments are applied.
        """
        #~ print "Data:",data

        for key, value in data.items():
            if key == "t_status" and self.short_status:
                value = self._shorten_status(value)
            alignedValue = self._apply_alignment(key, value)
            # Save the final, aligned value
            self.replace_dict[key] = alignedValue

        #~ print "Replace:",self.replace_dict

    def _shorten_status(self, status):
        """
            Returns the shortened versions of the status string.
        """
        #~ print "shortening"
        shorts = {}
        shorts["Stopped"] = "s"
        shorts["Verifying"] = "v"
        shorts["Up & Down"] = "ud"
        shorts["Downloading"] = "d"
        shorts["Seeding"] = "u"
        shorts["Idle"] = "i"

        return shorts[status]

    def _apply_alignment(self, key, value):
        """
            Using key looks up alignment info from the aligns dict. The alignment info (if any) is applied to the value.
            All tags except t_name:
            r - Right align
            l - Left align
            c - Center align
            t_name only:
            An integer X without a letter at the front - crop the name to X-3 characters long (+ last 3 characters are ellipsis)
            s - Add the conky scrolling tag to the name (currenty has no effect if the scrip updates each ~30 sec)
        """
        if key not in self.aligns:
            return value

        align = self.aligns[key]
        side = align[:1]

        if side not in "rlcns":
            side = "n" # crop
            align = "n"+align

        try:
            # get the number from the alignment
            padding = int(align[1:])
        except ValueError:
            print "Malformed alignment information for tag", key, ":", align
            return value

        if side=="r": # right align
            return value.rjust(padding)
        elif side=="l": # left align
            return value.ljust(padding)
        elif side=="c": # center align
            return value.center(padding)
        elif side=="n": # crop and add ellipsis
            return value[:(padding-3)]+"..."
        elif side=="s": # scroll
            return "${scroll "+str(padding)+" "+value+"}"
        else:
            return str(value)

    def get_string(self):
        return self.template.safe_substitute(self.replace_dict)
