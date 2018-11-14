# -*- coding: utf-8 -*-
import sys
import pygame

def check_events(settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd):
    """ Monitor the events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cmd_thread.stop()
            sbd.write_hiscore()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, settings, person)

def update_screen(settings, screen, team_flights, enemy_flights, person, boxes, sbd):
    """ Update the images """
    # Rewhite screen
    screen.fill(settings.bg_color)

    if settings.run_active:
        # Write edges and boxes
        pygame.draw.rect(screen, settings.eg_color, [settings.screen_offset, settings.screen_offset, 15 * settings.screen_scale, 28 * settings.screen_scale], 4)
        boxes.drawing()

        draw_timer(settings, screen)
        draw_data(settings, screen, team_flights, enemy_flights, person, boxes)

        person.drawing()
        for team in team_flights.sprites():
            team.drawing()
            team.draw_heal_circle()
        for enemy in enemy_flights.sprites():
            enemy.drawing()
            enemy.draw_attack_circle()

        if settings.show_route:
            draw_routes(settings, screen, team_flights, enemy_flights, person)

        if settings.timer / settings.time_period <= 15:  # ready go
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

def check_keydown_events(event, settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd):
    if event.key == pygame.K_SPACE:
        if not settings.run_active:
            settings.run_active = True
            if not settings.have_run:
                settings.have_run = True
                cmd_thread.start()
        settings.selecting_mode = True  # start to select mode
    elif event.key == pygame.K_c:
        if settings.run_active:
            cmd_thread.input_request()
    elif event.key == pygame.K_r:
        if settings.show_hiscore:
            if not settings.clean_request:  # press r again to assure
                settings.clean_request = True
            else:  # pressed again
                settings.clean_request = False
                sbd.clean_hiscore()
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
        if settings.selecting_mode:  # select training mode
            settings.selecting_mode = False
            settings.game_mode = 0
            settings.reset_request = True
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 0
    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
        if settings.selecting_mode:  # select training mode
            settings.selecting_mode = False
            settings.game_mode = 1
            settings.reset_request = True
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 1
    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
        if settings.selecting_mode:  # select training mode
            settings.selecting_mode = False
            settings.game_mode = 2
            settings.reset_request = True
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 2
    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
        if settings.selecting_mode:  # select training mode
            settings.selecting_mode = False
            settings.game_mode = 3
            settings.reset_request = True
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 3
    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 4
    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 5
    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
        if settings.run_active and settings.game_mode == 0:
            settings.enemy_status = 6
    elif event.key == pygame.K_UP:
        if settings.run_active:
            person._moving_up = True
    elif event.key == pygame.K_DOWN:
        if settings.run_active:
            person._moving_down = True
    elif event.key == pygame.K_LEFT:
        if settings.run_active:
            person._moving_left = True
    elif event.key == pygame.K_RIGHT:
        if settings.run_active:
            person._moving_right = True
    elif event.key == pygame.K_ESCAPE:
        if settings.run_active:  # back to menu
            settings.run_active = False
            settings.selecting_mode = False
            person.reinit([0.8, 0.8], [7.5, 0.9])  # reinit person moving on the title
        else:  # quit the program
            cmd_thread.stop()
            sys.exit()


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


def draw_info(settings, screen):
    screen_rect = screen.get_rect()
    title_image = settings.bottom_font.render("Explore Reactor Room (Flight Route Simulator)   Author: Shallwe   Date:2018/10/10   Version: 1.0.0", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 5
    title_image_rect.y = screen_rect.height - title_image_rect.height - 5
    screen.blit(title_image, title_image_rect)

def draw_title(settings, screen):
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    title_image = settings.title_font1.render("Explore Reactor Room", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.y -= 100 + 4 * settings.screen_scale
    screen.blit(title_image, title_image_rect)

    pos_offset = 10 - settings.screen_scale
    title_strings = ["SPACE :  Start", 
                    "F1 :  Instructions", 
                    "F2 :  Keyboard configuration", 
                    "F3 :  Scoreboard", 
                    "ESC :  Exit"]

    for index in range(5):
        title_image = settings.title_font2.render(title_strings[index], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.center = rect.center
        title_image_rect.y += pos_offset
        pos_offset += 22 + settings.screen_scale
        screen.blit(title_image, title_image_rect)



def draw_timer(settings, screen):
    if not settings.complete and not settings.failed:
        time_str = "Simulation time: {0:.2f} s".format(settings.timer)
        color = settings.title_color
    else:
        time_str = "Simulation time: {0:.2f} s".format(settings.complete_time)
        color = settings.font_color_1
    screen_rect = screen.get_rect()
    title_image = settings.title_font3.render(time_str, True, color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 16 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset
    screen.blit(title_image, title_image_rect)

    
def draw_data(settings, screen, team_flights, enemy_flights, person, boxes):
    rect = pygame.Rect(50, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center
    index = 0

    # team info
    for team in team_flights.sprites():
        title_image = settings.title_font4.render(team.get_info_str()[0], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
        title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
        index = index + 1
        screen.blit(title_image, title_image_rect)

        title_image = settings.title_font4.render(team.get_info_str()[1], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
        title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
        index = index + 1
        screen.blit(title_image, title_image_rect)

    # enemy info
    for enemy in enemy_flights.sprites():
        title_image = settings.title_font4.render(enemy.get_info_str()[0], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
        title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
        index = index + 1
        screen.blit(title_image, title_image_rect)

        title_image = settings.title_font4.render(enemy.get_info_str()[1], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
        title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
        index = index + 1
        screen.blit(title_image, title_image_rect)

    # person info
    title_image = settings.title_font4.render(person.get_info_str()[0], True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
    index = index + 1
    screen.blit(title_image, title_image_rect)

    title_image = settings.title_font4.render(person.get_info_str()[1], True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
    index = index + 1
    screen.blit(title_image, title_image_rect)


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
    title_image = settings.title_font2.render(status_str, True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset * 3 + title_image_rect.y + 1.1 * settings.screen_scale * index
    index = index + 1
    screen.blit(title_image, title_image_rect)


    # person status
    for enemy in enemy_flights.sprites():  # just to get a immune show time
        immune_show_time = enemy.attack_limit_time - 0.1
        break
    person_str = "HP: " + str(person.get_hp_info()[0])
    if settings.timer - person.get_hp_info()[1] < immune_show_time:
        person_str = person_str + "   (immuned)"
    elif boxes.is_in_protect_box(person.get_info()[0]):
        person_str = person_str + "   (protected)"
    title_image = settings.title_font2.render(person_str, True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset * 3.2 + title_image_rect.y + 1.1 * settings.screen_scale * index
    index = index + 1
    screen.blit(title_image, title_image_rect)


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
        title_image = settings.title_font2.render("Out of bound time: {0:.2f} s".format(settings.time_period * settings.out_times), True, (255, 0, 0), settings.bg_color)
    else:
        title_image = settings.title_font2.render("Out of bound time: {0:.2f} s".format(settings.time_period * settings.out_times), True, settings.title_color, settings.bg_color)

    title_image_rect = title_image.get_rect()
    title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset * 3.4 + title_image_rect.y + 1.1 * settings.screen_scale * index
    index = index + 1
    screen.blit(title_image, title_image_rect)


    # mission status
    mission_color = settings.title_color
    if settings.failed:
        mission_str = "MISSION FAILED !"  # three failed reasons
        mission_color = settings.font_color_1
    elif not settings.get_key:
        mission_str = "Mission 1 : Get the password"
        settings.complete_time = settings.timer
    elif not settings.all_open:
        mission_str = "Mission 2 : Open the boxes"
        settings.complete_time = settings.timer
    elif not settings.complete:
        mission_str = "Mission 3 : Go back"
        settings.complete_time = settings.timer
    else:
        mission_str = "MISSION COMPLETE !"
        mission_color = settings.font_color_1
    title_image = settings.title_font2.render(mission_str, True, mission_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.x = 15 * settings.screen_scale + 2 * settings.screen_offset
    title_image_rect.y = settings.screen_offset * 3.6 + title_image_rect.y + 1.1 * settings.screen_scale * index
    index = index + 1
    screen.blit(title_image, title_image_rect)


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
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    title_image = settings.title_font1.render("Game Instructions", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.y -= 180 + 2 * settings.screen_scale
    screen.blit(title_image, title_image_rect)

    pos_offset = -170
    instr_strings = ["This program simulates the scene of IARC Mission 8.",
                    "You can control the person and four team flights to complete the mission.", 
                    "Mission 1 : team flights must fly to the boxes to get the password.", 
                    "Mission 2 : the person must open all those boxes.", 
                    "Mission 3 : get back to the start line alive in 480 seconds.", 
                    "Your team flights should not get out of the bound for more than 10 seconds.", 
                    "You have 10 lives. Enemies will shoot you (-1 HP) if they get close to you.", 
                    "Each team flights can heal you once (+1 HP) if you get closer to them.", 
                    "The box located in the middle can protect you from attack.", 
                    "The flight command format examples are as follows.", 
                    "\"y 1\"  (go to Y-line 1m)", 
                    "\"f 6 2\"  (follow the leader flight with X-line 6m and 2m intervals)", 
                    "Have fun!"]

    for index in range(13):
        title_image = settings.title_font2.render(instr_strings[index], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.center = rect.center
        title_image_rect.y += pos_offset
        pos_offset += 12 + settings.screen_scale
        screen.blit(title_image, title_image_rect)


def show_key_config(settings, screen):
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    title_image = settings.title_font1.render("Keyboard configuration", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.y -= 130 + 4 * settings.screen_scale
    screen.blit(title_image, title_image_rect)

    image = pygame.image.load(r".\images\keyboard.jpg")
    rect = image.get_rect()
    image = pygame.transform.scale(image, (int(rect.width * settings.screen_scale / 22), int(rect.height * settings.screen_scale / 22)))
    rect = image.get_rect()
    rect.center = screen_rect.center
    rect.centery += settings.screen_scale * 2
    screen.blit(image, rect)


def show_ready_go(settings, screen):
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    if settings.timer / settings.time_period <= 8:
        str0 = "Ready ? "
    else:
        str0 = "  Go !  "
    title_image = settings.title_font1.render(str0, True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.x = 7.5 * settings.screen_scale + settings.screen_offset - rect.width / 2
    title_image_rect.y -= 40 + settings.screen_scale
    screen.blit(title_image, title_image_rect)


def show_pause(settings, screen):
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    title_image = settings.title_font1.render("Paused", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.x = 7.5 * settings.screen_scale + settings.screen_offset - rect.width / 2
    title_image_rect.y -= 50 + settings.screen_scale
    screen.blit(title_image, title_image_rect)


def show_selecting_mode(settings, screen):
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    title_image = settings.title_font1.render("Select mode", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.y -= 100 + 2 * settings.screen_scale
    screen.blit(title_image, title_image_rect)

    pos_offset = -10
    title_strings = ["0 :  Training", 
                    "1 :  Easy mode", 
                    "2 :  Medium mode", 
                    "3 :  Hard mode"]

    for index in range(4):
        title_image = settings.title_font3.render(title_strings[index], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.center = rect.center
        title_image_rect.y += pos_offset
        pos_offset += 25 + settings.screen_scale
        screen.blit(title_image, title_image_rect)


def show_scoreboard(settings, screen, sbd):
    rect = pygame.Rect(0, 0, 180, 50)
    screen_rect = screen.get_rect()
    rect.center = screen_rect.center

    title_image = settings.title_font1.render("Scoreboard", True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.y -= 150 + 2 * settings.screen_scale
    screen.blit(title_image, title_image_rect)

    sbd_strings = sbd.get_hiscore_string()
    pos_offset = - 50 - 2 * settings.screen_scale

    for index in range(6):
        title_image = settings.title_font3.render(sbd_strings[index], True, settings.title_color, settings.bg_color)
        title_image_rect = title_image.get_rect()
        title_image_rect.center = rect.center
        title_image_rect.y += pos_offset
        pos_offset += 30 + settings.screen_scale
        screen.blit(title_image, title_image_rect)

    if not settings.clean_request:
        clean_str = "Press R to reset scoreboard"
    else:
        clean_str = "Sure? (Press again to confirm)"
    title_image = settings.title_font2.render(clean_str, True, settings.title_color, settings.bg_color)
    title_image_rect = title_image.get_rect()
    title_image_rect.center = rect.center
    title_image_rect.y += pos_offset
    pos_offset += 40 + settings.screen_scale
    screen.blit(title_image, title_image_rect)


def print_welcome():
    print(" ----------------------------------- ")
    print("|       Explore Reactor Room        |")
    print("|             WELCOME !             |")
    print("|          Made by Shallwe          |")
    print(" ----------------------------------- ")


def print_info(team_flights, enemy_flights):
    for team in team_flights:
        team.print_info()
    for enemy in enemy_flights:
        enemy.print_info()


