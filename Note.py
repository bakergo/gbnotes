#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Handles note interactions with files"""
import datetime
import sqlite3

class NoteFile:
    """Abstraction of a file containing notes"""
    def __init__(self, path):
        """Initialize the note file using the provided path"""
        self.open_file = None
        self.open_file = open(path, 'a')
    
    def close(self):
        """Close up the file, make sure it's closed"""
        if(self.open_file is not None):
            self.open_file.close()
            self.open_file = None
                
    def write_note(self, subject, note):
        """Write the note, format below"""
        self.open_file.write('%s: %s -- %s' % 
            (datetime.datetime.now().ctime(), subject, note))

class NoteSqlite:
    """Abstraction of a sqlite database containing notes"""
    def __init__(self, path):
        """Open, create the required table Notes in the database"""
        self.open_file = None
        sqldb = sqlite3.connect(path)
        sqldb.execute('CREATE TABLE IF NOT EXISTS Notes(time DATETIME, subj TEXT, note TEXT);')
        self.open_file = sqldb
        
    def close(self):
        """Close & commit data"""
        if(self.open_file is not None):
            self.open_file.commit()
            self.open_file.close()
            self.open_file = None
            
    def write_note(self, subject, note):
        """Write the note to the database"""
        if self.open_file is not None:
            self.open_file.execute('INSERT INTO Notes(time,subj, note) VALUES (current_timestamp, ?,?);', (subject, note))
