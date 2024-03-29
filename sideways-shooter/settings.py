class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.rocket_speed = 1.5

        # Bullet settings
        self.bullet_speed = 4
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Alien Settings
        self.alien_speed = 1
        self.fleet_direction = 1
        self.fleet_drop_speed = 40
        
        #Stats
        self.rockets_limit = 3
        