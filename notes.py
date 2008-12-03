import datetime, time
import sqlite3

def openFile():
	return open('/home/gregorah/notes', 'a')

def writeNoteToFile(note):
	notesFile = openFile()
	notesFile.write(datetime.date.today().ctime())
	notesFile.write('\n')
	notesFile.write(note)
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

print "Taking notes..."
note = raw_input()
writeNote(note, True, True)


