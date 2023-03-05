# Recipes Project

Currently, there are 3 ways to run the chatbot, you need to provide a command-line argument:

  1. A sample recipe number from 1 to 5, e.g. `python3 chatbot.py 2`
  2. **A recipe URL, e.g. `python3 chatbot.py https://www.allrecipes.com/recipe/241890/grilled-chicken-marinade/`**
  3. A recipe query, e.g. `python3 chatbot.py spaghetti with meatballs`

But **the 2nd option will likely be most relevant for our purpose**. Moreover, at each step, you can currently ask the chatbot the following questions:

  1. How do I <action> [YouTube Search]
  2. What is <ingredient/tool> [Google Search]
  3. How much <ingredient>
  4. Go to step <number>
  5. What can I substitute for <ingredient> [Google Search]
  6. What temperature
  7. How long
  8. Next
  9. Back
  10. Repeat
  11. How (i.e. how to do action for current step) [YouTube Search]
