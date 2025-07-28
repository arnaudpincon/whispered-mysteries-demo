class Clue:
    def __init__(self, name, description, room_name):
        self.name = name
        self.description = description
        self.room_name = room_name
        self.is_collected = False

    def collect(self):
        self.is_collected = True
        return f"You have collected: {self.name}"
