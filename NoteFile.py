#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Handles note interactions with a file"""
import datetime

class NoteFile:
    """Abstraction of a file containing notes"""
    def __init__(self):
        """Initialize the note file"""
        self.open_files = list()
    def open_note(self, path):
        """Open up the file, append onry"""
        self.open_files.append(open(path, 'a'))
    def close_note(self):
        """Close up the file, make sure it's closed"""
        for open_file in self.open_files:
            open_file.close()
            self.open_files.remove(open_file)
    def write_note(self, subject, note):
        """Write the note, format below"""
        for open_file in self.open_files:
            open_file.write('%s: %s -- %s' % 
            (datetime.datetime.now().ctime(), subject, note))
