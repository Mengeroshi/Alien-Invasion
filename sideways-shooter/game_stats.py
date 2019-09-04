class GameStats:
    def __init__ (self, ai_game):

        self.settings = ai_game.settings
        
        self.game_active = True

        self.reset_stats()

    def reset_stats(self):
        self.rockets_left = self.settings.rockets_limit
