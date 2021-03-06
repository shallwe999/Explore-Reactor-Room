# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
import random

class TeamFlight(Sprite):
    def __init__(self, size, init_pos, goal_pos, final_pos, settings, screen):
        # size [length(x), width(y)]  goal_pos [x, y]  init_pos [x, y]  final_pos (of the destination) [x, y]
        """ Initialize information. """
        super(TeamFlight, self).__init__()

        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.max_v = 0.15  # max 1.0m/s
        self.heal_limit_time = 5.0
        self.route_points = self.settings.route_points
        self.reinit(size, init_pos, goal_pos, final_pos)

    def reinit(self, size, init_pos, goal_pos, final_pos):
        self._size_x = float(size[0])
        self._size_y = float(size[1])
        self._p_x = float(init_pos[0])
        self._p_y = float(init_pos[1])
        self._v_x = float(0)
        self._v_y = float(0)
        self._goal_x = float(goal_pos[0])
        self._goal_y = float(goal_pos[1])
        self._final_x = float(final_pos[0])
        self._final_y = float(final_pos[1])
        self._routes = [[self._p_x, self._p_y] for i in range(self.route_points)]

        self.can_heal = True
        self.heal_success_time = 0.0

        # Load the images (using relative path in Windows) (same size)
        self.image1 = pygame.image.load(r".\images\f1_1.png")
        self.image1 = pygame.transform.scale(self.image1, (int(self._size_x * self.settings.screen_scale), int(self._size_y * self.settings.screen_scale)))
        self.image2 = pygame.image.load(r".\images\f1_2.png")
        self.image2 = pygame.transform.scale(self.image2, (int(self._size_x * self.settings.screen_scale), int(self._size_y * self.settings.screen_scale)))
        self.rect = self.image1.get_rect()
        self.image_index = random.randint(1, 2)

        # Load the lazer image
        if self.settings.lazer_shown:
            self.lazer_img = pygame.image.load(r".\images\lazer1.png")
            self.lazer_img_1 = pygame.transform.scale(self.lazer_img, (int(1.9 * self.settings.screen_scale), int(1.9 * self.settings.screen_scale)))
            self.lazer_img_2 = pygame.transform.scale(self.lazer_img, (int(3.8 * self.settings.screen_scale), int(3.8 * self.settings.screen_scale)))

        # Set the position using float
        self.rect.centerx = self._p_x
        self.rect.centery = self._p_y


    def set_velocity(self, v):
        self._v = pow(v[0] * v[0] + v[1] * v[1], 0.5)
        if self._v >= self.max_v:  # limit the max velocity
            self._v_x = v[0] / self._v * self.max_v
            self._v_y = v[1] / self._v * self.max_v
            self._v = self.max_v
        else:
            self._v_x = v[0]
            self._v_y = v[1]

    def set_max_v(self, v):
        self.max_v = v

    def move(self):
        self._p_x = self._p_x + self._v_x
        self._p_y = self._p_y + self._v_y
        self.update_routes()

    def set_goal(self, goal):
        self._goal_x = goal[0]
        self._goal_y = goal[1]

    def get_goal(self):
        return [self._goal_x, self._goal_y]

    def get_info(self):
        """ Get infomation of the flight. """
        return [[self._p_x, self._p_y], [self._v_x, self._v_y]]

    def get_info_str(self):
        """ Give information string to screen. """
        return ["[Team   Flight]  Position: {0:>6.3f} m    {1:>6.3f} m  ".format(self._p_x, self._p_y)
              , "                 Velocity: {0:>6.3f} m/s  {1:>6.3f} m/s".format(self._v_x / self.settings.time_period, self._v_y / self.settings.time_period)]

    def print_info(self):
        """ Print infomation to the teminal. """
        print("[Team  Flight]  Position: %8.4f m  %8.4f m     Velocity: %8.4f m/s  %8.4f m/s"
                % (self._p_x, self._p_y, self._v_x / self.settings.time_period, self._v_y / self.settings.time_period))

    def drawing(self):
        """ Draw the flight in the specific position """
        self.rect.centerx = self._p_x * self.settings.screen_scale + self.settings.screen_offset
        self.rect.centery = self._p_y * self.settings.screen_scale + self.settings.screen_offset
        if self.image_index == 1:
            self.screen.blit(self.image1, self.rect)
            if not self.settings.paused:  # if pause, not move
                self.image_index = 2
        elif self.image_index == 2:
            self.screen.blit(self.image2, self.rect)
            if not self.settings.paused:  # if pause, not move
                self.image_index = 1

    def draw_heal_circle(self):
        """ Draw the attack circle """
        if self.heal_success_time > self.heal_limit_time * 0.2:  # display 80% time
            self.heal_success_time = self.heal_success_time - self.settings.time_period
            if self.settings.lazer_shown:
                # draw two images
                self.lazer_img_1_rect = self.lazer_img_1.get_rect()
                self.lazer_img_1_rect.center = self.rect.center
                self.screen.blit(self.lazer_img_1, self.lazer_img_1_rect)
                self.lazer_img_2_rect = self.lazer_img_2.get_rect()
                self.lazer_img_2_rect.center = self.rect.center
                self.screen.blit(self.lazer_img_2, self.lazer_img_2_rect)
            else:
                # draw three circles
                centerx = int(self._p_x * self.settings.screen_scale + self.settings.screen_offset)
                centery = int(self._p_y * self.settings.screen_scale + self.settings.screen_offset)
                pygame.draw.circle(self.screen, (50, 250, 50), (centerx, centery), int(1.5 * self.settings.screen_scale + 1), 2)
                pygame.draw.circle(self.screen, (50, 250, 50), (centerx, centery), int(1.0 * self.settings.screen_scale + 1), 2)
                pygame.draw.circle(self.screen, (50, 250, 50), (centerx, centery), int(0.5 * self.settings.screen_scale + 1), 2)


    def update_routes(self):
        temp_points = self.route_points - 1
        for index in range(temp_points):
            self._routes[index][0] = self._routes[index+1][0]
            self._routes[index][1] = self._routes[index+1][1]
        self._routes[temp_points][0] = self._p_x
        self._routes[temp_points][1] = self._p_y

    def get_routes(self):
        return self._routes

    def set_heal_args(self, heal_limit_time):
        self.heal_limit_time = heal_limit_time

    def heal(self, person, boxes):
        if self.can_heal:  # can only heal once
            p_person = person.get_info()[0]
            if not boxes.is_in_protect_box(p_person):  # not in the protect box
                if pow( pow(self._p_x - p_person[0], 2) + pow(self._p_y - p_person[1], 2) , 0.5 ) <= 1.5:  # (heal radius 1.5m) in the heal area
                    if self.settings.timer - person.get_hp_info()[1] >= self.heal_limit_time:  # without time limitation
                        person.heal(self.settings.timer)
                        self.can_heal = False
                        self.heal_success_time = self.heal_limit_time

    def reach_final_goal(self):
        if abs(self._p_x - self._final_x) <= 0.15 and abs(self._p_y - self._final_y) <= 0.15:  #小于一个阈值的时候算到达
            return True
        else:
            return False


