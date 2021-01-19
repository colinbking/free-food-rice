import os
from facebook_food import *
import psycopg2
import psycopg2.extras

from urllib.parse import urlparse, unquote
from dotenv import load_dotenv, find_dotenv
load_dotenv('.env')

import datetime as dt
from datetime import datetime
from pytz import timezone
url = urlparse(os.getenv("DATABASE_URL"))
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# # cur.execute("""
# #             CREATE TABLE events (
# #                 id INTEGER PRIMARY KEY,
# #                 name TEXT,
# #                 about TEXT,
# #                 time TEXT,
# #                 location TEXT,
# #                 food TEXT
# #                 )
# #             """

# #         )

# # s = ""
# # s += "SELECT"
# # s += " table_schema"
# # s += ", table_name"
# # s += " FROM information_schema.tables"
# # s += " WHERE "
# # s += " ORDER BY table_schema, table_name;"






# insert_sql = "INSERT INTO events(name, about, time, location, food) VALUES ('test', 'test', 'test', 'test', 'asdf');"
cur.execute("SELECT name, about, time, location, food, added_date FROM EVENTS")
events = []
ans = cur.fetchall()
for row in ans:
    events.append(row)
print(type(events), type(events[1]))

# print(res)
# cur.execute("SELECT * FROM /EVENTS WHERE name = 'test';")
# print(cur.fetchall())



# url = "https://m.facebook.com/groups/bakercollege"
# fs = FoodScraper(USERNAME, PWD)
# events = (fs.connect_and_scrape(url))

conn.close()

# today = dt.datetime.now(timezone('US/Central'))
# print(str(today)[0:11])