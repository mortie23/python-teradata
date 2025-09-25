create table
  PRD_ADS_PYTHON_NFL_DB.GAME_VENUE (
    GAME_VENUE_ID integer not null
  , GAME_ID integer not null
  , VENUE_ID integer not null
  , constraint GAME_VENUE_ID_PK primary key (GAME_VENUE_ID)
    --, constraint GAME_VENUE_GAME_ID_FK foreign key (GAME_ID) references PRD_ADS_PYTHON_NFL_DB.GAME (GAME_ID)
    --, constraint GAME_VENUE_VENUE_ID_FK foreign key (VENUE_ID) references PRD_ADS_PYTHON_NFL_DB.VENUE (VENUE_ID)
  )
;