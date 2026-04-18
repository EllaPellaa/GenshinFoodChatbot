# Making connection to the database with sqlite3

import sqlite3

DB_PATH = "food_db.db"

def get_db():
  """Get a database connection with Row factory for dict-like access."""
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn