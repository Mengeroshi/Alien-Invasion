import pygame

class Rocket:
    def __init__( self, Launcher):
        """Initialize the ship and set its starting position."""
        self.screen = Launcher.screen
        self.settings = Launcher.settings
        self.screen_rect = Launcher.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/rocket_i.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Store a decimal value for the ship's horizontal position.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.rocket_speed
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.rocket_speed
        
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.settings.rocket_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.settings.rocket_speed
            
        # Update rect object from self.x.
        if self.moving_up or self.moving_down:
            self.rect.centery = self.centery
        elif self.moving_left or self.moving_right:
            self.rect.centerx = self.centerx

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)