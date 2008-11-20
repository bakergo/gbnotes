#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define DEFAULT_FILE "notes"
#define DEFAULT_DB "/var/local/notes/notes.db"
#define STDIN_CHARS 512
#define FILE_IS_DEFAULT 1
#define CLEAR_FILE 2
#define STDIN 4
#define USEDB 8
#define bool char
#define TRUE 1
#define FALSE 0


char* writeFile = NULL;
char* dbFile = NULL;
int settings;


void error(const char* errMsg, const int line, const char* file,
	const bool fatal, const int exitCode)
{
	fprintf(stderr, "Error at line %d in file %s\n:%s\n",line,file,errMsg);
	if(fatal)
		exit(exitCode);
}

int parseArgs(int argc, char** args)
{
	char options = 1;
	settings = 0 | FILE_IS_DEFAULT;
	int i,j,p;
	for(p=i=1; i<argc && options; i=++p)
	{
		if(args[i][0] == '-')
		{
			for(j=0; args[i][j] != 0; j++)
			{
				switch(args[i][j])
				{
					case 'o':
						settings &= !FILE_IS_DEFAULT;
						writeFile=args[++p];
						break;
					case 'c':
						settings |= CLEAR_FILE;
						break;
					case 'i':
						settings |= STDIN;
						break;
					case 'd':
						settings |= USEDB;
						dbFile=args[++p];
						break;
				}
			}
		}
		else
		{
			options = 0;
			return p;
		}

	}

	settings |= (i==argc)<<2;
	return p;
}

void getFile()
{
	if(settings & FILE_IS_DEFAULT)
	{
		char* fileTmp = getenv("HOME");
		writeFile = malloc(strlen(fileTmp)+strlen(DEFAULT_FILE)+2);
		strcpy(writeFile, fileTmp);
		if(fileTmp[strlen(fileTmp)] != '/')
			strcat(writeFile, "/");
		strcat(writeFile, DEFAULT_FILE);
	}
	//else the file is specified; if they gave an invalid file
	//NOT MY PROBLEM KTHX
}

void getDB()
{
	if((settings & USEDB) && (!dbFile))
	{
		dbFile = DEFAULT_DB;
	}
}

FILE* openFile()
{
	FILE* fp;
	char* fileMode = "a";
	if(settings & CLEAR_FILE)
		fileMode = "w";
	fp=fopen(writeFile, fileMode);
	if(!fp)
	{
		const char* errFormat = "could not open file %s in mode %s";
		char* errMsg = malloc(strlen(errFormat)+strlen(writeFile)
							+strlen(fileMode));
		sprintf(errMsg, errFormat, writeFile, fileMode);
		error(errMsg, __LINE__, __FILE__, TRUE, 1);
		exit (1);
	}
	return fp;
}

void timeStamp(FILE* fp)
{
	time_t rawtime;
	time(&rawtime);
	fprintf(fp,"\n%s",ctime(&rawtime));
}

void kbInput(FILE* fp)
{
	printf("%s\n", "Taking notes...");
	char uIn[STDIN_CHARS];
	fgets(uIn, STDIN_CHARS,stdin);
	fprintf(fp,"%s", uIn);
	printf("%s", uIn);

}

void writeArgs(const int argc,  char * const *args, int i, FILE* fp)
{
	if(i<argc)
		fprintf(fp, "%s", args[i++]);
	for(;i<argc-1; i++)
		fprintf(fp," %s",args[i]);
}

void closeFile(FILE* fp)
{
	fputs("\n", fp);
	if(fclose(fp) == EOF)
	{
		error("failure while closing file", __LINE__, __FILE__, TRUE, 2);
		exit (2);
	}
}

int main (int argc, char** args)
{
	int argNum = parseArgs(argc, args);
	getFile();
	FILE* fp = openFile();
	timeStamp(fp);
	writeArgs(argc, args, argNum, fp);
	if(settings & STDIN)
		kbInput(fp);
	closeFile(fp);
	return 0;
}
