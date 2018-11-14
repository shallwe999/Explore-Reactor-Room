# -*- coding: utf-8 -*-
import pygame

class Boxes():
    def __init__(self, settings, screen):
        """ Initialize information. """
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Load the boxes ([x, y, width, height]  0: protect box  1-4: key box)
        self._boxes = [[6.8, 7.8, 1.4, 1.4], [1, 24.5, 1, 1], [5, 24.5, 1, 1], [9, 24.5, 1, 1], [13, 24.5, 1, 1]]
        self.reinit()
        
    def reinit(self):
        self._open = [False, False, False, False]
        self._opening_time = [0, 0, 0, 0]
        

    def drawing(self):
        """ Draw the boxes in the specific position """
        box = self._boxes[0]
        pygame.draw.rect(self.screen, self.settings.box_color_1, 
                [box[0] * self.settings.screen_scale + self.settings.screen_offset, 
                 box[1] * self.settings.screen_scale + self.settings.screen_offset, 
                 box[2] * self.settings.screen_scale, box[3] * self.settings.screen_scale], 0)

        for i in range(4):
            box = self._boxes[i+1]
            if self._open[i] == True:  # opened
                box_color = self.settings.box_color_2
            elif self.settings.get_key: # get key but not opened
                box_color = self.settings.box_color_3
            else:  # no key
                box_color = self.settings.box_color_3_no_key
            pygame.draw.rect(self.screen, box_color, 
                    [box[0] * self.settings.screen_scale + self.settings.screen_offset, 
                     box[1] * self.settings.screen_scale + self.settings.screen_offset, 
                     box[2] * self.settings.screen_scale, box[3] * self.settings.screen_scale], 0)


    def is_in_protect_box(self, p):
        box = self._boxes[0]
        if p[0] >= box[0] and p[0] <= box[0] + box[2] and p[1] >= box[1] and p[1] <= box[1] + box[3]:
            return True
        else:
            return False

    def is_in_key_box(self, p):
        results = [False, False, False, False]
        for i in range(4):
            box = self._boxes[i+1]
            if p[0] >= box[0] and p[0] <= box[0] + box[2] and p[1] >= box[1] and p[1] <= box[1] + box[3]:
                results[i] = True
        return results

    def update_info(self, settings, person):
        if settings.get_key:
            results = self.is_in_key_box(person.get_info()[0])
            for i in range(4):
                if results[i] == True:
                    self._opening_time[i] = self._opening_time[i] + 1
                    if self._opening_time[i] >= 40:  # 40 time periods
                        self._open[i] = True
                else:
                    self._opening_time[i] = 0

    def all_open(self):
        if self._open == [True, True, True, True]:
            return True
        else:
            return False


