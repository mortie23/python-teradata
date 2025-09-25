create table
  PRD_ADS_PYTHON_NFL_DB.GAME_TYPE (
    GAME_TYPE_ID integer not null
  , GAME_TYPE char(3) character set LATIN not CASESPECIFIC
  , constraint GAME_TYPE_ID_PK primary key (GAME_TYPE_ID)
  )
;