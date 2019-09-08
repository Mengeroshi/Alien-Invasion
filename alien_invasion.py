import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from sarturn import Saturn
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from dificulty import Hard

from  random import randint

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

        self.ship = Ship(self)
        self.saturn =Saturn(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.stats = GameStats(self)
        self.play_button = Button(self, "Play")

        self.proof_button = Hard(self, "Hard")

        self._create_fleet()
        self._create_constellation()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:    
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked  and not self.stats.game_active:
            self._start_game()
            

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
            
        self.ship.center_ship()

        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
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
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break    


    def _ship_hit(self):
        if self.stats.ships_left > 0:
        #Decrement the ships by 1
            self.stats.ships_left -= 1

            #Erease remaining bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #Pause the game
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    

    def _create_fleet(self):
        
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2* alien_height)
        
        for row_number  in range(number_rows):
            for alien_number  in  range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien.rect.height * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_constellation(self):
        star = Star(self)

        #Determine horizontal space
        star_width, star_height = star.rect.size
        milkyway_x = self.settings.screen_width #- (2* star_width)
        number_stars = milkyway_x // (1* star_width)

        #Determine vertical space
        milkyway_y = self.settings.screen_height
        number_star_rows = milkyway_y // (2*star_height)

        for row_star in range (number_star_rows):
            for star_number  in range (number_stars):
                self._create_star(star_number, row_star)

    def _create_star(self, star_number, row_star):
        star = Star(self)
        star_width, star_height = star.rect.size
        #Create a line of stars
        star.x = star_width + 2 * star_width * randint(-20,star_number)
        star.rect.x  = star.x
        #Create a serie of row of stars
        star.rect.y = star.rect.height + 2 * star_height * randint(-20,row_star)
        self.stars.add(star)   

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.saturn.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        #self.stars.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()
            self.proof_button.draw_button()
            #self.proof_button_2.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()