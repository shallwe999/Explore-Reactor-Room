# -*- coding: utf-8 -*-
import sys
import pygame

def check_events(settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd):
    """ Monitor the events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cmd_thread.stop()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, settings, person)


def update_screen(settings, screen, team_flights, enemy_flights, person, boxes, passwd, sbd):
    """ Update the images """
    # Rewhite screen
    screen.fill(settings.bg_color)

    if settings.run_active:
        # Write edges and boxes
        zone_width = 15 * settings.screen_scale
        zone_height = 28 * settings.screen_scale
        pygame.draw.rect(screen, settings.eg_color_2, [settings.screen_offset, settings.screen_offset, zone_width, zone_height], 4)
        pygame.draw.rect(screen, settings.eg_color_1, [settings.screen_offset, settings.screen_offset, zone_width, zone_height], 2)
        boxes.drawing()

        draw_timer(settings, screen)
        draw_data(settings, screen, team_flights, enemy_flights, person, boxes)

        if settings.crack_qrcode and not settings.get_key:
            passwd.draw_qrcode([7.5, 4])  # draw QR code

        # draw flights and person
        for team in team_flights.sprites():
            team.draw_heal_circle()
        for enemy in enemy_flights.sprites():
            enemy.draw_attack_circle()
        if settings.draw_person or settings.paused:  # to show the -1HP effect
            person.drawing()
        if ((person.healing_protect and settings.timer - person.get_hp_info()[1] < 5.0-0.1)
                or settings.timer - person.get_hp_info()[1] < settings.show_immune_time
                or boxes.is_in_protect_box(person.get_info()[0])):
            person.draw_shield()
        for team in team_flights.sprites():
            team.drawing()
        for enemy in enemy_flights.sprites():
            enemy.drawing()

        if settings.show_route:
            draw_routes(settings, screen, team_flights, enemy_flights, person)

        if settings.timer / settings.time_period <= 20:  # ready go
            show_ready_go(settings, screen)

        if settings.paused:  # paused
            show_pause(settings, screen)
    
    # Add title
    if not settings.run_active:
        draw_title(settings, screen)
        person.drawing()
        person.move_on_title()
    
    # show select mode
    if settings.selecting_mode:
        screen.fill(settings.bg_color)
        show_selecting_mode(settings, screen)

    # show instructions
    if settings.show_instr:
        screen.fill(settings.bg_color)
        show_instructions(settings, screen)
    # show key config
    elif settings.show_keyboard:
        screen.fill(settings.bg_color)
        show_key_config(settings, screen)
    # show hiscore
    elif settings.show_hiscore:
        screen.fill(settings.bg_color)
        show_scoreboard(settings, screen, sbd)

    draw_info(settings, screen)

    # See the screen
    pygame.display.flip()


def update_screen_with_loading(settings, screen):
    """ Update the screen only with the loading text """
    screen.fill(settings.bg_color)
    show_loading_image(settings, screen)
    draw_info(settings, screen)
    # See the screen
    pygame.display.flip()


def check_keydown_events(event, settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd):
    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
        if not settings.run_active and not settings.show_instr and not settings.show_keyboard and not settings.show_hiscore:  # in main menu to enter
            if settings.choose_index % 5 == 0:  # start the game
                settings.run_active = True
                if not settings.have_run:
                    settings.have_run = True
                    cmd_thread.start()
                settings.selecting_mode = True  # start to select mode
            elif settings.choose_index % 5 == 1:
                settings.show_instr = True
            elif settings.choose_index % 5 == 2:
                settings.show_keyboard = True
            elif settings.choose_index % 5 == 3:
                settings.show_hiscore = True
            elif settings.choose_index % 5 == 4:  # quit
                cmd_thread.stop()
                sys.exit()
            settings.choose_index = 0
        elif settings.selecting_mode:  # in game mode to enter
            settings.selecting_mode = False
            settings.game_mode = settings.choose_index % 4
            settings.choose_index = 0
            settings.reset_request = True
            update_screen_with_loading(settings, screen)
    elif event.key == pygame.K_ESCAPE:
        if settings.run_active or settings.show_instr or settings.show_keyboard or settings.show_hiscore:  # back to menu
            settings.show_instr = False
            settings.show_keyboard = False
            settings.show_hiscore = False
            settings.run_active = False
            settings.selecting_mode = False
            settings.choose_index = 0
            person.reinit([0.8, 0.8], [7.5, 0.9])  # reinit person moving on the title
        else:  # quit the program
            cmd_thread.stop()
            sys.exit()
    elif event.key == pygame.K_c:
        if settings.run_active and not settings.paused:
            cmd_thread.input_request()
    elif event.key == pygame.K_r:
        if settings.show_hiscore:
            if not settings.clean_request:  # press r again to assure
                settings.clean_request = True
            else:  # pressed again
                settings.clean_request = False
                sbd.clean_hiscore()
                sbd.write_hiscore()
        elif settings.run_active:
            settings.show_route = not settings.show_route
    elif event.key == pygame.K_p:
        if settings.run_active:
            settings.paused = not settings.paused
    elif event.key == pygame.K_i:
        print_info(team_flights, enemy_flights)
    elif event.key == pygame.K_F1:
        if settings.show_keyboard or settings.show_hiscore:
            settings.show_keyboard = False
            settings.show_hiscore = False
            settings.paused = not settings.paused
        settings.show_instr = not settings.show_instr
        settings.paused = not settings.paused
    elif event.key == pygame.K_F2:
        if settings.show_instr or settings.show_hiscore:
            settings.show_instr = False
            settings.show_hiscore = False
            settings.paused = not settings.paused
        settings.show_keyboard = not settings.show_keyboard
        settings.paused = not settings.paused
    elif event.key == pygame.K_F3:
        if settings.show_instr or settings.show_keyboard:
            settings.show_instr = False
            settings.show_keyboard = False
            settings.paused = not settings.paused
        settings.show_hiscore = not settings.show_hiscore
        settings.clean_request = False
        settings.paused = not settings.paused
    elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 0
            settings.enemy_status_changed = True
    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 1
            settings.enemy_status_changed = True
    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 2
            settings.enemy_status_changed = True
    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 3
            settings.enemy_status_changed = True
    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 4
            settings.enemy_status_changed = True
    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 5
            settings.enemy_status_changed = True
    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 6
            settings.enemy_status_changed = True
    elif event.key == pygame.K_UP:
        if not settings.run_active or settings.selecting_mode:
            settings.choose_index -= 1
        elif settings.run_active:
            person._moving_up = True
    elif event.key == pygame.K_DOWN:
        if not settings.run_active or settings.selecting_mode:
            settings.choose_index += 1
        elif settings.run_active:
            person._moving_down = True
    elif event.key == pygame.K_LEFT:
        if settings.run_active:
            person._moving_left = True
    elif event.key == pygame.K_RIGHT:
        if settings.run_active:
            person._moving_right = True


def check_keyup_events(event, settings, person):
    if event.key == pygame.K_UP:
        if settings.run_active:
            person._moving_up = False
    elif event.key == pygame.K_DOWN:
        if settings.run_active:
            person._moving_down = False
    elif event.key == pygame.K_LEFT:
        if settings.run_active:
            person._moving_left = False
    elif event.key == pygame.K_RIGHT:
        if settings.run_active:
            person._moving_right = False


def draw_string_framework(settings, screen, string, string_font, string_color, background_color,
        x_offset, y_offset, get_centered=False, image_height_offset=0, button_drawn=False, draw_button_chosen=False):
    """ Draw the strings onto the screen quickly. """
    # If get_center is false, default x and y are zeros.
    screen_rect = screen.get_rect()
    image = string_font.render(string, True, string_color, background_color)
    image_rect = image.get_rect()
    image_rect.x = 0
    image_rect.y = 0
    if get_centered:
        image_rect.center = screen_rect.center
    image_rect.x += x_offset
    image_rect.y += y_offset + image_height_offset * image_rect.height

    if button_drawn:
        draw_button(settings, screen, image_rect, draw_button_chosen)
    screen.blit(image, image_rect)


def draw_info(settings, screen):
    str0 = "Explore Reactor Room (Flight Route Simulator)   Author: Shallwe   Date:2018/11/14   Version: 1.1.2"
    str0_font = settings.bottom_font
    pos_x = 5
    pos_y = screen.get_rect().height - 5
    draw_string_framework(settings, screen, str0, str0_font,
            settings.title_color, settings.bg_color, pos_x, pos_y, image_height_offset=-1)


def draw_title(settings, screen):
    image = pygame.image.load(r".\images\title.png")
    rect = image.get_rect()
    image = pygame.transform.scale(image, (int(rect.width * settings.screen_scale / 34), int(rect.height * settings.screen_scale / 34)))
    rect = image.get_rect()
    rect.center = screen.get_rect().center
    rect.centery -= 125 + 3 * settings.screen_scale
    screen.blit(image, rect)

    pos_offset = 20 - settings.screen_scale
    title_strings = ["Start", 
                    "Instructions", 
                    "Keyboard config", 
                    "Scoreboard", 
                    "Exit"]

    for index in range(5):
        if index == (settings.choose_index % 5):
            color = settings.choose_color
            button_chosen = True
        else:
            color = settings.title_color
            button_chosen = False
        draw_string_framework(settings, screen, title_strings[index], settings.title_font3, color, None, 
                0, pos_offset, get_centered=True, button_drawn=True, draw_button_chosen=button_chosen)
        pos_offset += 2 * settings.screen_scale


def draw_timer(settings, screen):
    if not settings.complete and not settings.failed:
        time_str = "Simulation time: {0:.2f} s".format(settings.timer)
        color = settings.title_color
    else:
        time_str = "Simulation time: {0:.2f} s".format(settings.complete_time)
        color = settings.font_color_1and2

    pos_x = 16 * settings.screen_scale + 2 * settings.screen_offset
    pos_y = settings.screen_offset - 5
    draw_string_framework(settings, screen, time_str, settings.title_font3, 
            color, settings.bg_color, pos_x, pos_y)

    
def draw_data(settings, screen, team_flights, enemy_flights, person, boxes):
    # get the height of the string image
    image = settings.title_font4.render("123456", True, settings.title_color, settings.bg_color)
    str_height = image.get_rect().height
    index = 0  # set index

    # team info
    for team in team_flights.sprites():

        pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
        pos_y = settings.screen_offset * 2.7 + index * (str_height + settings.screen_scale / 2)
        draw_string_framework(settings, screen, team.get_info_str()[0], settings.title_font4, 
                settings.title_color, settings.bg_color, pos_x, pos_y)
        index = index + 1

        pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
        pos_y = settings.screen_offset * 2.7 + index * (str_height + settings.screen_scale / 2)
        draw_string_framework(settings, screen, team.get_info_str()[1], settings.title_font4, 
                settings.title_color, settings.bg_color, pos_x, pos_y)
        index = index + 1

    # enemy info
    for enemy in enemy_flights.sprites():
        pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
        pos_y = settings.screen_offset * 2.7 + index * (str_height + settings.screen_scale / 2)
        draw_string_framework(settings, screen, enemy.get_info_str()[0], settings.title_font4, 
                settings.title_color, settings.bg_color, pos_x, pos_y)
        index = index + 1

        pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
        pos_y = settings.screen_offset * 2.7 + index * (str_height + settings.screen_scale / 2)
        draw_string_framework(settings, screen, enemy.get_info_str()[1], settings.title_font4, 
                settings.title_color, settings.bg_color, pos_x, pos_y)
        index = index + 1

    # person info
    pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
    pos_y = settings.screen_offset * 2.7 + index * (str_height + settings.screen_scale / 2)
    draw_string_framework(settings, screen, person.get_info_str()[0], settings.title_font4, 
            settings.title_color, settings.bg_color, pos_x, pos_y)
    index = index + 1

    pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
    pos_y = settings.screen_offset * 2.7 + index * (str_height + settings.screen_scale / 2)
    draw_string_framework(settings, screen, person.get_info_str()[1], settings.title_font4, 
            settings.title_color, settings.bg_color, pos_x, pos_y)
    index = index + 1


    # person status
    for enemy in enemy_flights.sprites():  # just to get a immune show time
        settings.show_immune_time = enemy.attack_limit_time - 0.1
        break
    person_str = "HP: " + str(person.get_hp_info()[0])
    pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
    pos_y = settings.screen_offset * 2.6 + 1.1 * settings.screen_scale * index
    draw_string_framework(settings, screen, person_str, settings.title_font2, 
            settings.title_color, settings.bg_color, pos_x, pos_y)
    index = index + 1

    # draw icons behind the string
    if person.healing_protect and settings.timer - person.get_hp_info()[1] < 5.0-0.1:  # immuned (+1HP)
        show_protected_icon = True
        settings.draw_person = True
    elif settings.timer - person.get_hp_info()[1] < settings.show_immune_time:  # immuned (-1HP)
        show_protected_icon = True
        settings.draw_person = not settings.draw_person
    elif boxes.is_in_protect_box(person.get_info()[0]):  # protected
        show_protected_icon = True
        settings.draw_person = True
    else:
        show_protected_icon = False
        settings.draw_person = True
    draw_icons(settings, screen, pos_x, pos_y - int(settings.screen_scale/3), show_protected_icon)


    # write AI status
    if settings.enemy_status == 0:
        status_str = "hovering"
    elif settings.enemy_status == 1:
        status_str = "moving straight"
    elif settings.enemy_status == 2:
        status_str = "moving circular"
    elif settings.enemy_status == 3:
        status_str = "approaching flights"
    elif settings.enemy_status == 4:
        status_str = "performing task (easy)"
    elif settings.enemy_status == 5:
        status_str = "performing task (medium)"
    elif settings.enemy_status == 6:
        status_str = "performing task (hard)"
    status_str = "AI status: " + status_str
    pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
    pos_y = settings.screen_offset * 3 + 1.1 * settings.screen_scale * index
    draw_string_framework(settings, screen, status_str, settings.title_font2, 
            settings.title_color, settings.bg_color, pos_x, pos_y)
    index = index + 1


    # write out of bound time
    out_of_bound_flag = False
    for team in team_flights.sprites():
        if team.get_info()[0][0] < 0.0 or team.get_info()[0][0] > 15.0 or team.get_info()[0][1] < 0.0 or team.get_info()[0][1] > 28.0:
            if not settings.out_of_bound_flag:  #check the last status of out of bound
                settings.out_times = 0
            out_of_bound_flag = True
            settings.out_times = settings.out_times + 1
            break

    settings.out_of_bound_flag = out_of_bound_flag
    if out_of_bound_flag:
        draw_out_of_bound_progress_bar(settings, screen)


    # mission status
    mission_color = settings.title_color
    if settings.failed:
        mission_str = "MISSION FAILED !"  # three failed reasons
        mission_color = settings.font_color_1and2
    elif not settings.get_key:
        mission_str = "Mission 1: Get the password"
        settings.complete_time = settings.timer
    elif not settings.all_open:
        mission_str = "Mission 2: Open the boxes"
        settings.complete_time = settings.timer
    elif not settings.complete:
        mission_str = "Mission 3: Go back"
        settings.complete_time = settings.timer
    else:
        mission_str = "MISSION COMPLETE !"
        mission_color = settings.font_color_1and2
    pos_x = 15 * settings.screen_scale + 2 * settings.screen_offset
    pos_y = settings.screen_offset * 3.4 + 1.1 * settings.screen_scale * index
    draw_string_framework(settings, screen, mission_str, settings.title_font2, 
            mission_color, settings.bg_color, pos_x, pos_y)
    index = index + 1


def draw_routes(settings, screen, team_flights, enemy_flights, person):
    n_points = settings.route_points
    for team, enemy in zip(team_flights.sprites(), enemy_flights.sprites()):
        routes = team.get_routes()
        for i in range(n_points):
            pos_x = int(routes[i][0] * settings.screen_scale + settings.screen_offset)
            pos_y = int(routes[i][1] * settings.screen_scale + settings.screen_offset)
            pygame.draw.circle(screen, settings.team_route_color, [pos_x, pos_y], 2)
        routes = enemy.get_routes()
        for i in range(n_points):
            pos_x = int(routes[i][0] * settings.screen_scale + settings.screen_offset)
            pos_y = int(routes[i][1] * settings.screen_scale + settings.screen_offset)
            pygame.draw.circle(screen, settings.enemy_route_color, [pos_x, pos_y], 2)

    routes = person.get_routes()
    for i in range(n_points):
        pos_x = int(routes[i][0] * settings.screen_scale + settings.screen_offset)
        pos_y = int(routes[i][1] * settings.screen_scale + settings.screen_offset)
        pygame.draw.circle(screen, settings.person_route_color, [pos_x, pos_y], 2)


def show_instructions(settings, screen):
    y_offset = - 200 - settings.screen_scale
    draw_string_framework(settings, screen, "Game Instructions", settings.title_font1, 
            settings.title_color, None, 0, y_offset, get_centered=True)

    pos_offset = -178
    instr_strings = ["This program simulates the scene of IARC Mission 8.",
                    "You can control the person and four team flights to complete the mission.", 
                    "Mission 1 : team flights fly to boxes to crack the QR code of the password.", 
                    "Mission 2 : the person must open all those boxes.", 
                    "Mission 3 : get back to the start line alive in 480 seconds.", 
                    "Your team flights should not get out of the bound for more than 10 seconds.", 
                    "You have 10 lives. Enemies will shoot you (-1 HP) if they get close to you.", 
                    "Each team flights can heal you once (+1 HP) if you get closer to them.", 
                    "The box located in the middle can protect you from attack.", 
                    "The flight command format examples are as follows.", 
                    "\"y 1\"  (go to Y-line 1m)    \"y 2 3\"  (go to Y-line 2m with interval 3m)", 
                    "\"f 6 2\"  (follow the leader flight with X-line 6m and 2m intervals)", 
                    "\"s 1\"  (hover at 1m ahead)", 
                    "Have fun!"]

    for index in range(14):
        y_offset = pos_offset
        pos_offset += 12 + settings.screen_scale
        draw_string_framework(settings, screen, instr_strings[index], settings.title_font2, 
                settings.title_color, settings.bg_color, 0, y_offset, get_centered=True)
        index = index + 1


def show_key_config(settings, screen):
    # show string
    y_offset = - 130 - 4 * settings.screen_scale
    draw_string_framework(settings, screen, "Keyboard configuration", settings.title_font1, 
            settings.title_color, None, 0, y_offset, get_centered=True)

    # show image
    image = pygame.image.load(r".\images\keyboard.jpg")
    rect = image.get_rect()
    image = pygame.transform.scale(image, (int(rect.width * settings.screen_scale / 22), int(rect.height * settings.screen_scale / 22)))
    rect = image.get_rect()
    rect.center = screen.get_rect().center
    rect.centery += settings.screen_scale * 2
    screen.blit(image, rect)


def show_ready_go(settings, screen):
    if settings.timer / settings.time_period <= 10:
        str0 = "Ready ? "
    else:
        str0 = "  Go !  "
    image = settings.title_font1.render(str0, True, settings.title_color, None)
    image_rect = image.get_rect()
    image_rect.center = screen.get_rect().center
    image_rect.x = 7.5 * settings.screen_scale + settings.screen_offset - image_rect.width / 2
    image_rect.y -= 10 + settings.screen_scale
    screen.blit(image, image_rect)


def show_pause(settings, screen):
    image = settings.title_font1.render("Paused", True, settings.title_color, None)
    image_rect = image.get_rect()
    image_rect.center = screen.get_rect().center
    image_rect.x = 7.5 * settings.screen_scale + settings.screen_offset - image_rect.width / 2
    image_rect.y -= 60 + settings.screen_scale
    screen.blit(image, image_rect)


def show_selecting_mode(settings, screen):
    y_offset = - 100 - 2 * settings.screen_scale
    draw_string_framework(settings, screen, "Select mode", settings.title_font1, 
            settings.title_color, None, 0, y_offset, get_centered=True)

    pos_offset = -20
    title_strings = ["Training mode", 
                    "Easy mode", 
                    "Medium mode", 
                    "Hard mode"]

    for index in range(4):
        if index == (settings.choose_index % 4):
            color = settings.choose_color
            button_chosen = True
        else:
            color = settings.title_color
            button_chosen = False
        draw_string_framework(settings, screen, title_strings[index], settings.title_font3, color, None, 
                0, pos_offset, get_centered=True, button_drawn=True, draw_button_chosen=button_chosen)
        pos_offset += 2 + 2 * settings.screen_scale


def show_scoreboard(settings, screen, sbd):
    y_offset = - 150 - 2 * settings.screen_scale
    draw_string_framework(settings, screen, "Scoreboard", settings.title_font1, 
            settings.title_color, None, 0, y_offset, get_centered=True)

    sbd_strings = sbd.get_hiscore_string()
    pos_offset = - 50 - 2 * settings.screen_scale
    for index in range(6):
        draw_string_framework(settings, screen, sbd_strings[index], settings.title_font3, 
                settings.title_color, settings.bg_color, 0, pos_offset, get_centered=True)
        pos_offset += 30 + settings.screen_scale

    if not settings.clean_request:
        clean_str = "Press R to reset scoreboard"
    else:
        clean_str = "Sure? (Press again to confirm)"
    draw_string_framework(settings, screen, clean_str, settings.title_font2, 
            settings.title_color, settings.bg_color, 0, pos_offset + 10, get_centered=True)


def show_loading_image(settings, screen):
    image = settings._loading_img
    rect = image.get_rect()
    rect.center = screen.get_rect().center
    rect.centery -= settings.screen_scale
    screen.blit(image, rect)


def draw_icons(settings, screen, x_offset, y_offset, show_protected_icon):
    # 3 icons are the same size
    rect = settings._img_mission1.get_rect()
    rect.y = y_offset

    rect.x = x_offset + 4 * settings.screen_scale
    if show_protected_icon:
        screen.blit(settings._img_protected, rect)

    rect.x = x_offset + 8.8 * settings.screen_scale
    if settings.get_key:
        screen.blit(settings._img_mission1, rect)
    else:
        screen.blit(settings._img_mission1_u, rect)

    rect.x = x_offset + 11 * settings.screen_scale
    if settings.all_open:
        screen.blit(settings._img_mission2, rect)
    else:
        screen.blit(settings._img_mission2_u, rect)
    
    rect.x = x_offset + 13.2 * settings.screen_scale
    if settings.complete:
        screen.blit(settings._img_mission3, rect)
    else:
        screen.blit(settings._img_mission3_u, rect)


def draw_out_of_bound_progress_bar(settings, screen):
    # background progress bar
    rect = settings._progbar1.get_rect()
    rect.centerx = 7.5 * settings.screen_scale + settings.screen_offset
    rect.centery = 15 * settings.screen_scale + settings.screen_offset
    screen.blit(settings._progbar1, rect)

    # running progress bar
    tmp_progbar = pygame.transform.scale(settings._progbar2, (int(12*min(settings.out_times*settings.time_period/10.0, 1.0)*0.975 * settings.screen_scale), int(0.6 * settings.screen_scale)))
    rect.x += rect.width * 0.015
    rect.y += rect.height * 0.13
    screen.blit(tmp_progbar, rect)

    # text
    text_image = settings.title_font2.render("Out of bound! Time:{0:.1f} s".format(settings.time_period * settings.out_times), True, settings.title_color, None)
    rect.centery -= 2 * settings.screen_scale
    screen.blit(text_image, rect)


def draw_button(settings, screen, content_rect, button_chosen):
    if button_chosen:
        button_img = settings._button1
    else:
        button_img = settings._button2
    button_img = pygame.transform.scale(button_img, (int(content_rect.width + settings.screen_scale*3), int(content_rect.height + settings.screen_scale/3)))
    rect = button_img.get_rect()
    rect.centerx = content_rect.centerx
    rect.centery = content_rect.centery
    screen.blit(button_img, rect)


def print_welcome():
    print("      ----------------------------------- ")
    print("     |       Explore Reactor Room        |")
    print("     |             WELCOME !             |")
    print("     |          Made by Shallwe          |")
    print("      ----------------------------------- ")


def print_info(team_flights, enemy_flights):
    for team in team_flights:
        team.print_info()
    for enemy in enemy_flights:
        enemy.print_info()

