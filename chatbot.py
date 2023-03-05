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
        x = input("You: ").lower()
        if x == "q" or x == "quit":
            break

        valid_input = False

        regex_searches = ["how do i (.*)", "what is (.*)", "how much (.*)", "go to step (.*)", "what can i substitute for (.*)"]
        exact_matches = ["what temperature", "how long", "next", "back", "repeat", "show me all ingredients", "how"]

        for i, regex in enumerate(regex_searches):
          match = re.search(regex, x)

          if match:
            if i == 0:
              videos = API.search_by_keywords(q="how to " + match[1], search_type=["video"], limit=5)

              print(f"ChefBot: Here is a video showing you how to '{match[1]}'")
              print(f"https://www.youtube.com/watch?v={videos.items[0].id.videoId}")
            elif i == 1:
              results = search(f"what is {match[1]}", num_results=3)

              print(f"ChefBot: Here are your results for search '{match[1]}'")
              for result in results:
                  print("ChefBot:", result)
            elif i == 2:
              quantity = ingredient_lookup(recipe_data.ingredient_quantities, match[1])
              if quantity is None:
                print(f"ChefBot: Unsure how much quantity needed for ingredient '{match[1]}'; please try another query")
              else:
                print(quantity)
            elif i == 3:
              if not match[1].isnumeric():
                print("Error: Step number must be numeric, i.e. 1, 2, 3")
                valid_input = True
                break

              temp_idx = int(match[1]) - 1

              if temp_idx <= 0 or temp_idx >= len(recipe_data.steps):
                print("Error: Invalid Step Number")
                valid_input = True
                break

              idx = temp_idx
              output_step(recipe_data.steps, idx)
            elif i == 4:
              results = search(f"what can I substitute for {match[1]}", num_results=3)

              print(f"ChefBot: Here are your results for substitutes for '{match[1]}'")
              for result in results:
                  print(result)

            valid_input = True
            break

        if not valid_input:
          for i, match in enumerate(exact_matches):
            if x == match:
              if i == 0:
                current_temperature = recipe_data.parsed_steps[idx].temperature

                if current_temperature is None:
                  print("ChefBot: No temperature associated with this recipe step")
                else:
                  print("ChefBot:", current_temperature)
              elif i == 1:
                current_time = recipe_data.parsed_steps[idx].time

                if current_time is None:
                  print("ChefBot: No time amount associated with this recipe step")
                else:
                  print("ChefBot:", current_time)
              elif i == 2:
                idx += 1
                output_step(recipe_data.steps, idx)
              elif i == 3:
                if idx == 0:
                  print("ChefBot: Cannot go back from the first step")
                  valid_input = True
                  break

                idx -= 1
                output_step(recipe_data.steps, idx)
              elif i == 4:
                output_step(recipe_data.steps, idx)
              elif i == 5:
                print(recipe_data.ingredient_quantities)
              elif i == 6:
                action = recipe_data.parsed_steps[idx].action
                search_query = action[0] + " " + action[1]

                videos = API.search_by_keywords(q="how to " + search_query, search_type=["video"], limit=5)

                print(f"ChefBot: Here is a video showing you how to '{search_query}'")
                print(f"https://www.youtube.com/watch?v={videos.items[0].id.videoId}")

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
      print("ChefBot: Done with recipe, chatbot closing now")
      exit(0)

    extra_output = f"(First Step)" if idx == 0 else "(Last Step)" if idx == len(step_list) - 1 else ""
    print(f"ChefBot [Step {idx + 1}]: {extra_output} {step_list[idx]}")

def print_error_message():
  print()
  print("Sorry, we didn't recognize your input. Please ask a question in one of the following forms (case insensitive):\n")
  print("1. How do I <action>\n2. What is <ingredient/tool>\n3. How much <ingredient>\n4. Go to step <number>\n5. What can I substitute for <ingredient>\n6. What temperature")
  print("7. How long\n8. Next\n9. Back\n10. Repeat\n11. How (i.e. how to do action for current step)")
  print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please provide a recipe query or number")
      exit(1)

    if len(sys.argv) == 2:
      main(sys.argv[1])
    else:
      main("+".join(sys.argv[1:]))
