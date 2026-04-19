# Includes some helper tools for multiple files
#

# Normalization helper for ingredient names
def normalize_ingredient_name(name: str) -> str:
  """Normalize ingredient name and handle plurals."""
  name = name.lower().strip()

  if name.endswith("ies"):
    name = name[:-3] + "y"
  elif name.endswith("s"):
    name = name[:-1]

  return name