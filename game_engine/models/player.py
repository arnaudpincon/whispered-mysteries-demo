class Player:
    def __init__(self, name):
        self.name = name
        self.current_location = None
        self.inventory = []

    def move(self, room):
        """Move to a specified room from the list of exits."""
        self.current_location = room
        return f"You enter {self.current_location}"
    
    #    if room.name in self.current_location.exits:
    #         self.current_location = room
    #         return f"You enter {self.current_location}.

    def collect_clue(self, clue_name):
        for clue in self.current_location.clues:
            if clue.name.lower() == clue_name.lower() and not clue.is_collected:
                clue.collect()
                self.inventory.append(clue)
                self.current_location.remove_clue(clue)
                print(f"You have added {clue.name} to your inventory.")
                return True
        print("You can not interact with this object")
        return False
