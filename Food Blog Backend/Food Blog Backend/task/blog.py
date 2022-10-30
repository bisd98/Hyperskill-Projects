import sys
import sqlite3

args = sys.argv
conn = sqlite3.connect(args[1])
cur = conn.cursor()

table_names = ['meals', 'ingredients', 'measures']

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


with conn:
    for name in table_names:
        cur.execute(f""" CREATE TABLE IF NOT EXISTS {name}(
                    {name[:-1]}_id INTEGER PRIMARY KEY,
                    {name[:-1]}_name TEXT {'NOT NULL' if name != 'measures' else ''} UNIQUE
                    );""")
        for value in data[name]:
            cur.execute(f"INSERT OR IGNORE INTO {name} ({name[:-1]}_name) VALUES ('{value}');")
        cur.execute('PRAGMA foreign_keys = ON;')
        conn.commit()

with conn:
    cur.execute(""" CREATE TABLE IF NOT EXISTS recipes (
                    recipe_id INTEGER PRIMARY KEY,
                    recipe_name TEXT NOT NULL,
                    recipe_description TEXT
                    );""")
    cur.execute(""" CREATE TABLE IF NOT EXISTS serve (
                    serve_id INTEGER PRIMARY KEY,
                    meal_id INTEGER NOT NULL,
                    recipe_id INTEGER NOT NULL,
                    FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
                    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
                    );""")
    cur.execute(""" CREATE TABLE IF NOT EXISTS quantity (
                    quantity_id INTEGER PRIMARY KEY,
                    measure_id INTEGER NOT NULL,
                    ingredient_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    recipe_id INTEGER NOT NULL,
                    FOREIGN KEY (measure_id) REFERENCES measures(measure_id),
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
                    );""")
    conn.commit()


def recipe_search(ing_val, meal_val):
    with conn:
        cur.execute(f"""SELECT recipe_id FROM quantity
                        WHERE""")


def measure_search(in_value):
    with conn:
        try:
            measure_values = cur.execute("SELECT measure_name FROM measures")
            m_values = [v[0] for v in measure_values.fetchall()]
            if " ".join(m_values).count(in_value) == 1:
                return True
        except TypeError:
            return False


def ingredient_search(in_value):
    with conn:
        try:
            ingredient_values = cur.execute("SELECT ingredient_name FROM ingredients")
            i_values = [v[0] for v in ingredient_values.fetchall()]
            if " ".join(i_values).count(in_value) == 1:
                return True
        except TypeError:
            return False


def get_id(in_value, table):
    with conn:
        table_value = cur.execute(f"SELECT {table[:-1]}_id FROM {table} "
                                  f"WHERE {table[:-1]}_name LIKE '{in_value}%';")
        value_id = table_value.fetchone()[0]
        return value_id


if len(args) > 2:
    ing_id, meal_id = [], []
    ing_values = args[2][14:].split(',')
    meal_values = args[3][8:].split(',')
    for val in ing_values:
        try:
            ing_id.append(get_id(val, 'ingredients'))
        except TypeError:
            print('ingredients error')
    for val in meal_values:
        try:
            meal_id.append(get_id(val, 'meals'))
        except TypeError:
            print('meals error')
    recipe_lists_id = []
    with conn:
        for val in ing_id:
            rec_values = cur.execute(f"SELECT recipe_id FROM quantity WHERE ingredient_id = {val}")
            recipe_lists_id.append(set(rec_values.fetchall()))
    rec_id = [x[0] for x in recipe_lists_id[0].intersection(*recipe_lists_id)]
    with conn:
        recipe_list = []
        for val in rec_id:
            rec_name = cur.execute(f"SELECT recipe_name FROM recipes WHERE recipe_id = {val}")
            recipe_list.append(rec_name.fetchall()[0][0])
        print(f"Recipes selected for you: {', '.join(recipe_list)}")
    exit()  #TRZEBA UWZGLĘDNIĆ MEALS

print('Pass the empty recipe name to exit.')
while True:
    in_recipe = input('Recipe name: ')
    if not in_recipe:
        break
    in_desc = input('Recipe description: ')
    meal_times = cur.execute('SELECT * FROM meals')
    meal_row = cur.fetchall()
    print(f'{meal_row[0][0]}) {meal_row[0][1]}  {meal_row[1][0]}) {meal_row[1][1]}  '
          f'{meal_row[2][0]}) {meal_row[2][1]}  {meal_row[3][0]}) {meal_row[3][1]}')
    meal_time = [int(x) for x in input('When the dish can be served: ').split()]
    with conn:
        cur.execute(f"INSERT INTO recipes (recipe_name, recipe_description)"
                    f"VALUES ('{in_recipe}', '{in_desc}');")
        example = cur.execute(f"SELECT recipe_id FROM recipes WHERE recipe_name = '{in_recipe}'")
        current_recipe_id = example.fetchone()[0]
        for meal in meal_time:
            cur.execute(f"INSERT INTO serve (meal_id, recipe_id)"
                        f"VALUES ({meal}, {current_recipe_id});")
        conn.commit()
    while True:
        ingredients = [x for x in input('Input quantity of ingredient <press enter to stop>: ').split()]
        if not ingredients:
            break
        try:
            quantity = int(ingredients[0])
        except ValueError:
            print('The quantity is not conclusive!')
            continue
        if len(ingredients) < 3:
            if ingredient_search(ingredients[1]):
                ingredient = get_id(ingredients[1], 'ingredients')
                measure = get_id("", 'measures')
                pass
            else:
                print('The ingredient is not conclusive!')
                continue
        else:
            if measure_search(ingredients[1]):
                measure = get_id(ingredients[1], 'measures')
                if ingredient_search(ingredients[2]):
                    ingredient = get_id(ingredients[2], 'ingredients')
                    pass
                else:
                    print('The ingredient is not conclusive!')
                    continue
            else:
                print('The ingredient is not conclusive!')
                continue
        with conn:
            current_recipe_id = get_id(in_recipe, 'recipes')
            cur.execute(f"INSERT INTO quantity (measure_id, ingredient_id, quantity, recipe_id)"
                        f"VALUES ({measure}, {ingredient}, '{quantity}', {current_recipe_id});")
            conn.commit()

conn.close()
