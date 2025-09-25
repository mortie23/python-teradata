create table
  PRD_ADS_PYTHON_NFL_DB.VENUE (
    VENUE_ID integer not null
  , VENUE_NAME varchar(50) character set LATIN not CASESPECIFIC
  , CAPACITY integer
  , SURFACE varchar(50) character set LATIN not CASESPECIFIC
  , VENUE_TYPE varchar(50) character set LATIN not CASESPECIFIC
  , constraint VENUE_ID_PK primary key (VENUE_ID)
  )
;