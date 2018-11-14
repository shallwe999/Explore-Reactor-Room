# -*- coding: utf-8 -*-
import pygame
import math
from pygame.sprite import Sprite

class EnemyFlight(Sprite):
    def __init__(self, size, init_pos, settings, screen, rotate_angle=0):
        # size [length(x), width(y)]  init_pos [x, y]  rotate_angle: optional arguments
        """ Initialize information. """
        super(EnemyFlight, self).__init__()

        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.max_v = 0.2  # max 1m/s
        self.attack_radius = 2.1
        self.attack_limit_time = 5.0
        self.route_points = self.settings.route_points
        self.reinit(size, init_pos, rotate_angle)

    def reinit(self, size, init_pos, rotate_angle=0):
        self._size_x = float(size[0])
        self._size_y = float(size[1])
        self._p_x = float(init_pos[0])
        self._p_y = float(init_pos[1])
        self._v_x = 0.0
        self._v_y = 0.0
        self._routes = [[self._p_x, self._p_y] for i in range(self.route_points)]

        self.attack_success_time = 0.0
        self._v = 0.0
        self._rotate_angle = rotate_angle
        self._now_angle = 0

        # Load the image (using relative path in Windows)
        self.image = pygame.image.load(r".\images\f2.jpg")
        self.image = pygame.transform.scale(self.image, (int(self._size_x * self.settings.screen_scale), int(self._size_y * self.settings.screen_scale)))
        self.rect = self.image.get_rect()

        # Set the position using float
        self.rect.centerx = self._p_x
        self.rect.centery = self._p_y


    def set_velocity(self, v):
        self._v = pow(v[0] * v[0] + v[1] * v[1], 0.5)
        if self._v >= self.max_v and self._v > 0:  # limit the max velocity
            self._v_x = v[0] / self._v * self.max_v
            self._v_y = v[1] / self._v * self.max_v
            self._v = self.max_v
        else:
            self._v_x = v[0]
            self._v_y = v[1]
            
        if self._v == 0:
           self._now_angle = math.pi / 2
        elif self._v_y >= 0:
            self._now_angle = math.acos(self._v_x / self._v)
        else:
            self._now_angle = - math.acos(self._v_x / self._v)


    def set_max_v(self, v):
        self.max_v = v

    def move(self):
        """ Let the flight move. (Just according to _v_x and _v_y) """
        self._p_x = self._p_x + self._v_x
        self._p_y = self._p_y + self._v_y
        self.update_routes()

    def move_circle(self):
        """ Let the flight move circularly """
        self._now_angle = self._now_angle + self._rotate_angle
        if self._now_angle >= 2 * math.pi:
            self._now_angle = self._now_angle - 2 * math.pi
        elif self._now_angle < 0:
            self._now_angle = self._now_angle + 2 * math.pi

        self._v_x = self._v * math.cos(self._now_angle)
        self._v_y = self._v * math.sin(self._now_angle)
        self._p_x = self._p_x + self._v_x
        self._p_y = self._p_y + self._v_y
        self.update_routes()

    def get_info(self):
        """ Get infomation of the flight. """
        return [[self._p_x, self._p_y], [self._v_x, self._v_y]]

    def get_info_str(self):
        """ Give information string to screen. """
        return ["[Enemy  Flight]  Position: {0:>6.3f} m    {1:>6.3f} m  ".format(self._p_x, self._p_y)
              , "                 Velocity: {0:>6.3f} m/s  {1:>6.3f} m/s".format(self._v_x / self.settings.time_period, self._v_y / self.settings.time_period)]

    def get_direction(self):
        """ Calculate the moving direction. """
        return self._now_angle

    def print_info(self):
        """ Print infomation to the teminal. """
        print("[Enemy Flight]  Position: %8.4f m  %8.4f m     Velocity: %8.4f m/s  %8.4f m/s"
                % (self._p_x, self._p_y, self._v_x / self.settings.time_period, self._v_y / self.settings.time_period))

    def drawing(self):
        """ Draw the ship in the specific position """
        self.rect.centerx = self._p_x * self.settings.screen_scale + self.settings.screen_offset
        self.rect.centery = self._p_y * self.settings.screen_scale + self.settings.screen_offset
        self.screen.blit(self.image, self.rect)

    def draw_attack_circle(self):
        """ Draw the attack circle """
        if self.attack_success_time > self.attack_limit_time * 0.2:  # display 80% time
            self.attack_success_time = self.attack_success_time - self.settings.time_period
            centerx = int(self._p_x * self.settings.screen_scale + self.settings.screen_offset)
            centery = int(self._p_y * self.settings.screen_scale + self.settings.screen_offset)
            pygame.draw.circle(self.screen, (250, 50, 50), (centerx, centery), int(self.attack_radius * self.settings.screen_scale + 1), 2)
            pygame.draw.circle(self.screen, (250, 50, 50), (centerx, centery), int(self.attack_radius / 3*2 * self.settings.screen_scale + 1), 2)
            pygame.draw.circle(self.screen, (250, 50, 50), (centerx, centery), int(self.attack_radius / 3 * self.settings.screen_scale + 1), 2)

    def update_routes(self):
        temp_points = self.route_points - 1
        for index in range(temp_points):
            self._routes[index][0] = self._routes[index+1][0]
            self._routes[index][1] = self._routes[index+1][1]
        self._routes[temp_points][0] = self._p_x
        self._routes[temp_points][1] = self._p_y

    def get_routes(self):
        return self._routes

    def set_attack_args(self, attack_radius, attack_limit_time):
        self.attack_radius = attack_radius
        self.attack_limit_time = attack_limit_time

    def attack(self, person, boxes):
        p_person = person.get_info()[0]
        if not boxes.is_in_protect_box(p_person):  # not in the protect box
            if pow( pow(self._p_x - p_person[0], 2) + pow(self._p_y - p_person[1], 2) , 0.5 ) <= self.attack_radius:  # in the attack area
                if self.settings.timer - person.get_hp_info()[1] >= self.attack_limit_time:  # out of time limitation
                    person.hit(self.settings.timer)
                    self.attack_success_time = self.attack_limit_time



