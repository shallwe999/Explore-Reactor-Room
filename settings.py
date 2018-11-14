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

        # Set screen size
        self.screen_scale = window_size  # (fit 15~30  best 25) decided in json file
        self.screen_offset = 30  # (best 30)

        # Set colors and fonts
        self.bg_color = (230, 230, 230)
        self.eg_color = (255, 153, 51)
        self.title_color = (20, 20, 20)
        self.box_color_1 = (100, 100, 200)
        self.box_color_2 = (100, 200, 100)
        self.box_color_3 = (200, 100, 100)
        self.box_color_3_no_key = (150, 100, 100)
        self.team_route_color = (50, 50, 220)
        self.enemy_route_color = (220, 50, 50)
        self.person_route_color = (220, 50, 220)
        self.font_color_1 = (254, 67, 101)
        self.title_font1 = pygame.font.SysFont("Times New Roman", int(2.2 * self.screen_scale), True, True)
        self.title_font2 = pygame.font.SysFont("Times New Roman", int(1.1 * self.screen_scale), True, True)
        self.title_font3 = pygame.font.SysFont("Times New Roman", int(1.2 * self.screen_scale), True, True)
        self.title_font4 = pygame.font.SysFont("Consolas", int(0.6 * self.screen_scale) - 1, True, True)
        self.bottom_font = pygame.font.SysFont("Times New Roman", int(0.5 * self.screen_scale + 1), True, True)

        # other settings
        self.run_active = False
        self.have_run = False  # if run_active has been activated, do not launch cmd thread again
        self.selecting_mode = False
        self.game_mode = 0  # 0: training  1: easy  2: medium  3: hard
        self.reset_request = False  # game reset
        self.paused = False  # game paused
        self.init_game_args()  # initialize arguments

        # Set APF settings
        self.k_att = 1.2
        self.k_rep = 0.4
        self.d_o = 5
        self.d_dr = 0.5
        self.adv_length = 0.05
        self.k_mvrep = 1
        self.angle_multi = 3.14159265 / 3
        self.k_force = 0.02

        # enemy_mission_args: easy, medium, hard
        # [0]velocity factor; [1]random offset 1; [2]random offset 2;
        # [3]max_v(0.9m/s(0.18) 1.2m/s(0.24) 1.4m/s(0.28)); [4]attack radius; [5]attack limit period; [6]destination offset to person
        self.enemy_mission_args = [[0.6, 2, 3, 0.1798, 2.1, 5.0, 2.0], [0.9, 1.5, 2.25, 0.2398, 2.4, 5.0, 2.2], [1.2, 1, 1.5, 0.2798, 2.7, 4.0, 2.4]]

        # other settings
        self.route_points = route_points


    def init_game_args(self):
        # init arguments
        self.show_instr = False
        self.show_keyboard = False
        self.show_hiscore = False
        self.show_route = False
        self.clean_request = False  # clean hiscore request

        self.enemy_status = 2    # 0: hover  1: move straight  2: move circular  3: approach team flights  4~6: performing defend task
        self.timer = 0.0
        self.time_period = 0.2
        self.out_of_bound_flag = False
        self.out_times = 0
        self.person_direction = 0  # 0: stand  1: up  2: down  3: left  4: right
        self.get_key = False  # get the password of the boxes
        self.all_open = False  # open all boxes
        self.failed = False
        self.complete = False
        self.complete_time = 0.0
        self.hiscore_recorded = False
