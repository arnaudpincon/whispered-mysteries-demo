class Secret:
    def __init__(self, condition, secret):
        self.condition = condition
        self.secret = secret
        self.shown = False

    def reveal(self, clue):
        if clue == self.condition:
            return f"You have unlocked a secret: {self.secret}"
        return f"{clue} can't be used here."
    
    def set_shown(self, shown: bool):
        """Set the shown status of the secret."""
        self.shown = shown
