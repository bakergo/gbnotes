#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Reads from stdin and logs a note to a file"""
import sys
import optparse
import os
import subprocess
import tempfile
from Note import NoteFile, NoteSqlite

def main():
    """Run the arguments, then write the notes until the stream is
    finished parsing out"""
    parser = optparse.OptionParser(
        usage='Take notes and store them in a database')
    parser.add_option('--nodb', default=False, action='store_true', 
        help='Does not use the database when writing a note.')
    parser.add_option('--nofile', default=False, action='store_true', 
        help='Does not use the notes file when writing a note.')
    parser.add_option('-d', '--database', default='~/.notes.db', 
        type="string", help='Specify the database file used')
    parser.add_option('-f', '--file', default='~/notes.txt', 
        type="string", help='Specify the note text file used')
    parser.add_option('-s', '--subject', default='', type="string",
        help='Specify the subject of the note to be taken')

    (options, arguments) = parser.parse_args()

    notefiles = list()
    if(not options.nofile):
        notefiles.append(NoteFile(os.path.expanduser(options.file)))
    if(not options.nodb):
        notefiles.append(NoteSqlite(os.path.expanduser(options.database)))

    tmpfile = tempfile.NamedTemporaryFile(suffix='.txt', prefix='note-',
            delete=False)
    print >> tmpfile
    print >> tmpfile , '# Write your notes, one per line, and be satisfied'
    print >> tmpfile , '# Lines beginning with # will be ignored'
    tmpfile.close()
    subprocess.call(['editor', tmpfile.name])
    with open(tmpfile.name) as writtenfile:
        for note in writtenfile:
            note = note.strip()
            if len(note > 0 and note[0] != '#'):
                for notefile in notefiles:
                    notefile.write_note(options.subject, note.strip())
    os.remove(tmpfile.name)
    for notefile in notefiles:
        notefile.close()

if(__name__ == "__main__"):
    sys.exit(main())
