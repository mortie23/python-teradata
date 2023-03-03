# %%
user = "MORTCH"
password = user
host = "tdvm"
database = "PRD_ADS_PYTHON_NFL_DB"

# %%
# This one works for reading Teradata out of the box
import teradatasql
import csv
import pandas as pd

con = teradatasql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
)

# %%
query = f"""
select 
  TableName
  , count(*) as ColumnCount 
from 
  dbc.columnsv
where 
  databasename='{database}'
group by 
  TableName
order by 
  TableName
"""
tables = pd.read_sql(query, con)

# %%
# Order
order = pd.DataFrame(
    [
        [1, "GAME_TYPE"],
        [2, "GAME"],
        [3, "WEATHER"],
        [4, "VENUE"],
        [5, "GAME_VENUE"],
        [6, "TEAM_LOOKUP"],
        [7, "GAME_STATS"],
        [8, "PLAYER"],
    ],
    columns=["order", "TableName"],
)

table_load = tables.merge(order, how="right", on="TableName")

# %%
# Loading data
cur = con.cursor()


# %%
def insert_rows_from_csv(
    tablename: str,
    columncount: int,
):
    """Insert rows from a CSV into a Teradat table

    Args:
        tablename (str): the name of the table
        columncount (int): the number of columns in the table
    """
    columncount_questionmark = ", ?" * (columncount - 1)
    exec_string = f"{{fn teradata_read_csv(./data/{tablename.lower()}.csv)}}insert into {tablename} (?{columncount_questionmark})"
    cur.execute(exec_string)


# %%
# Load all tables
for index, row in table_load.iterrows():
    print(row["TableName"], row["ColumnCount"])
    insert_rows_from_csv(row["TableName"], row["ColumnCount"])

# %%
query = "select * from player"
df = pd.read_sql(query, con)
df

# %%
# Truncate all tables
table_load = table_load.sort_values(by="order", ascending=False)
for index, row in table_load.iterrows():
    print(row["TableName"])
    cur.execute(f"delete from {row['TableName']}")
# %%
