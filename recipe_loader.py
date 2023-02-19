import spacy
from sample_recipes import recipe1, recipe2, recipe3, recipe4, recipe5

nlp = spacy.load("en_core_web_sm")

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

    for ingredient in ingredients:
        doc = nlp(ingredient)

        for token in doc:
            if token.dep_ == "ROOT":
                modifiers = [child.text for child in token.children if child.text not in measure_words]
                print(f"Ingredient: {' '.join(modifiers) if len(modifiers) > 0 else ''} {token.text}")
            elif token.dep_ == "nummod":
                print(f"Quantity: {token.text} {token.head.text}")

def load_recipes():
    text = "Heat a large skillet over medium heat. Cook and stir lean ground beef in the hot skillet until some of the fat starts to render, 3 to 4 minutes. Add onion and bell pepper; continue to cook until vegetables have softened and beef is cooked through, 3 to 5 more minutes."
    steps = text.split(".")
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

if __name__ == "__main__":
    load_ingredients()
    print()
    load_recipes()
