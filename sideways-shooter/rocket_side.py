import pygame

class Rocket:
    def __init__( self, Launcher):
        """Initialize the ship and set its starting position."""
        self.screen = Launcher.screen
        self.settings = Launcher.settings
        self.screen_rect = Launcher.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/rocket-side.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the left center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's horizontal position.
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.rocket_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.rocket_speed
            
        # Update rect object from self.x.
        if self.moving_up or self.moving_down:
            self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)