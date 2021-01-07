import string

class FoodFinder():
    def __init__(self):
        self.food_words = {"free", "food", "canes", "cane", "chickfila", "chick-fil-a", "chicken", "nugget", "sweet", "bread", "chocolate", "sandwich", "cookie", "avocado", "toast", "cheese", "ice", "cream"}
    def update_dict(self, event_dict):
        for event in event_dict:
            event["food"] = self.find_food(event["desc"])
    
    def find_food(self, text):
        for word in text.split(" "):
            word = word.lower().translate(str.maketrans('', '', string.punctuation))
            if word in self.food_words:
                return True
            return False
        

