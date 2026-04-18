# All statements for querying the database.
#

from db import get_db

def get_schema() -> str:
  """Database schema showing all tables and columns"""
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
  schemas = [row[0] for row in cursor.fetchall() if row[0]]
  conn.close()
  return "\n\n".join(schemas)

def get_all_foods():
  """Get all foods from the database."""
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM foods")
  foods = [dict(row) for row in cursor.fetchall()]
  conn.close()
  return foods 

def get_food_by_id(food_id):
  """Get a food item from the database by id."""
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM foods WHERE id = ?", (food_id,))
  food = cursor.fetchone()
  conn.close()
  return dict(food) if food else None

def get_food_by_name(food_name):
  """Get food items from the database by name."""
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM foods WHERE LOWER(name) LIKE LOWER(?)", (f"%{food_name}%",)
)
  foods = [dict(row) for row in cursor.fetchall()]
  conn.close()
  return foods

def find_foods_by_ingredient(ingredient_name):
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("""
    SELECT f.*
    FROM foods f
    JOIN food_ingredients fi ON f.id = fi.food_id
    JOIN ingredients i ON i.id = fi.ingredient_id
    WHERE LOWER(i.name) = LOWER(?)
  """, (ingredient_name,))
  foods = [dict(row) for row in cursor.fetchall()]
  conn.close()
  return foods