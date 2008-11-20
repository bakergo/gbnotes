#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define DEFAULT_FILE "notes"
#define STDIN_CHARS 512
#define FILE_IS_DEFAULT 1
#define CLEAR_FILE 2
#define STDIN 4
char* writeFile;
int settings;

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
						settings = settings & 
						!FILE_IS_DEFAULT;

						writeFile=args[++p];
						break;

					case 'c':
						settings |= CLEAR_FILE;
						break;
					case 'i':
						settings |= STDIN;
				}
			}
		}
		else
		{
			options = 0;
			return p;
		}

	}
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
	//else the file is specified; They gave an invalid file
	//NOT MY PROBLEM KTHX
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
		fprintf(stderr, "Could not open file %s in mode %s",writeFile,fileMode);
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
}

int main (int argc, char** args)
{
	int i = parseArgs(argc, args);
	settings |= (i==argc)<<2;
	getFile();
	FILE* fp = openFile();
	timeStamp(fp);
	for(;i<argc; i++)
		fprintf(fp,(i+1==argc)?"%s" : "%s ",args[i]);
	if(settings & STDIN)
		kbInput(fp);
	fputs("\n", fp);
	if(fclose(fp)==EOF)
	{
		fputs("failure while closing file", stderr);
		exit (2);
	}

	return 0;
}
