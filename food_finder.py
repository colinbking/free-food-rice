import string

class FoodFinder():
    def __init__(self):
        self.food_words = {"free", "goodie", "cake", "cupcake", "donut", "taco", "meat", "roast", "fried", "grab","food", "canes", "cane", "chickfila", "chick-fil-a", "chicken", "nugget", "sweet", "bread", "chocolate", "sandwich", "cookie", "avocado", "toast", "cheese", "ice", "cream"}
    def update_dict(self, event_dict):
        count = 0
        for event in event_dict:
            event["food"] = self.find_food(event["desc"])
            if event["food"] == "true":
                count += 1
        return count
    
    def find_food(self, text):
        for word in text.split(" "):
            word = word.lower().translate(str.maketrans('', '', string.punctuation))
            if word in self.food_words:
                return "true"
            return "false"
        

