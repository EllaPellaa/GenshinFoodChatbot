# Creating the Genshin Impact food database for the chatbot
#
# Usage: python create_food_db.py
# Output: food_db.db (SQLite database)
#

import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = "food_db.db"

if os.path.exists(DB_PATH):
  os.remove(DB_PATH)
  print(f"Removed existing database at {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the tables for the database
cursor.execute("""
CREATE TABLE 
""")