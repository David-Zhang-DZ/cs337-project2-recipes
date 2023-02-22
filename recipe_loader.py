import spacy
import re
import sys
import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me

NLP = spacy.load("en_core_web_sm")
DEFAULT_MEASURE_WORDS = set(["teaspoon", "tablespoon", "cup", "pound", "ounce", "teaspoons", "tablespoons", "cups", "pounds", "ounces"])

ingredients, steps = [], [] # Will be filled in w/ command-line args

def load_ingredients():
    quantities = {}

    token_filter = lambda s : s.text not in DEFAULT_MEASURE_WORDS and s.dep_ != "nummod" and s.pos_ in ["PROPN", "NOUN", "VERB", "ADJ"]
    comma_surrounded_by_keywords = lambda doc, idx: doc[idx - 1].pos_ not in ["PROPN", "NOUN", "ADJ"] or doc[idx + 1].pos_ not in ["PROPN", "NOUN", "ADJ"]
    start_noun_chunk = lambda text, noun_chunks: any([chunk.startswith(text) for chunk in noun_chunks])

    for ingredient in ingredients:
        doc = NLP(ingredient)
        curr_ingredient, curr_quantity = [], ""
        noun_chunks = [str(chunk) for chunk in list(doc.noun_chunks)]

        for idx, token in enumerate(doc):
            if token_filter(token):
              curr_ingredient.append(token.text)
            elif token.text == "," and (comma_surrounded_by_keywords(doc, idx) or not start_noun_chunk(doc[idx + 1].text, noun_chunks)):
              break
            elif token.dep_ == "nummod":
                curr_measure_word = ""
                measure_word_matches = [e for e in ingredient.split(" ") if e in DEFAULT_MEASURE_WORDS]

                if measure_word_matches:
                  curr_measure_word = measure_word_matches[0]

                curr_quantity = f"{token.text} {curr_measure_word}".strip()

        curr_ingredient = " ".join(curr_ingredient)
        quantities[curr_ingredient] = curr_quantity if curr_quantity else None

    return quantities

def load_recipe_actions():
    actions = []
    prev_ingredients = []

    for step in steps:
        doc = NLP(step)

        action = None
        ingredients = []
        temperatures = []

        for i, token in enumerate(doc):
            if token.dep_ == "ROOT":
                action = token.text
            elif token.dep_ == "dobj":
                ingredients.append(token.text)

            if token.text.isnumeric() and doc[i + 1].text == "°":
              temperatures.append(doc[i].text + doc[i + 1].text)



              # for child in token.children:
              #   if child.text == "°":
              #     for sub_child in child.children:

              #       if sub_child.dep_ == "nummod":
              #         temperatures.append(sub_child.text + child.text)



        if len(temperatures) > 0:
          print(temperatures)

        if ingredients:
          actions.append((action, ', '.join(ingredients)))
          prev_ingredients = ingredients
        else:
          actions.append((action, ', '.join(prev_ingredients)))

    return actions

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

def init_recipe_data(recipe_query=None, recipe_url=None):
  global ingredients
  global steps

  if not recipe_url:
    URL = f"https://www.allrecipes.com/search?q={recipe_query}"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, "html.parser")
    all_results = soup.find("div", {"id": "search-results__content_1-0"})
    first_page_results = all_results.find("div", {"id": "card-list_1-0"})
    recipe_url = first_page_results.find("a")["href"]

    if not recipe_url:
      print("Error: Could not find recipes")
      exit(1)

  scraper = scrape_me(recipe_url)
  ingredients, steps = scraper.ingredients(), scraper.instructions_list()

  ingredients = parse_ingredients(ingredients)
  steps = parse_steps(steps)

  return steps, ingredients

# def determine_measure_words():
#   global measure_words

#   for k in DEFAULT_MEASURE_WORDS:
#     measure_words.add(k)

#   for ingredient in ingredients:
#         doc = NLP(ingredient)

#         for token in doc:
#             if token.dep_ == "nummod" and token.head.dep_ != "ROOT":
#                 measure_word = token.head.text

#                 if measure_word not in measure_words:
#                   measure_words.add(measure_word)

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please provide a recipe query")
      exit(1)

    if str(sys.argv[1]).startswith("https://"):
      init_recipe_data(recipe_url=str(sys.argv[1]))
    else:
      recipe_query = "+".join(sys.argv[1:])
      init_recipe_data(recipe_query=recipe_query)

    ingredients = load_ingredients()
    actions = load_recipe_actions()

    print("INGREDIENTS:", ingredients)
    print()
    print("RAW STEPS:", steps)
    print()
    print("ACTIONS:", actions)
