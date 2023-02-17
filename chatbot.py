def main():
    steps = ["Wash the rice", "Put the rice in the rice cooker", "Turn on the rice cooker"]
    idx = 0
    outputStep(steps, idx)
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

def outputStep(step_list, idx):
    if idx < 0 or idx >= len(step_list):
        print(f"Response: Out of steps at step: {idx}")
    print(f"Response: {step_list[idx]}")


if __name__ == "__main__":
    main()