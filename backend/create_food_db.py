# Creating the Genshin Impact food database for the chatbot
#
# Usage: python create_food_db.py
# Output: food_db.db (SQLite database)
#

import sqlite3
import os

DB_PATH = "food_db.db"

if os.path.exists(DB_PATH):
  os.remove(DB_PATH)
  print(f"Removed existing database at {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ----- Create the tables for the database -----

# Table for food items
cursor.execute("""
  CREATE TABLE foods(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      description TEXT,
      rarity INTEGER,
      effects TEXT
  )
""")

# Table for ingredients
cursor.execute("""
  CREATE TABLE ingredients(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE NOT NULL
  )
""")

# Table for the many-to-many relationship between foods and ingredients
cursor.execute("""
  CREATE TABLE food_ingredients(
      food_id INTEGER,
      ingredient_id INTEGER,
      amount INTEGER,
      FOREIGN KEY (food_id) REFERENCES foods(id),
      FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
  )
""")

# ----- Insert some data to the database -----

# Ingredients
ingredients = [
    ("Carrot",),
    ("Shrimp Meat",),
    ("Calla Lily",),
    ("Mint",),
    ("Radish",),
    ("Cheese",),
    ("Tofu",),
    ("Crab Roe",),
    ("Crab",),
    ("Lotus Head",),
    ("Ham",),
    ("Apple",),
    ("Pinecone",),
    ("Jam",),
    ("Butter",),
    ("Sweet Flower",),
    ("Cabbage",),
    ("Salt",),
    ("Pepper",),
    ("Jueyun Chili",),
    ("Mushroom",),
    ("Bird Egg",),
    ("Sugar",),
    ("Milk",),
    ("Flour",),
    ("Rice",),
    ("Fish",),
    ("Fowl",),
    ("Raw Meat",),
    ("Onion",),
    ("Tomato",),
    ("Potato",),
]

cursor.executemany("""
    INSERT INTO ingredients (name)
    VALUES (?)
""", ingredients)

# Foods
foods = [
    (
        "Sweet Madame",
        "Honey-roasted fowl. The honey and sweet flowers come together to complement the tender fowl meat.",
        2,
        "Restores 20 - 24% of Max HP and an additional 900 - 1,500 HP to the selected character."
    ),
    (
        "Mondstadt Hash Brown",
        "A fried cake of mashed potatoes. A little bit of pinecone helps give it a nice crunch, and great with a bit of jam. Loved by people of all ages.",
        3,
        "Restores 30 - 34% of Max HP and an additional 600 - 1,900 HP to the selected character."
    ),
    (
        "Satisfying Salad",
        "A vegetable salad. Not just steamed potatoes and fresh vegetables, but also a hard-boiled egg to top it off. Satisfying to both the eyes and stomach.",
        2,
        "Increases all party members\\' CRIT Rate by 6 - 12% for 300s."
    ),
    (
        "Jade Parcels",
        "An exquisite-looking dish. The ham\\'s sweetness is locked inside the fresh vegetables, drizzled with a spicy broth. Delicious is an understatement.",
        4,
        "Increases all party members\\' ATK by 224 - 320 and CRIT Rate by 6 - 10% for 300 seconds."
    ),
    (
        "Crab Roe Tofu",
        "A dish with a tender mouthfeel. Crab roe is stir-fried till the oil within oozes out before being added to boiled tofu and accented with broth. Simple, yes, but gloriously fresh.",
        2,
        "Revives a character and restores 400 HP."
    ),
    (
        "Mushroom Pizza",
        "A pizza covered in cheese and mushrooms. It\\'s a party in your mouth and the cheese and mushrooms invited all their delicious friends.",
        3,
        "Restores 26 - 30% of Max HP to the selected character. Regenerates 450 - 790 HP every 5s for the next 30s."
    ),
    (
        "Radish Veggie Soup",
        "Radish-based vegetable soup. Its flavor is delicately between tart and sweet. With luscious radish, it\\'s a well-balanced dish.",
        1,
        "Restores 8 - 10% of Max HP to the selected character. Regenerates 210 - 300 HP every 5s for the next 30s."
    ),
    (
        "Qingce Stir Fry",
        "A dish cooked over a roaring fire. They say it was originally just a rustic dish that everyone in Qingce Village knew how to make. But quite unexpectedly, its crispy and spicy dishes gained the recognition of people from elsewhere, and thus began to spread throughout the Liyue region.",
        3,
        "Increases all party members\\' ATK by 160 - 228 for 300s."
    ),
    (
        "Rice Pudding",
        "A dessert made from rice. The soft, sticky rice and the sweet milk have melded together perfectly, Their tastes complimenting each other. If you eat it hot, you can enjoy the dense rice grains, and if you leave it till its cold, you can savor the gentle fragrance of milk - each possessing its own beauty. People who eat such a dish cannot help but wonder: how many experiments led up to this moment?",
        3,
        "Restores 85 - 100 Stamina."
    ),
    (
        "Calla Lily Seafood Soup",
        "A balanced combination of seafood. The delicacy of crab and mint make for a clear soup, and the calla lily brings it a refreshing taste.",
        3,
        "Increases all party members\\' DEF by 165 - 235 for 300s."
    ),
    (
        "Barbatos Ratatouille",
        "A simple chowder with a long history. The ingredients are similarly traditional and simple. No matter where you are, a piping-hot chowder of this sort can always give you a sense of real and unsurpassed satisfaction.",
        3,
        "Decreases Stamina depleted by gliding and sprinting for all party members by 15 - 25% for 900s."
    ),
    (
        "Golden Shrimp Balls",
        "A deep-fried shrimp dish. The aroma assaults your senses, while the crispy potatoes bring out the light sweetness of the shrimp meat. This, in tandem with its cute, small shape, makes it very enticing indeed.",
        3,
        "Revives the selected character. Restores 900 - 1,500 HP."
    ),
    (
        "Sticky Honey Roast",
        "A meat dish in a sweet honey sauce. The carrots take the gamey edge off the meat, and the sauce brings it all together sweetly. The perfect warm dish for a cold winter night.",
        3,
        "Decreases Stamina depleted by climbing and sprinting for all party members by 15-25% for 900s."
    ),
]

cursor.executemany("""
    INSERT INTO foods (name, description, rarity, effects)
    VALUES (?, ?, ?, ?)
""", foods)

# Food ingredients
food_ingredients = [
    # Sweet Madame (1)
    (1, 28, 2),  # Fowl
    (1, 16, 2),  # Sweet Flower

    # Mondstadt Hash Brown (2)
    (2, 32, 2),  # Potato
    (2, 13, 2),  # Pinecone
    (2, 14, 1),  # Jam

    # Satisfying Salad (3)
    (3, 12, 2),  # Apple
    (3, 32, 1),  # Potato
    (3, 22, 1),  # Bird Egg
    (3, 17, 2),  # Cabbage

    # Jade Parcels (4)
    (4, 11, 1),  # Ham
    (4, 17, 2),  # Cabbage
    (4, 10, 3),  # Lotus Head
    (4, 20, 2),  # Jueyun Chili

    # Crab Roe Tofu (5)
    (5, 8, 1),   # Crab Roe
    (5, 7, 1),   # Tofu

    # Mushroom Pizza (6)
    (6, 25, 3),  # Flour
    (6, 21, 4),  # Mushroom
    (6, 6, 1),   # Cheese
    (6, 17, 1),  # Cabbage

    # Radish Veggie Soup (7)
    (7, 5, 1),   # Radish
    (7, 4, 1),  # Mint

    # Qingce Stir Fry (8)
    (8, 20, 1),  # Jueyun Chili
    (8, 10, 2),  # Lotus Head
    (8, 17, 1),  # Cabbage
    (8, 21, 3),  # Mushroom

    # Rice Pudding (9)
    (9, 26, 2),  # Rice
    (9, 24, 2),  # Milk
    (9, 23, 2),  # Sugar
    (9, 22, 3),  # Bird Egg

    # Calla Lily Seafood Soup (10)
    (10, 3, 1),  # Calla Lily
    (10, 9, 4),  # Crab
    (10, 4, 2),  # Mint

    # Barbatos Ratatouille (11)
    (11, 1, 4),  # Carrot
    (11, 30, 4), # Onion
    (11, 32, 4), # Potato

    # Golden Shrimp Balls (12)
    (12, 2, 4),  # Shrimp Meat
    (12, 32, 3), # Potato

    # Sticky Honey Roast (13)
    (13, 29, 3), # Raw Meat
    (13, 1, 2),  # Carrot
    (13, 23, 2), # Sugar
]

cursor.executemany("""
    INSERT INTO food_ingredients (food_id, ingredient_id, amount)
    VALUES (?, ?, ?)
""", food_ingredients)

# ----- For debugging purposes -----
#food_name = 'sticky honey'
#cursor.execute("SELECT * FROM foods WHERE LOWER(name) LIKE LOWER(?)", (f"%{food_name}%",))
#print(cursor.fetchall())

conn.commit()
conn.close()