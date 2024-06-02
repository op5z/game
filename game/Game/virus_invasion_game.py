import sys
import pygame
import random
from pygame.sprite import Group
from settings import Settings
from robot import Robot
from virus import Virus
from laser_beam import LaserBeam

class VirusInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound("sound/fire.wav")
        self.virus_destroy_sound = pygame.mixer.Sound("sound/su.wav")

        # الحصول على معلومات الشاشة الحالية
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        # تعيين حجم الشاشة على كامل الشاشة
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.bg_image = pygame.image.load("images/bg22.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Virus Invasion Game")
        self.laser_beams = Group()
        self.viruses = Group()
        self.robot = Robot(self)
        self.virus_destroyed_count = 0
        self.robot_lives = 3
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.robot.update()
            self._update_laser_beams()
            self._update_screen()
            self._update_viruses()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.USEREVENT + 1:
                self._create_virus()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.robot.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.robot.moving_left = True
        elif event.key == pygame.K_UP:
            self.robot.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.robot.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.robot_lives > 0:
                self._fire_laser_beam()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.robot.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.robot.moving_left = False
        elif event.key == pygame.K_UP:
            self.robot.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.robot.moving_down = False

    def _fire_laser_beam(self):
        if len(self.laser_beams) < self.settings.laser_beams_allowed:
            new_laser_beam = LaserBeam(self)
            self.laser_beams.add(new_laser_beam)
            self.laser_sound.play()

    def _update_laser_beams(self):
        self.laser_beams.update()
        for laser_beam in self.laser_beams.copy():
            if laser_beam.rect.bottom <= 0:
                self.laser_beams.remove(laser_beam)
        collisions = pygame.sprite.groupcollide(self.laser_beams, self.viruses, True, True)
        if collisions:
            self.virus_destroyed_count += len(collisions)
            self.virus_destroy_sound.play()

    def _update_screen(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.robot.blitme()
        for laser_beam in self.laser_beams.sprites():
            laser_beam.draw_laser_beam()
        for virus in self.viruses.sprites():
            virus.blitme()
        self._show_virus_destroyed_count()
        self._show_robot_lives()
        pygame.display.flip()

    def _create_fleet(self):
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)

    def _create_virus(self):
        virus = Virus(self)
        virus_width, virus_height = virus.rect.size
        virus.x = random.randint(0, self.settings.screen_width - virus_width)
        virus.rect.x = virus.x
        virus.rect.y = random.randint(-10 * virus_height, -virus_height)
        self.viruses.add(virus)

    def _update_viruses(self):
        for virus in self.viruses.sprites():
            virus.rect.y += self.settings.base_virus_speed
            if virus.rect.top > self.settings.screen_height:
                self.viruses.remove(virus)
                self.robot_lives -= 1
                if self.robot_lives <= 0:
                    self._game_over()
            elif virus.rect.colliderect(self.robot.rect):
                self.viruses.remove(virus)
                self.robot_lives -= 1
                if self.robot_lives <= 0:
                    self._game_over()

    def _show_virus_destroyed_count(self):
        font = pygame.font.SysFont(None, 48)
        virus_destroyed_count_text = font.render(f"Score: {self.virus_destroyed_count}", True, (0, 0, 0))
        self.screen.blit(virus_destroyed_count_text, (10, 10))

    def _show_robot_lives(self):
        font = pygame.font.SysFont(None, 48)
        robot_lives_text = font.render(f"Lives: {self.robot_lives}", True, (0, 0, 0))
        self.screen.blit(robot_lives_text, (self.settings.screen_width - 150, 10))

    def _game_over(self):
        high_score = self._read_high_score()
        if self.virus_destroyed_count > high_score:
            self._write_high_score()
        font = pygame.font.SysFont(None, 64)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        score_text = font.render(f"High Score: {high_score}", True, (0, 0, 255))
        self.screen.blit(game_over_text, (self.settings.screen_width // 2 - 150, self.settings.screen_height // 2 - 50))
        self.screen.blit(score_text, (self.settings.screen_width // 2 - 150, self.settings.screen_height // 2 + 50))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self._reset_game()
                    elif event.key == pygame.K_q:
                        sys.exit()

    def _read_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def _write_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.virus_destroyed_count))

    def _reset_game(self):
        self.virus_destroyed_count = 0
        self.robot_lives = 3
        self.viruses.empty()
        self.laser_beams.empty()
        self._create_fleet()


if __name__ == '__main__':
    vi = VirusInvasion()
    vi.run_game()
