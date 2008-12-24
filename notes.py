#!/usr/bin/python
import datetime, time
import sqlite3
import sys

def openFile():
	return open('/home/gregorah/notes', 'a')

def writeNoteToFile(note):
	notesFile = openFile()
	notesFile.write(datetime.date.today().ctime())
	notesFile.write('\n')
	notesFile.write(note)
	notesFile.write('\n\n')
	notesFile.close()

def ensureDB(conn):
	conn.execute('CREATE TABLE IF NOT EXISTS Notes(time DATETIME, note TEXT);')
	return conn

def openDB():
	return ensureDB(sqlite3.connect('/home/gregorah/.notes.db'))

def insertNote(notesDB, note):
	notesDB.execute('INSERT INTO Notes(time, note) VALUES (current_timestamp,?);', (note,))

def writeNoteToDatabase(note):
	notesDB = openDB()
	insertNote(notesDB, note)
	notesDB.commit()
	notesDB.close()

def writeNote(note, writeFile, writeDatabase):
	if(writeFile):
		writeNoteToFile(note)
	if(writeDatabase):
		writeNoteToDatabase(note)

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
			print "Usage: notes [--nodb] [--nofile]"
			print "--nodb: does not use ~/.notes.db when writing a note."
			print "--nofile: does not use ~/notes when writing a note."
			exit()
showHelp()
print "Taking notes..."
note = raw_input()

writeNote(note, isWriteFile(), isWriteDb())

