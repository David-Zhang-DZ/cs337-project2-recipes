import sys
import spacy
import re
from pyyoutube import Api
from googlesearch import search
from recipe_loader import Recipe

NLP = spacy.load("en_core_web_sm")
API = Api(api_key="AIzaSyCFOl8vv1md_YmVgkmYvQ9O_MZCgmkCYlc")

def main(data_source):
    print("Loading, parsing recipe data")
    recipe_data = Recipe(data_source)
    print("Done loading recipe data!\n")

    idx = 0
    output_step(recipe_data.steps, idx)

    while True:
        x = input("Input: ").lower()
        if x == "q" or x == "quit":
            break

        valid_input = False

        regex_searches = ["how do i (.*)", "what is (.*)", "how much (.*) do i need"]
        exact_matches = ["what temperature", "how long", "next", "back", "repeat"]

        for i, regex in enumerate(regex_searches):
          match = re.search(regex, x)

          if match:
            if i == 0:
              videos = API.search_by_keywords(q="how to " + match[1], search_type=["video"], limit=5)
              print(f"https://www.youtube.com/watch?v={videos.items[0].id.videoId}")
            elif i == 1:
              results = search(f"what is {match[1]}", num_results=3)
              for result in results:
                  print(result)
            else:
              quantity = ingredient_lookup(recipe_data.ingredient_quantities, match[1])

              if quantity is None:
                print(f"Response: Unsure how much quantity needed for ingredient '{match[1]}'; please try another query")
              else:
                print(quantity)

            valid_input = True
            break

        if not valid_input:
          for i, match in enumerate(exact_matches):
            if x == match:
              if i == 0:
                current_temperature = recipe_data.parsed_steps[idx].temperature

                if current_temperature is None:
                  print("Response: No temperature associated with this recipe step")
                else:
                  print("Response:", current_temperature)
              elif i == 1:
                current_time = recipe_data.parsed_steps[idx].time

                if current_time is None:
                  print("Response: No time amount associated with this recipe step")
                else:
                  print("Response:", current_time)
              elif i == 2:
                idx += 1
                output_step(recipe_data.steps, idx)
              elif i == 3:
                if idx == 0:
                  print("Response: Cannot go back from the first step")
                  valid_input = True
                  break

                idx -= 1
                output_step(recipe_data.steps, idx)
              else:
                output_step(recipe_data.steps, idx)

              valid_input = True
              break

        if not valid_input:
          print_error_message()

def ingredient_lookup(quantities, query):
  for ingredient, quantity in quantities.items():
    if query in ingredient:
      return quantity

  return None

def output_step(step_list, idx):
    if idx == len(step_list):
      print("Response: Done with recipe, chatbot closing now")
      exit(0)

    extra_output = f"(First Step)" if idx == 0 else "(Last Step)" if idx == len(step_list) - 1 else ""
    print(f"Response: {extra_output} {step_list[idx]}")

def print_error_message():
  print()
  print("Sorry, we didn't recognize your input. Please ask a question in one of the following forms (case insensitive):\n")
  print("1. How do I (.*)\n2. What is (.*)\n3. How much (.*) do I need\n4. What temperature")
  print("5. How long\n6. Next\n7. Back\n8. Repeat")
  print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please provide a recipe query or number")
      exit(1)

    if len(sys.argv) == 2:
      main(sys.argv[1])
    else:
      main("+".join(sys.argv[1:]))
