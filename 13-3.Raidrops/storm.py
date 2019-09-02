import sys

import pygame

from settings import Settings
from raindrop import Raindrop


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.raindrops = pygame.sprite.Group()

        self._create_storm()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_raindrops()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            sys.exit()

    def _update_raindrops(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._storm_direction()
        #self.raindrops.update()

    def _create_storm(self):
        """Create the fleet of aliens."""
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size

        available_space_x = self.settings.screen_width #- (2 * raindrop_width)
        number_raindrops_x = available_space_x // (2 * raindrop_width)

        available_space_y = self.settings.screen_height - (5* raindrop_height)
        number_raindrop_rows = available_space_y // (2 * raindrop_height)

        for raindrop_row in range(number_raindrop_rows):
            for raindrops_num in range (number_raindrops_x):
                self._create_raindrop(raindrops_num, raindrop_row)
                
    def _create_raindrop(self, raindrops_num, raindrop_row):
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size

        raindrop.x = raindrop_width + 2 * raindrop_width * raindrops_num
        raindrop.rect.x = raindrop.x

        raindrop.rect.y = raindrop.rect.height + 2 * raindrop.rect.height *  raindrop_row
        self.raindrops.add(raindrop)    
        
            
    def _storm_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for raindrop in self.raindrops.sprites():
            raindrop.rect.y += self.settings.storm_speed
            

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        self.raindrops.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
