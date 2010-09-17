#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Reads from stdin and logs a note to a file"""
import datetime
import sqlite3
import sys
import optparse
import os

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
				open_file.write('%s: %s -- %s' % (datetime.datetime.now().ctime(), subject, note))

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
		
def main():
	"""Run the arguments, then write the notes until the stream is
	finished parsing out"""
	parser = optparse.OptionParser(
		usage='Take notes and store them in a database')
	parser.add_option('--nodb', default=False, action='store_true', 
		help='Does not use the database when writing a note.')
	parser.add_option('--nofile', default=False, action='store_true', 
		help='Does not use the notes file when writing a note.')
	parser.add_option('--db', default='~/.notes.db', type="string", 
		help='Specify the database file used')
	parser.add_option('--file', default='~/notes.txt', type="string", 
		help='Specify the note text file used')

	(options, arguments) = parser.parse_args()

	notefiles = list()
	if(not options.nofile):
		fnote = NoteFile()
		fnote.open_note(os.path.expanduser(options.file))
		notefiles.append(fnote)
	if(not options.nodb):
		dbnote = NoteSqlite()
		dbnote.open_note(os.path.expanduser(options.db))
		notefiles.append(dbnote)

	subj = ' '.join(arguments)
	if(len(subj > 0)):
		print "Taking notes on subject %s. ^D to quit." % subj
	else:
		print "Taking notes. ^D to quit."
	
	note = sys.stdin.readline()	
	while (len(note) != 0):
		for notefile in notefiles:
			notefile.write_note(subj, note)
		note = sys.stdin.readline()

	for notefile in notefiles:
		notefile.close_note()
if(__name__ == "__main__"):
	sys.exit(main())
