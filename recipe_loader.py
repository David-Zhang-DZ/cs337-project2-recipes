import spacy
import re
import sys
from sample_recipes import recipe1, recipe2, recipe3, recipe4, recipe5

nlp = spacy.load("en_core_web_sm")
# measure_words = ["ounces", "teaspoon",  "cup", "tablespoon", "pound"]
ingredients, steps, measure_words = [], [], [] # Will be filled in w/ command-line args

def load_ingredients():
    ingredients = ["1 pound ground chicken",
                    "1 large egg",
                    "1/2 cup panko breadcrumbs",
                    "1 teaspoon onion powder",
                    "1/2 teaspoon garlic powder",
                    "1/2 teaspoon kosher salt",
                    "1/4 teaspoon ground black pepper",
                    "4 large carrots, sliced into 1/4-inch thick rounds"    
                    ]

    measure_words = ["teaspoon",  "cup", "tablespoon", "pound"]
    quantities = {}
    for ingredient in ingredients:
        doc = nlp(ingredient)
        curr_quantity = None
        for token in doc:
            if token.dep_ == "ROOT":
                quantities[token.text] = curr_quantity
                modifiers = [child.text for child in token.children if child.text not in measure_words]
                #print(f"Ingredient: {' '.join(modifiers) if len(modifiers) > 0 else ''} {token.text}")
            elif token.dep_ == "nummod":
                #print(f"Quantity: {token.text} {token.head.text}")
                curr_quantity = token.text + " " + token.head.text
                 
    return quantities

def load_recipes():
    for step in steps:
        doc = nlp(step)

        action = None
        ingredients = []

        for token in doc:
            if token.dep_ == "ROOT":
                action = token.text
            elif token.dep_ == "dobj":
                ingredients.append(token.text)

        print(f"Action: {action}, ingredients:{', '.join(ingredients)}")

# def parse_ingredients(raw_ingredients):


def parse_steps(raw_steps):
    steps = []

    for s in raw_steps:
      s = s.replace("\n", "")
      res = re.split("[.:;]", s)

      for subres in res:
        if subres:
          steps.append(subres.strip())

    return steps

def init_recipe_data(recipe_number):
  global ingredients
  global steps

  if recipe_number == 1:
    ingredients, steps = recipe1.INGREDIENTS, recipe1.STEPS

  if recipe_number == 2:
    ingredients, steps = recipe2.INGREDIENTS, recipe2.STEPS

  if recipe_number == 3:
    ingredients, steps = recipe3.INGREDIENTS, recipe3.STEPS

  if recipe_number == 4:
    ingredients, steps = recipe4.INGREDIENTS, recipe4.STEPS

  if recipe_number == 5:
    ingredients, steps = recipe5.INGREDIENTS, recipe5.STEPS

  # ingredients = parse_ingredients(ingredients)
  steps = parse_steps(steps)

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please provide a recipe number")
      exit(1)

    recipe_number = int(sys.argv[1])

    if recipe_number not in [1, 2, 3, 4, 5]:
      print("Invalid recipe number")
      exit(1)

    init_recipe_data(recipe_number)

    # load_ingredients()
    # print()
    # load_recipes()
