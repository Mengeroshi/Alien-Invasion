
import pygame
import sys
from settings import Settings
from bullet import Bullet
from alien import Alien
from rocket_side import Rocket
from game_stats import GameStats
from time import sleep

class Launcher:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Rocket Launcher")

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.stats = GameStats(self)

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.rocket.update()
                self._update_bullets()
                self._update_alien()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.x > self.settings.screen_width:
                 self.bullets.remove(bullet)
                 
        self._check_bullet_alien_collision()
        

    def _check_bullet_alien_collision(self):    
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.rocket, self.aliens):
            self._rocket_hit()
        
        self._check_aliens_bottom()

    
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                self._rocket_hit()
                break    


    def _rocket_hit(self):
        if self.stats.rockets_left > 0:
            self.stats.rockets_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.rocket.center_ship()

            sleep(0.5)

        else: self.stats.game_active = False        


    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_height #-  (2* alien_height)
        number_aliens_y  = available_space_y // (2* alien_height)
        
        rocket_width = self.rocket.rect.width
        availble_space_x = self.settings.screen_width 
        number_rows = availble_space_x // (2* alien_width) - 5 

        for row_number in  range (number_rows):
            for alien_number in range(number_aliens_y):
                self._create_alien(alien_number, row_number)
        

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        rocket_width = self.rocket.rect.width

        alien.y = alien_height + 2 * alien_height * alien_number
        alien.rect.y = alien.y

        alien.rect.x = (alien.rect.width + 2 * alien.rect.width * row_number)  + ((8 * alien_width) + rocket_width)
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.rocket.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        self.aliens.draw(self.screen)
        
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    rckt = Launcher()
    rckt.run_game()