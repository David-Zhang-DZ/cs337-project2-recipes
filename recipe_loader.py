import spacy
import re
import sys
from sample_recipes import recipe1, recipe2, recipe3, recipe4, recipe5

NLP = spacy.load("en_core_web_sm")
DEFAULT_MEASURE_WORDS = set(["teaspoon", "tablespoon", "cup", "pound"])

ingredients, steps, measure_words = [], [], set([]) # Will be filled in w/ command-line args

def load_ingredients():
    quantities = {}

    curr_ingredient, curr_quantity = None, None

    for ingredient in ingredients:
        doc = NLP(ingredient)

        for token in doc:
            if token.dep_ == "ROOT":
                modifiers = [child.text for child in token.children if child.text not in measure_words and child.dep_ != "nummod"]
                curr_ingredient = f"{' '.join(modifiers) if len(modifiers) > 0 else ''} {token.text}".strip()

                quantities[curr_ingredient] = curr_quantity
                curr_ingredient, curr_quantity = None, None
            elif token.dep_ == "nummod":
                curr_measure_word = ""
                measure_word_matches = [e for e in ingredient.split(" ") if e in measure_words]

                if measure_word_matches:
                  curr_measure_word = measure_word_matches[0]

                curr_quantity = f"{token.text} {curr_measure_word}".strip()

    return quantities

def load_recipe_actions():
    actions = []
    prev_ingredients = []

    for step in steps:
        doc = NLP(step)

        action = None
        ingredients = []

        for token in doc:
            if token.dep_ == "ROOT":
                action = token.text
            elif token.dep_ == "dobj":
                ingredients.append(token.text)

        if ingredients:
          actions.append((action, ', '.join(ingredients)))
          prev_ingredients = ingredients
        else:
          actions.append((action, ', '.join(prev_ingredients)))

    return actions

def determine_measure_words():
  global measure_words

  for k in DEFAULT_MEASURE_WORDS:
    measure_words.add(k)

  for ingredient in ingredients:
        doc = NLP(ingredient)

        for token in doc:
            if token.dep_ == "nummod" and token.head.dep_ != "ROOT":
                measure_word = token.head.text

                if measure_word not in measure_words:
                  measure_words.add(measure_word)

def parse_ingredients(raw_ingredients):
  ingredients = []

  for ingredient in raw_ingredients:
    ingredient = re.sub("\(.*?\)", "", ingredient)
    ingredient = re.sub(" +", " ", ingredient)

    ingredients.append(ingredient)

  return ingredients

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

  ingredients = parse_ingredients(ingredients)
  steps = parse_steps(steps)

  return steps, ingredients

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please provide a recipe number")
      exit(1)

    recipe_number = int(sys.argv[1])

    if recipe_number not in [1, 2, 3, 4, 5]:
      print("Invalid recipe number")
      exit(1)

    init_recipe_data(recipe_number)
    determine_measure_words()

    ingredients = load_ingredients()
    actions = load_recipe_actions()

    print("INGREDIENTS:", ingredients)
    print()
    print("RAW STEPS:", steps)
    print()
    print("ACTIONS:", actions)
