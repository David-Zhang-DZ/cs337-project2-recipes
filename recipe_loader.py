import spacy

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

nlp = spacy.load("en_core_web_sm")
for ingredient in ingredients:
    doc = nlp(ingredient)

    for token in doc:
        if token.dep_ == "ROOT":
            modifiers = [child.text for child in token.children if child.text not in measure_words]
            print(f"Ingredient: {' '.join(modifiers) if len(modifiers) > 0 else ''} {token.text}")
        elif token.dep_ == "nummod":
            print(f"Quantity: {token.text} {token.head.text}")
        #print(token.text, token.dep_, token.head.text, token.head.pos_,
        #        [child for child in token.children])