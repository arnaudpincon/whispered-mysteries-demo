from typing import Any, Dict, List


class Room:
    def __init__(self, name, description, exits, image_url=""):
        self.name = name
        self.description = description
        self.exits = exits
        self.characters = []
        self.clues = []
        self.image_url = image_url

    def add_clue(self, clue):
        self.clues.append(clue)

    def remove_clue(self, clue):
        if clue in self.clues:
            self.clues.remove(clue)

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        if character in self.characters:
            self.characters.remove(character)

    def add_exit(self, room):
        self.exits.append((room))
