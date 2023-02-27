import spacy
import re
import sys
import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me
from sample_recipes import recipe1, recipe2, recipe3, recipe4, recipe5
from cooking_lexicon import DEFAULT_MEASURE_WORDS, DEFAULT_TIME_WORDS, DEFAULT_COOKING_ACTIONS
from recipe_step import RecipeStep

NLP = spacy.load("en_core_web_sm")

class Recipe:
  def __init__(self, data_source):
    self.ingredients = []
    self.steps = []

    self.ingredient_quantities = {}
    self.parsed_steps = []

    self.init_recipe_data(data_source)
    self.load_ingredients()
    self.load_recipe_steps()

  def init_recipe_data(self, data_source):
    if data_source.isnumeric():
      recipe_number = int(data_source)

      if recipe_number == 1:
        self.ingredients, self.steps = recipe1.INGREDIENTS, recipe1.STEPS

      if recipe_number == 2:
        self.ingredients, self.steps = recipe2.INGREDIENTS, recipe2.STEPS

      if recipe_number == 3:
        self.ingredients, self.steps = recipe3.INGREDIENTS, recipe3.STEPS

      if recipe_number == 4:
        self.ingredients, self.steps = recipe4.INGREDIENTS, recipe4.STEPS

      if recipe_number == 5:
        self.ingredients, self.steps = recipe5.INGREDIENTS, recipe5.STEPS
    else:
      recipe_url = data_source.copy()

      if not recipe_url.startswith("https://"):
        recipe_query = "+".join(data_source)
        recipe_url = f"https://www.allrecipes.com/search?q={recipe_query}"

      r = requests.get(recipe_url)

      soup = BeautifulSoup(r.content, "html.parser")
      all_results = soup.find("div", {"id": "search-results__content_1-0"})
      first_page_results = all_results.find("div", {"id": "card-list_1-0"})
      recipe_url = first_page_results.find("a")["href"]

      if not recipe_url:
        print("Error: Could not find recipes")
        exit(1)

      scraper = scrape_me(recipe_url)
      self.ingredients, self.steps = scraper.ingredients(), scraper.instructions_list()

    self.ingredients = self.parse_ingredients(self.ingredients)
    self.steps = self.parse_steps(steps)

  def load_ingredients(self):
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

    self.ingredient_quantities = quantities.copy()

  def load_recipe_steps(self):
    res = []
    prev_ingredient = None

    for step in steps:
        doc = NLP(step.lower())

        action = None
        ingredient = None
        temperature = None
        time = None

        has_verbs = any([token.pos_ == "VERB" for token in doc])

        for i, token in enumerate(doc):
            if not has_verbs and i == 0:
              action = token.text

            if not action and token.dep_ == "ROOT":
                action = token.text

            if token.text in DEFAULT_COOKING_ACTIONS and token.pos_ != "NOUN":
                action = token.text

            valid_ingredient = (action != token.text and not ingredient)
            valid_dep_and_pos = (has_verbs and token.dep_ in ["dobj", "conj", "dep", "compound"] and token.pos_ in ["NOUN", "PROPN"]) or (not has_verbs and token.dep_ == "ROOT")

            if valid_ingredient and valid_dep_and_pos:
                ingredient = token.text

            valid_temp_parse = (token.text.isnumeric() and doc[i + 1].text == "°" and (doc[i + 2].text == "f" or doc[i + 2].text == "c"))
            valid_time_parse = (token.text.isnumeric() and doc[i + 1].text in DEFAULT_TIME_WORDS)

            if not temperature and valid_temp_parse:
              temperature = doc[i].text + doc[i + 1].text + doc[i + 2].text.upper()

            if not time and valid_time_parse:
               time = doc[i].text + " " + doc[i + 1].text

        current_action_parse = None

        if ingredient:
          current_action_parse = (action, ingredient)
          prev_ingredient = ingredient
        else:
          current_action_parse = (action, prev_ingredient)

        step_object = RecipeStep(step, current_action_parse, temperature, time)
        res.append(step_object)

    self.parsed_steps = res.copy()

  def parse_ingredients(self, raw_ingredients):
    ingredients = []

    for ingredient in raw_ingredients:
      ingredient = re.sub("\(.*?\)", "", ingredient)
      ingredient = re.sub(" +", " ", ingredient)

      ingredients.append(ingredient)

    return ingredients

  def parse_steps(self, raw_steps):
    steps = []

    for s in raw_steps:
      s = s.replace("\n", "")
      res = re.split("[.:;]", s)

      for subres in res:
        if subres:
          steps.append(subres.strip())

    return steps
