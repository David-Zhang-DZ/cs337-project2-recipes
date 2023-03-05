class RecipeStep:
  def __init__(self, text, action, temperature, time):
    self.text = text
    self.action = action
    self.temperature = temperature
    self.time = time

  def print(self):
    print("TEXT:", self.text)
    print("ACTION:", self.action)

    if self.temperature:
      print("TEMPERATURE:", self.temperature)

    if self.time:
      print("TIME:", self.time)

    print()
