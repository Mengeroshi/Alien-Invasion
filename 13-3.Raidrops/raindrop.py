import pygame
from pygame.sprite import Sprite
 
class Raindrop(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, storm):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = storm.screen
        self.settings = storm.settings
        self.screen_rect = storm.screen.get_rect()

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/raindrop.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

#    def check_edges(self):
#        """Return True if alien is at edge of screen."""
#        #screen_rect = self.screen.get_rect()
#        if self.rect.top < self.screen_rect.bottom
#            #return True
#            print("lel")

    def update(self):
        """Move the alien right or left."""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x