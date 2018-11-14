# -*- coding: utf-8 -*-
import pygame
import random

class Person():
    def __init__(self, size, init_pos, settings, screen):
        # size [length(x), width(y)]  init_pos [x, y]
        """ Initialize information. """
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.max_v = 0.225
        self.route_points = self.settings.route_points
        self.reinit(size, init_pos)

    def reinit(self, size, init_pos):
        self._size_x = float(size[0])
        self._size_y = float(size[1])
        self._p_x = float(init_pos[0])
        self._p_y = float(init_pos[1])
        self._v_x = float(0)
        self._v_y = float(0)
        self._moving_up = False
        self._moving_down = False
        self._moving_left = False
        self._moving_right = False
        self.title_v_x = 0.3
        self._routes = [[self._p_x, self._p_y] for i in range(self.route_points)]
        self._now_gif = 0
        self._gifs = [0 for i in range(6)]
        
        self._hp = 10
        self._hit_time = -10
        self.healing_protect = False

        # Load the image (using relative path in Windows)
        for i in range(6):
            self._gifs[i] = pygame.image.load(r".\images\p{0:d}.png".format(i+1))
            self._gifs[i].set_alpha(220)
        self._gif = pygame.transform.scale(self._gifs[0], (int(self._size_x * self.settings.screen_scale), int(self._size_y * self.settings.screen_scale)))
        self.rect = self._gif.get_rect()

        # Load the shield image
        self._shield_img = pygame.image.load(r".\images\shield.png")
        self._shield_img = pygame.transform.scale(self._shield_img, (int(self._size_x*3 * self.settings.screen_scale), int(self._size_y*3 * self.settings.screen_scale)))
        self._shield_rect = self._shield_img.get_rect()

        # Set the position using float
        self.rect.centerx = self._p_x
        self.rect.centery = self._p_y


    def set_velocity(self):
        if self._moving_up and not self._moving_down and not self._moving_left and not self._moving_right:  # 单键操作
            self._v_x = 0.0
            self._v_y = - self.max_v
        elif not self._moving_up and self._moving_down and not self._moving_left and not self._moving_right:
            self._v_x = 0.0
            self._v_y = self.max_v
        elif not self._moving_up and not self._moving_down and self._moving_left and not self._moving_right:
            self._v_x = - self.max_v
            self._v_y = 0.0
        elif not self._moving_up and not self._moving_down and not self._moving_left and self._moving_right:
            self._v_x = self.max_v
            self._v_y = 0.0
        elif self._moving_up and not self._moving_down and self._moving_left and not self._moving_right:  # 双键操作
            self._v_x = - 0.7 * self.max_v
            self._v_y = - 0.7 * self.max_v
        elif self._moving_up and not self._moving_down and not self._moving_left and self._moving_right:
            self._v_x = 0.7 * self.max_v
            self._v_y = - 0.7 * self.max_v
        elif not self._moving_up and self._moving_down and self._moving_left and not self._moving_right:
            self._v_x = - 0.7 * self.max_v
            self._v_y = 0.7 * self.max_v
        elif not self._moving_up and self._moving_down and not self._moving_left and self._moving_right:
            self._v_x = 0.7 * self.max_v
            self._v_y = 0.7 * self.max_v
        elif self._moving_up and not self._moving_down and self._moving_left and self._moving_right:  # 三键操作
            self._v_x = 0.0
            self._v_y = - self.max_v
        elif not self._moving_up and self._moving_down and self._moving_left and self._moving_right:
            self._v_x = 0.0
            self._v_y = self.max_v
        elif self._moving_up and self._moving_down and self._moving_left and not self._moving_right:
            self._v_x = - self.max_v
            self._v_y = 0.0
        elif self._moving_up and self._moving_down and not self._moving_left and self._moving_right:
            self._v_x = self.max_v
            self._v_y = 0.0
        else:
            self._v_x = 0.0
            self._v_y = 0.0

    def move(self):
        self.set_velocity()
        if self._p_x + self._v_x >= 0.0 and self._p_x + self._v_x <= 15.0:
            self._p_x = self._p_x + self._v_x
        if self._p_y + self._v_y >= 0.0 and self._p_y + self._v_y <= 28.0:
            self._p_y = self._p_y + self._v_y
        self.update_routes()
        self.update_gif()

    def move_on_title(self):
        self._p_x = self._p_x + self.title_v_x
        if self._p_x >= 36.0:
            self.title_v_x = 0.1 + random.random()*0.4
            self._p_x = -4.0
            self._p_y = 8.5 + random.random()*3
        self.update_gif(ontitle=True)

    def get_info(self):
        """ Get infomation of the flight. """
        return [[self._p_x, self._p_y], [self._v_x, self._v_y]]

    def get_info_str(self):
        """ Give information string to screen. """
        return ["[Person]         Position: {0:>6.3f} m    {1:>6.3f} m  ".format(self._p_x, self._p_y)
              , "                 Velocity: {0:>6.3f} m/s  {1:>6.3f} m/s".format(self._v_x / self.settings.time_period, self._v_y / self.settings.time_period)]

    def print_info(self):
        """ Print infomation to the teminal. """
        print("[Person]           Position: %9.5f m  %9.5f m     Velocity: %9.5f m/s  %9.5f m/s"
                % (self._p_x, self._p_y, self._v_x / self.settings.time_period, self._v_y / self.settings.time_period))

    def drawing(self):
        """ Draw the image in the specific position """
        self.rect.centerx = self._p_x * self.settings.screen_scale + self.settings.screen_offset
        self.rect.centery = self._p_y * self.settings.screen_scale + self.settings.screen_offset
        self.screen.blit(self._gif, self.rect)

    def draw_shield(self):
        self._shield_rect.centerx = self._p_x * self.settings.screen_scale + self.settings.screen_offset
        self._shield_rect.centery = self._p_y * self.settings.screen_scale + self.settings.screen_offset
        self.screen.blit(self._shield_img, self._shield_rect)

    def update_routes(self):
        temp_points = self.route_points - 1
        for index in range(temp_points):
            self._routes[index][0] = self._routes[index+1][0]
            self._routes[index][1] = self._routes[index+1][1]
        self._routes[temp_points][0] = self._p_x
        self._routes[temp_points][1] = self._p_y

    def get_routes(self):
        return self._routes

    def update_gif(self, ontitle=False):
        if self._now_gif >= 5:
            self._now_gif = 0
        else:
            self._now_gif = self._now_gif + 1
        if not ontitle:
            self._gif = pygame.transform.scale(self._gifs[self._now_gif], (int(self._size_x * self.settings.screen_scale), int(self._size_y * self.settings.screen_scale)))
        else:  # show person on the title, bigger
            self._gif = pygame.transform.scale(self._gifs[self._now_gif], (int(1.4*self._size_x * self.settings.screen_scale), int(1.4*self._size_y * self.settings.screen_scale)))
        self.rect = self._gif.get_rect()

    def get_hp_info(self):
        return [self._hp, self._hit_time]
    
    def hit(self, new_hit_time):
        self._hp = max(self._hp - 1, 0)
        self._hit_time = new_hit_time
    
    def heal(self, new_hit_time):
        self._hp = min(self._hp + 1, 10)
        self._hit_time = new_hit_time
        self.healing_protect = True

