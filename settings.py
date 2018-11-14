# -*- coding: utf-8 -*-
import pygame
import sys
import json

class Settings():
    """ Store the settings """

    def __init__(self, settings_json_file):
    # Initialize settings

        # Load json file first
        with open(settings_json_file, 'r', encoding='utf-8') as f:
            load_data = json.load(f)
            window_size = int(load_data['window_size'])
            if window_size < 15 or window_size > 30:
                print("[INFO] Program settings argument 'window_size' error. Fail to launch.")
                sys.exit()
            route_points = int(load_data['route_points'])
            if route_points < 10 or route_points > 100:
                print("[INFO] Program settings argument 'route_points' error. Fail to launch.")
                sys.exit()
            lazer_shown = bool(load_data['lazer_shown'])

        # Set screen size
        self.screen_scale = window_size  # (fit 15~30  best 25) decided in json file
        self.screen_offset = 30  # (best 30)

        # Set colors and fonts
        self.bg_color = (230, 230, 230)
        self.eg_color_1 = (255, 153, 51)
        self.eg_color_2 = (255, 180, 50)
        self.title_color = (20, 20, 20)
        self.choose_color = (225, 205, 90)
        self.box_color_1 = (100, 100, 200)
        self.box_color_2 = (100, 200, 100)
        self.box_color_3 = (200, 100, 100)
        self.box_color_3_no_key = (150, 100, 100)
        self.team_route_color = (50, 50, 220)
        self.enemy_route_color = (220, 50, 50)
        self.person_route_color = (220, 50, 220)
        self.font_color_1 = (254, 67, 101)
        self.font_color_2 = (131, 175, 161)
        self.title_font1 = pygame.font.SysFont("Times New Roman", int(2.2 * self.screen_scale), True, True)
        self.title_font2 = pygame.font.SysFont("Times New Roman", int(1.1 * self.screen_scale), True, True)
        self.title_font3 = pygame.font.SysFont("Times New Roman", int(1.2 * self.screen_scale), True, True)
        self.title_font4 = pygame.font.SysFont("Consolas", int(0.6 * self.screen_scale) - 1, True, True)
        self.bottom_font = pygame.font.SysFont("Times New Roman", int(0.5 * self.screen_scale + 1), True, True)

        # Load the icons (using relative path in Windows)
        icon_size = int(1.8 * self.screen_scale)
        self._img_protected = pygame.image.load(r".\images\protected.png")
        self._img_protected = pygame.transform.scale(self._img_protected, (icon_size, icon_size))
        self._img_mission1 = pygame.image.load(r".\images\mission1.png")
        self._img_mission1 = pygame.transform.scale(self._img_mission1, (icon_size, icon_size))
        self._img_mission1_u = pygame.image.load(r".\images\mission1_u.png")
        self._img_mission1_u = pygame.transform.scale(self._img_mission1_u, (icon_size, icon_size))
        self._img_mission2 = pygame.image.load(r".\images\mission2.png")
        self._img_mission2 = pygame.transform.scale(self._img_mission2, (icon_size, icon_size))
        self._img_mission2_u = pygame.image.load(r".\images\mission2_u.png")
        self._img_mission2_u = pygame.transform.scale(self._img_mission2_u, (icon_size, icon_size))
        self._img_mission3 = pygame.image.load(r".\images\mission3.png")
        self._img_mission3 = pygame.transform.scale(self._img_mission3, (icon_size, icon_size))
        self._img_mission3_u = pygame.image.load(r".\images\mission3_u.png")
        self._img_mission3_u = pygame.transform.scale(self._img_mission3_u, (icon_size, icon_size))

        # Load the progress bar (using relative path in Windows)
        self._progbar1 = pygame.image.load(r".\images\prog_bar1.png")
        self._progbar1 = pygame.transform.scale(self._progbar1, (int(12 * self.screen_scale), int(1.2 * self.screen_scale)))
        self._progbar2 = pygame.image.load(r".\images\prog_bar2.png")
        self._progbar3 = pygame.image.load(r".\images\prog_bar3.png")
        self._progbar3 = pygame.transform.scale(self._progbar3, (int(12 * self.screen_scale), int(1.2 * self.screen_scale)))
        self._progbar4 = pygame.image.load(r".\images\prog_bar4.png")

        # Load the button
        self._button1 = pygame.image.load(r".\images\button1.png")
        self._button2 = pygame.image.load(r".\images\button2.png")

        # Load the loading image
        self._loading_img = pygame.image.load(r".\images\loading.png")
        _loading_img_rect = self._loading_img.get_rect()
        self._loading_img = pygame.transform.scale(self._loading_img, (int(_loading_img_rect.width * self.screen_scale / 28), int(_loading_img_rect.height * self.screen_scale / 28)))

        # other settings
        self.choose_index = 0
        self.run_active = False
        self.have_run = False  # if run_active has been activated, do not launch cmd thread again
        self.selecting_mode = False
        self.game_mode = 0  # 0: training  1: easy  2: medium  3: hard
        self.reset_request = False  # game reset
        self.paused = False  # game paused
        self.init_game_args()  # initialize arguments

        # Set APF settings
        self.k_att = 1.2
        self.k_rep = 0.3
        self.d_o = 5
        self.d_dr = 0.6
        self.adv_length = 0.05
        self.k_mvrep = 1
        self.angle_multi = 3.14159265 / 3
        self.k_force = 0.02

        # enemy_mission_args: easy, medium, hard
        # [0]velocity factor; [1]random offset 1; [2]random offset 2;
        # [3]max_v(0.9m/s(0.135) 1.2m/s(0.18) 1.4m/s(0.21)); [4]attack radius; [5]attack limit period;
        # [6]destination offset to person; [7]box open time periods
        self.enemy_mission_args = [[0.6, 2, 3, 0.1348, 2.1, 5.5, 2.0, 50], [0.9, 1.5, 2.25, 0.1798, 2.4, 5.0, 2.2, 55], [1.2, 1, 1.5, 0.2098, 2.7, 4.5, 2.4, 60]]

        # other settings
        self.route_points = route_points
        self.lazer_shown = lazer_shown


    def init_game_args(self):
        # init arguments
        self.show_instr = False
        self.show_keyboard = False
        self.show_hiscore = False
        self.show_route = False
        self.clean_request = False  # clean hiscore request
        self.draw_person = True  # to show the -1HP effect

        self.enemy_status = 2    # 0: hover  1: move straight  2: move circular  3: approach team flights  4~6: performing defend task
        self.enemy_status_changed = False  # enemy_status is changed, arguments should be reset
        self.timer = 0.0
        self.time_period = 0.15
        self.out_of_bound_flag = False
        self.out_times = 0
        self.person_direction = 0  # 0: stand  1: up  2: down  3: left  4: right
        self.crack_qrcode = False  # get the QRcode of the boxes
        self.get_key = False  # get the password of the boxes
        self.all_open = False  # open all boxes
        self.failed = False
        self.complete = False
        self.complete_time = 0.0
        self.hiscore_recorded = False
        self.show_immune_time = 0

        self.clock_1 = 30  # 30 periods per clock
        self.font_color_1and2 = self.font_color_1


    def change_font_color(self):
        if self.font_color_1and2 == self.font_color_1:
            self.font_color_1and2 = self.font_color_2
        else:
            self.font_color_1and2 = self.font_color_1

