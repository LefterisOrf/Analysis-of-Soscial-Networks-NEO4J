'AoSN_HW2' 

DB constraints:  
  CREATE CONSTRAINT uniqueAuthor IF NOT EXISTS
  ON (n:Author)
  ASSERT n.name IS UNIQUE

  CREATE CONSTRAINT uniqueAuthor IF NOT EXISTS
  ON (n:Publication)
  ASSERT n.title IS UNIQUE
