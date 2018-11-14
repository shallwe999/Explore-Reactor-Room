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
        
        # Load the box image (using relative path in Windows)
        self._boximage = pygame.image.load(r".\images\box.png")
        self._boximage = pygame.transform.scale(self._boximage, (int(1.4 * self.settings.screen_scale), int(0.7 * self.settings.screen_scale)))

        # Load the progress bar from settings
        self._progbar1 = self.settings._progbar1
        self._progbar2 = self.settings._progbar2
        self._progbar3 = self.settings._progbar3
        self._progbar4 = self.settings._progbar4


    def reinit(self):
        self._open = [False, False, False, False]
        self._opening_time = [0, 0, 0, 0]
        if self.settings.game_mode == 0:
            self._unlock_finish_time = 40
        else:
            self._unlock_finish_time = self.settings.enemy_mission_args[self.settings.game_mode - 1][7]
        self._crack_time = 0
        self._crack_finish_time = 30


    def drawing(self):
        """ Draw the boxes in the specific position """
        box = self._boxes[0]
        pygame.draw.rect(self.screen, self.settings.box_color_1, 
                [box[0] * self.settings.screen_scale + self.settings.screen_offset, 
                 box[1] * self.settings.screen_scale + self.settings.screen_offset, 
                 box[2] * self.settings.screen_scale, box[3] * self.settings.screen_scale], 0)

        self.rect = self._boximage.get_rect()
        for i in range(4):
            self.rect.centerx = (self._boxes[i+1][0] + self._boxes[i+1][3]/2) * self.settings.screen_scale + self.settings.screen_offset
            self.rect.centery = 26 * self.settings.screen_scale + self.settings.screen_offset
            self.screen.blit(self._boximage, self.rect)

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
            if self._opening_time[i] > 0 and not self._open[i] and not self.settings.out_of_bound_flag:  # draw the progress bar
                self.draw_progress_bar_1(i)

        if self._crack_time > 0 and not self.settings.out_of_bound_flag:  # draw the progress bar
                self.draw_progress_bar_2()


    def draw_progress_bar_1(self, index):
        # background progress bar
        rect = self._progbar3.get_rect()
        rect.centerx = 7.5 * self.settings.screen_scale + self.settings.screen_offset
        rect.centery = 15 * self.settings.screen_scale + self.settings.screen_offset
        self.screen.blit(self._progbar3, rect)

        # running progress bar
        tmp_progbar = pygame.transform.scale(self._progbar4, (int(12*self._opening_time[index]/self._unlock_finish_time*0.975 * self.settings.screen_scale), int(0.6 * self.settings.screen_scale)))
        rect.x += rect.width * 0.015
        rect.y += rect.height * 0.13
        self.screen.blit(tmp_progbar, rect)

        # text
        text_image = self.settings.title_font3.render("Unlocking...", True, self.settings.title_color, None)
        rect.centery -= 2 * self.settings.screen_scale
        self.screen.blit(text_image, rect)

    def draw_progress_bar_2(self):
        # background progress bar
        rect = self._progbar3.get_rect()
        rect.centerx = 7.5 * self.settings.screen_scale + self.settings.screen_offset
        rect.centery = 15 * self.settings.screen_scale + self.settings.screen_offset
        self.screen.blit(self._progbar3, rect)

        # running progress bar
        tmp_progbar = pygame.transform.scale(self._progbar4, (int(12*self._crack_time/self._crack_finish_time*0.975 * self.settings.screen_scale), int(0.6 * self.settings.screen_scale)))
        rect.x += rect.width * 0.015
        rect.y += rect.height * 0.13
        self.screen.blit(tmp_progbar, rect)

        # text
        text_image = self.settings.title_font3.render("Cracking...", True, self.settings.title_color, None)
        rect.centery -= 2 * self.settings.screen_scale
        self.screen.blit(text_image, rect)


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
                    if self._opening_time[i] > self._unlock_finish_time:
                        self._open[i] = True
                        self._opening_time[i] = 0
                else:
                    self._opening_time[i] = 0

    def all_open(self):
        if self._open == [True, True, True, True]:
            return True
        else:
            return False

    def crack(self, all_reach_final_goal):
        if all_reach_final_goal:
            self._crack_time = self._crack_time + 1
            if self._crack_time > self._crack_finish_time:
                self.settings.crack_qrcode = True  # 全部到达密码箱前，破解得到二维码
                self._crack_time = 0
        else:
            self._crack_time = 0


