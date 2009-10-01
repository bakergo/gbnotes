#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, time
import sqlite3
import sys

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

def isWriteDb():
	for arg in sys.argv:
		if(arg == '--nodb'):
			return False
	return True

def isWriteFile():
	for arg in sys.argv:
		if(arg == '--nofile'):
			return False
	return True

def showHelp():
	for arg in sys.argv:
		if(arg == '-h'):
			print "Usage: note [-h] [--nodb] [--nofile] [SUBJ]"
			print "-h: display this help and exit."
			print "--nodb: does not use ~/.notes.db when writing a note."
			print "--nofile: does not use ~/notes when writing a note."
			exit()
def parseSubj():
	if(len(sys.argv) > 1):
		if(sys.argv[len(sys.argv)-1] != '--nodb' and sys.argv[len(sys.argv)-1] != '--nofile'):
			return sys.argv[len(sys.argv)-1]
		else:
			return ''
	else:
		return ''

def makeNoteFiles():
	notefiles = list()
	if(isWriteFile()):
		n = NoteFile()
		n.open_note("/home/gregorah/notes")
		notefiles.append(n)
	if(isWriteDb()):
		n = NoteSqlite()
		n.open_note("/home/gregorah/.notes.db")
		notefiles.append(n)
	return notefiles

showHelp()
print "Taking notes. ^D to quit."

notefiles = makeNoteFiles()
note = sys.stdin.readline()
subj = parseSubj()

while (len(note) != 0):
	for notefile in notefiles:
		notefile.write_note(subj,note)
	note = sys.stdin.readline()

for notefile in notefiles:
	notefile.close_note()
