create table "game" (
      "game_id" integer not null primary key,
    , "game_type_id" integer not null,
    , "WEEK" integer not null,
    , "HOME_TEAM_ID" integer not null,
    , "AWAY_TEAM_ID" integer not null
);