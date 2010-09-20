#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Reads from stdin and logs a note to a file"""
import sys
import optparse
import os
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

    if(len(options.subject) > 0):
        print "Taking notes on subject %s. ^D to quit." % options.subject
    else:
        print "Taking notes. ^D to quit."
    
    note = sys.stdin.readline() 
    while (len(note) != 0):
        for notefile in notefiles:
            notefile.write_note(options.subject, note)
        note = sys.stdin.readline()
        
    for notefile in notefiles:
        notefile.close()

if(__name__ == "__main__"):
    sys.exit(main())
