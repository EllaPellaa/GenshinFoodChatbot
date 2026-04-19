# The tools the LLM can use
#

from services import find_foods_by_ingredient, get_schema, get_all_foods, get_food_by_id, get_food_by_name, get_all_ingredients, get_ingredient_by_name, get_ingredients_for_food

def get_schema_tool():
  """Get database schema showing all tables and columns"""
  result = get_schema()
  return result

# Get all foods tool
def get_all_foods_tool():
  """Get all foods from the database."""
  result = get_all_foods()

  if not result:
    return {"found": False, "foods": []}
  
  return {"found": True, "foods": result}

# Get food by id tool
def get_food_by_id_tool(food_id: int):
  """Get a food item from the database by id."""
  result = get_food_by_id(food_id)

  if not result:
    return {"found": False, "food": None}
  
  return {"found": True, "food": result}

# Get food by name tool
def get_food_by_name_tool(food_name: str):
  """Get food items from the database by name."""
  result = get_food_by_name(food_name)

  if not result:
    return {"found": False, "foods": []}
  
  return {"found": True, "foods": result}

# Find food by ingredient tool
def find_foods_by_ingredient_tool(ingredient_name: str):
  """Find food items from the database by ingredient name."""
  result = find_foods_by_ingredient(ingredient_name)

  if not result:
    return {"found": False, "foods": []}
  
  return {"found": True, "foods": result}

# Get all ingredients tool
def get_all_ingredients_tool():
  """Get all ingredients from the database."""
  result = get_all_ingredients()

  if not result:
    return {"found": False, "ingredients": []}
  
  return {"found": True, "ingredients": result}

# Get ingredient by name tool
def get_ingredient_by_name_tool(ingredient_name: str):
  """Find ingredient from database by name."""
  result = get_ingredient_by_name(ingredient_name)
  if not result:
    return {"found": False, "ingredients": []}
  
  return {"found": True, "ingredients": result}

# Get all ingredients and their amounts for a specific food by id
def get_ingredients_for_food_tool(food_name: str):
  """Get all ingredients and their amounts for a food item by name"""
  result = get_ingredients_for_food(food_name)
  if not result:
    return {"found": False, "ingredients": []}
  
  return {"found": True, "ingredients": result}