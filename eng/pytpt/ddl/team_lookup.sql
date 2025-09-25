create table
  TEAM_LOOKUP (
    TEAM_ID integer not null
  , TEAM varchar(50) character set LATIN not CASESPECIFIC
  , TEAM_SHORT char(3) character set LATIN not CASESPECIFIC
  , CONFERENCE char(3) character set LATIN not CASESPECIFIC
  , DIVISION varchar(10) character set LATIN not CASESPECIFIC
  , constraint TEAM_ID_PK primary key (TEAM_ID)
  )
;