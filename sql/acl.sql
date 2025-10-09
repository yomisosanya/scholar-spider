-- Access Control List

USE DATABASE cuny_research_record;

-- User Types

  -- generic roles
  CREATE ROLE member LOGIN;
  CREATE ROLE guest;

  -- admin users
  CREATE ROLE user1;
  CREATE ROLE user2;
  CREATE ROLE user3;


-- Permissions Section

GRANT admin TO user1 WITH INHERIT TRUE;
GRANT admin TO user2 WITH INHERIT TRUE;
GRANT admin TO user3 WITH INHERIT TRUE;








