#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, time
import sqlite3
import sys
import optparse
import os

class NoteFile:
	def __init__(self):
		self.open_files = list()
	def open_note(self, path):
		self.open_files.append(open(path, 'a'))
	def close_note(self):
		for open_file in self.open_files:
			open_file.close()
			self.open_files.remove(open_file)
	def write_note(self, subject, note):
		for open_file in self.open_files:
				open_file.write('%s: %s -- %s' % (datetime.datetime.now().ctime(),subject,note))

class NoteSqlite:
	def __init__(self):
		self.databases = list()
	def open_note(self, path):
		db = sqlite3.connect(path)
		db.execute('CREATE TABLE IF NOT EXISTS Notes(time DATETIME, subj TEXT, note TEXT);')
		self.databases.append(db)
	def close_note(self):
		for db in self.databases:
			db.commit()
			db.close()
			self.databases.remove(db)
	def write_note(self, subject, note):
		for db in self.databases:
			db.execute('INSERT INTO Notes(time,subj, note) VALUES (current_timestamp, ?,?);', (subject,note))

def parseSubj(args):
	if(len(args) > 0):
		return args[0]
	else:
		return ''

parser = optparse.OptionParser(usage='Take notes and store them in a database')
parser.add_option('--nodb',default=False,action='store_true', help='Does not use the database when writing a note.')
parser.add_option('--nofile',default=False, action='store_true', help='Does not use the notes file when writing a note.')
parser.add_option('--db', default='~/.notes.db', type="string", help='Specify the database file used')
parser.add_option('--file', default='~/notes.txt', type="string", help='Specify the note text file used')

(options, arguments) = parser.parse_args()

notefiles = list()
if(not options.nofile):
	n = NoteFile()
	n.open_note(os.path.expanduser(options.file))
	notefiles.append(n)
if(not options.nodb):
	n = NoteSqlite()
	n.open_note(os.path.expanduser(options.db))
	notefiles.append(n)

print "Taking notes. ^D to quit."

note = sys.stdin.readline()
subj = parseSubj(arguments)

while (len(note) != 0):
	for notefile in notefiles:
		notefile.write_note(subj,note)
	note = sys.stdin.readline()

for notefile in notefiles:
	notefile.close_note()
