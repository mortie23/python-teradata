create table
  PRD_ADS_PYTHON_NFL_DB.PLAYER (
    GAME_PLAYER_ID integer not null
  , week integer
  , GAME_ID integer not null
  , TEAM_ID integer not null
  , HOME_AWAY varchar(50) character set LATIN not CASESPECIFIC
  , PLAYER_NAME varchar(100) character set LATIN not CASESPECIFIC
  , FIELD_POSITION char(3) character set LATIN not CASESPECIFIC
  , RUSHING_ATTEMPTS integer
  , RUSHING_YARDS integer
  , RUSHING_TD integer
  , RECEIVING_TARGETS integer
  , RECEPTIONS integer
  , RECEIVING_YARDS integer
  , RECEIVING_TD integer
  , TOTAL_TD integer
  , FUMBLES integer
  , PASS_ATTEMPTS integer
  , PASS_COMPLETIONS integer
  , PASSING_YARDS integer
  , PASSING_TD integer
  , INTERCEPTIONS integer
  , constraint GAME_PLAYER_ID_PK primary key (GAME_PLAYER_ID)
    --, constraint PLAYER_GAME_ID_FK foreign key (GAME_ID) references PRD_ADS_PYTHON_NFL_DB.GAME (GAME_ID)
    --, constraint PLAYER_TEAM_ID_FK foreign key (TEAM_ID) references PRD_ADS_PYTHON_NFL_DB.TEAM_LOOKUP (TEAM_ID)
  )
;