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

    # print(recipe_data.ingredient_quantities)
    # for s in recipe_data.parsed_steps:
    #   s.print()

    idx = 0
    outputStep(recipe_data.steps, idx)

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
              # Ingredient quantity lookup
              pass

            valid_input = True
            break

        if not valid_input:
          for i, match in enumerate(exact_matches):
            if x == match:
              if i == 0:
                # Temp lookup
                pass
              elif i == 1:
                # Time lookup
                pass
              elif i == 2:
                idx += 1
                outputStep(recipe_data.steps, idx)
              elif i == 3:
                idx -= 1
                outputStep(recipe_data.steps, idx)
              else:
                outputStep(recipe_data.steps, idx)

              valid_input = True
              break

        if not valid_input:
          # Print some error message
          pass

def outputStep(step_list, idx):
    if idx < 0 or idx >= len(step_list):
        print(f"Response: Out of steps at step: {idx}")

    extra_output = f"(First Step)" if idx == 0 else "(Last Step)" if idx == len(step_list) - 1 else ""
    print(f"Response: {extra_output} {step_list[idx]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please provide a recipe query or number")
      exit(1)

    if len(sys.argv) == 2:
      main(sys.argv[1])
    else:
      main("+".join(sys.argv[1:]))
