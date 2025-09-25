create table
  GAME_STATS (
    GAME_TEAM_ID integer not null
  , GAME_ID integer not null
  , TEAM_ID integer not null
  , TOTAL_FIRST_DOWNS integer
  , PASSING_FIRST_DOWNS integer
  , RUSHING_FIRST_DOWNS integer
  , PENALTY_FIRST_DOWNS integer
  , THIRD_DOWN_ATTEMPTS integer
  , THIRD_DOWN_CONVERSIONS integer
  , THIRD_DOWN_CONVERSION_PERC decimal(10, 5)
  , THIRD_DOWN_PASSING_CONVERSIONS integer
  , THIRD_DOWN_RUSHING_CONVERSIONS integer
  , THIRD_DOWN_PENALTY_CONVERSIONS integer
  , FOURTH_DOWN_ATTEMPTS integer
  , FOURTH_DOWN_CONVERSIONS integer
  , FOURTH_DOWN_CONVERSION_PERC decimal(10, 5)
  , FOURTH_DOWN_PASSING_CONVERSIONS integer
  , FOURTH_DOWN_RUSHING_CONVERSIONS integer
  , FOURTH_DOWN_PENALTY_CONVERSIONS integer
  , TOTAL_PLAYS integer
  , TOTAL_YARDS integer
  , YARDS_PER_PLAY decimal(10, 5)
  , RUSHING_PLAYS integer
  , RUSHING_YARDS integer
  , RUSHING_YARDS_PER_PLAY decimal(10, 5)
  , PASSING_PLAYS integer
  , PASSING_COMPLETIONS integer
  , PASSING_YARDS_PER_PLAY decimal(10, 5)
  , INTERCEPTIONS integer
  , SACKS integer
  , NET_PASSING_YARDS integer
  , GROSS_PASSING_YARDS integer
  , SACK_YARDS integer
  , TOTAL_RETURN_YARDS integer
  , PUNT_RETURNS integer
  , PUNT_RETURN_YARDS integer
  , KICK_OFF_RETURNS integer
  , KICK_OFF_RETURN_YARDS integer
  , INTERCEPTION_RETURNS integer
  , INTERCEPTION_RETURN_YARDS integer
  , KICK_OFFS integer
  , KICK_OFFS_IN_ENDZONE integer
  , TOUCHBACKS integer
  , PUNTS integer
  , AVERAGE_PUNT_YARDS integer
  , PUNTS_BLOCKED integer
  , AVERAGE_NET_PUNT_YARDS integer
  , PENALTIES integer
  , PENALTY_YARDS integer
  , FUMBLES integer
  , FUMBLES_LOST integer
  , TOTAL_TD integer
  , PASSING_TD integer
  , RUSHING_TD integer
  , INTERCEPTION_TD integer
  , FUMBLE_TD integer
  , PUNT_RETURN_TD integer
  , KICK_OFF_RETURN_TD integer
  , FIELD_GOAL_RETURN_TD integer
  , EXTRA_POINT_ATTEMPTS integer
  , EXTRA_POINTS_MADE integer
  , EXTRA_POINTS_BLOCKED integer
  , TWO_POINT_CONVERSION_ATTEMPTS integer
  , TWO_POINT_CONVERSIONS_MADE integer
  , FIELD_GOAL_ATTEMPTS integer
  , FIELD_GOALS_MADE integer
  , FIELD_GOALS_BLOCKED integer
  , REDZONE_VISITS integer
  , REDZONE_TD integer
  , REDZONE_EFFICIENCY integer
  , GOAL_TO_GO_ATTEMPTS integer
  , GOAL_TO_GO_TD integer
  , GOAL_TO_GO_EFFICIENCY integer
  , SAFETIES integer
  , TURNOVERS integer
  , POINTS_SCORED integer
  , TIME_OF_POSSESION varchar(10)
  , WIN_LOSS char(1)
  , constraint GAME_TEAM_ID_PK primary key (GAME_TEAM_ID)
  )
;

--, constraint GAME_STATS_GAME_ID_FK foreign key (GAME_ID) references PRD_ADS_PYTHON_NFL_DB.GAME (GAME_ID)
--, constraint GAME_STATS_TEAM_ID_FK foreign key (TEAM_ID) references PRD_ADS_PYTHON_NFL_DB.TEAM_LOOKUP (TEAM_ID)