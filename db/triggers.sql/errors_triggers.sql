CREATE TRIGGER AFTER INSERT ON Errors
BEGIN
	UPDATE Errors
	SET ErrDate = DateTime('now')
	WHERE ID = new.ID;
END;
