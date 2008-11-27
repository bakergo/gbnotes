import datetime, time

def openFile():
	return open('/home/gregorah/notes', 'a')

def writeNoteToFile(note):
	notesFile = openFile()
	notesFile.write(datetime.date.today().ctime())
	notesFile.write('\n')
	notesFile.write(note)
	notesFile.close()

def openDB()
	return sqlite3.connect('/home/gregorah/.notes.db')

def insertNote(notesDB, note)
	notesDB.execute('INSERT INTO Notes(time, note) VALUES (?,?)', (datetime.date.today().ctime(), note))

def writeNoteToDatabase(note):
	notesDB = openDB()
	insertNote(notesDB, note)
	notesdb.close();

def writeNote(note, writeFile, writeDatabase):
	if(writeFile):
		writeNoteToFile(note)
	if(writeDatabase):
		writeNoteToDatabase(note)

print "Taking notes..."
note = raw_input()
writeNote(note, True, False)


