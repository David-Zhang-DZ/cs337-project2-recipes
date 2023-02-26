import spacy
import re
from pyyoutube import Api
from googlesearch import search
from recipe_loader import load_ingredients, init_recipe_data

nlp = spacy.load("en_core_web_sm")

def main():
    api = Api(api_key="AIzaSyCFOl8vv1md_YmVgkmYvQ9O_MZCgmkCYlc")

    steps, _ = init_recipe_data(1)
    idx = 0
    outputStep(steps, idx)
    #quantities = load_ingredients()
    #print(quantities.keys())
    while True:
        x = input("Input: ")
        if x == "q" or x == "quit":
            break

        match = re.search("how do i (.*)", x.lower()) #Youtube Search
        if match:
            print(match[1])
            videos = api.search_by_keywords(q="how to " + match[1], search_type=["video"], limit=5)
            print(f"https://www.youtube.com/watch?v={videos.items[0].id.videoId}")
        match = re.search('what is (.*)', x.lower()) #Google Search
        if match:
            print(match[1])
            results = search(f"what is {match[1]}", num_results=3)
            for result in results:
                print(result)
            

        #match = re.search("how much (.*) do i need", x.lower())
        
        #match = re.search('what temperature', x.lower())
        #match = re.search('how long do i do (.*)', x.lower())
       
        
        # doc = nlp(x)
        # object = "NO OBJECT!!!!"
        # for token in doc:
        #     if token.dep_ == "dobj":
        #         modifiers = f"{' '.join([child.text for child in token.children if len([subchild.text for subchild in child.children]) == 0])}"
        #         dobj = token.text
        #         if len(modifiers) > 0:
        #             object = f"{modifiers} {dobj}"
        #         else:
        #             object = dobj

        if "next" in x.lower():
            idx += 1
            outputStep(steps, idx)
        elif "back" in x.lower():
            idx -= 1
            outputStep(steps, idx)
        elif "repeat" in x.lower():
            outputStep(steps, idx)
        
        
        # elif "how much" in x.lower():
        #     print(f"Object: {object}")
        #     if object in quantities:
        #         print(quantities[object])



def outputStep(step_list, idx):
    if idx < 0 or idx >= len(step_list):
        print(f"Response: Out of steps at step: {idx}")
    print(f"Response: {step_list[idx]}")


if __name__ == "__main__":
    main()
