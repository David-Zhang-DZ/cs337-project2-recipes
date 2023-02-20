import spacy
import re
from recipe_loader import load_ingredients, init_recipe_data

nlp = spacy.load("en_core_web_sm")

def main():
    steps, _ = init_recipe_data(1)
    idx = 0
    #outputStep(steps, idx)
    quantities = load_ingredients()
    print(quantities.keys())
    while True:
        x = input("Input: ")
        if x == "q" or x == "quit":
            break

        doc = nlp(x)
        object = "NO OBJECT!!!!"
        for token in doc:
            if token.dep_ == "dobj":
                modifiers = f"{' '.join([child.text for child in token.children if len([subchild.text for subchild in child.children]) == 0])}"
                dobj = token.text
                if len(modifiers) > 0:
                    object = f"{modifiers} {dobj}"
                else:
                    object = dobj

        if "next" in x.lower():
            idx += 1
            outputStep(steps, idx)
        elif "back" in x.lower():
            idx -= 1
            outputStep(steps, idx)
        elif "repeat" in x.lower():
            outputStep(steps, idx)
        elif "how much" in x.lower():
            print(f"Object: {object}")
            if object in quantities:
                print(quantities[object])



def outputStep(step_list, idx):
    if idx < 0 or idx >= len(step_list):
        print(f"Response: Out of steps at step: {idx}")
    print(f"Response: {step_list[idx]}")


if __name__ == "__main__":
    main()
