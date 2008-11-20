CREATE TABLE Errors
(
	ID	INTEGER PRIMARY KEY AUTOINCREMENT
	,ErrDate	DATE
	,Message	Text
	,Line	INTEGER
	,File	Varchar
	,CompDate	DATE
	,CompTime	TIME
);