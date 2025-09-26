create table
  VENUE (
    VENUE_ID integer not null
  , VENUE_NAME varchar(50) character set unicode
  , CAPACITY integer
  , SURFACE varchar(50) character set unicode
  , VENUE_TYPE varchar(50) character set unicode
  , constraint VENUE_ID_PK primary key (VENUE_ID)
  )
;