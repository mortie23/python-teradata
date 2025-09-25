create table
  GAME (
    GAME_ID integer not null
  , GAME_TYPE_ID integer not null
  , week integer
  , HOME_TEAM_ID integer
  , AWAY_TEAM_ID integer
  )
;

--, constraint GAME_ID_PK primary key (GAME_ID)
--, constraint GAME_GAME_TYPE_ID_FK foreign key (GAME_TYPE_ID) references PRD_ADS_PYTHON_NFL_DB.GAME_TYPE (GAME_TYPE_ID)