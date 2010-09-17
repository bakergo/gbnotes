#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
"""Handles note interactions with a SQLite database"""

class NoteSqlite:
    """Abstraction of a sqlite database containing notes"""
    def __init__(self):
        """Initialize the list of databases to use"""
        self.databases = list()
    def open_note(self, path):
        """Open, create the required table Notes in the database"""
        sqldb = sqlite3.connect(path)
        sqldb.execute('CREATE TABLE IF NOT EXISTS Notes(time DATETIME, subj TEXT, note TEXT);')
        self.databases.append(sqldb)
    def close_note(self):
        """Close & commit data"""
        for sqldb in self.databases:
            sqldb.commit()
            sqldb.close()
            self.databases.remove(sqldb)
    def write_note(self, subject, note):
        """Write the note to the database"""
        for sqldb in self.databases:
            sqldb.execute('INSERT INTO Notes(time,subj, note) VALUES (current_timestamp, ?,?);', (subject, note))
