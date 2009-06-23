#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, time
import sqlite3
import sys

class noteFile:
	def open_note(self):
		self.f = open('/home/gregorah/notes', 'a')
		
	def close_note(self):
		self.f.close()
		
	def write_note(self, note):
		self.f.write('%s: %s' % (datetime.datetime.now().ctime(), note))

class noteDb:
	def open_note(self):
		self.db = sqlite3.connect('/home/gregorah/.notes.db')
		self.db.execute('CREATE TABLE IF NOT EXISTS Notes(time DATETIME, note TEXT);')

	def close_note(self):
		self.db.commit()
		self.db.close()

	def write_note(self, note):
		self.db.execute('INSERT INTO Notes(time, note) VALUES (current_timestamp, ?);', (note,))

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
			print "Usage: notes [-h] [--nodb] [--nofile]"
			print "-h: display this help and exit."
			print "--nodb: does not use ~/.notes.db when writing a note."
			print "--nofile: does not use ~/notes when writing a note."
			exit()

def makeNoteFiles():
	notefiles = list()
	if(isWriteFile()):
		notefiles.append(noteFile())
	if(isWriteDb()):
		notefiles.append(noteDb())
	for notefile in notefiles:
		notefile.open_note()
	return notefiles

showHelp()
print "Taking notes..."

notefiles = makeNoteFiles()
note = sys.stdin.readline()

while (len(note) != 0):
	for notefile in notefiles:
		notefile.write_note(note)
	note = sys.stdin.readline()

for notefile in notefiles:
	notefile.close_note()
	