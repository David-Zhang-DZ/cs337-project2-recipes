import re
from recipe_loader import load_ingredients

def main():
    steps = ["Wash the rice", "Put the rice in the rice cooker", "Turn on the rice cooker"]
    idx = 0
    outputStep(steps, idx)
    quantities = load_ingredients()
    print(quantities.keys())
    while True:
        x = input("Input: ")
        if x == "q" or x == "quit":
            break
        
        if "next" in x.lower():
            idx += 1
            outputStep(steps, idx)
        elif "back" in x.lower():
            idx -= 1
            outputStep(steps, idx)
        elif "repeat" in x.lower():
            outputStep(steps, idx)
        elif "how much" in x.lower():
            match = x.split()
            match = match.pop()
            if match in quantities:
                print(quantities[match])
            
            

def outputStep(step_list, idx):
    if idx < 0 or idx >= len(step_list):
        print(f"Response: Out of steps at step: {idx}")
    print(f"Response: {step_list[idx]}")


if __name__ == "__main__":
    main()