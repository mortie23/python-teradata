create table
  WEATHER (
    WEATHER_GAME_ID integer not null
  , GAME_ID integer not null
  , TEMPERATURE integer
  , WEATHER_CONDITION varchar(50) character set LATIN not CASESPECIFIC
  , WIND_SPEED integer
  , HUMIDITY integer
  , WIND_DIRECTION char(3) character set LATIN not CASESPECIFIC
  , constraint WEATHER_GAME_ID_PK primary key (WEATHER_GAME_ID)
  )
;

--, constraint WEATHER_GAME_ID_FK foreign key (GAME_ID) references PRD_ADS_PYTHON_NFL_DB.GAME (GAME_ID)