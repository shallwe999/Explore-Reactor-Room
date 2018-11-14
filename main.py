# -*- coding: utf-8 -*-
# Explore Reactor Room (Flight Route Simulator)   Author: Shallwe   Date:2018/11/14   Version: 1.1.2
import math
import random
import threading
import time
from queue import Queue

import pygame
from pygame.sprite import Group

import apf
import tcmd
import terminal_func as tfunc
from boxes import Boxes
from enemyflight import EnemyFlight
from password import Password
from person import Person
from scoreboard import ScoreBoard
from settings import Settings
from teamflight import TeamFlight


def process(q, cmd_thread):
    # 初始化
    pygame.init()
    updated_frame = False  # update a frame
    settings = Settings("data\program_settings.json")
    screen = pygame.display.set_mode((32 * settings.screen_scale + 2 * settings.screen_offset, 28 * settings.screen_scale + 2 * settings.screen_offset))
    sbd = ScoreBoard("data\hiscore.csv")
    passwd = Password(settings, screen)
    tfunc.print_welcome()

    team_flights = Group()
    enemy_flights = Group()

    team1 = TeamFlight([0.8, 0.8], [3.5, 0.5], [1.5, 1.5], [1.5, 26], settings, screen)
    team1.print_info()
    team_flights.add(team1)
    team2 = TeamFlight([0.8, 0.8], [5.5, 0.5], [5.5, 1.5], [5.5, 26], settings, screen)
    team2.print_info()
    team_flights.add(team2)
    team3 = TeamFlight([0.8, 0.8], [9.5, 0.5], [9.5, 1.5], [9.5, 26], settings, screen)
    team3.print_info()
    team_flights.add(team3)
    team4 = TeamFlight([0.8, 0.8], [11.5, 0.5], [13.5, 1.5], [13.5, 26], settings, screen)
    team4.print_info()
    team_flights.add(team4)
    
    enemy1 = EnemyFlight([0.8, 0.8], [2, 10], settings, screen, rotate_angle=math.pi/100)
    enemy1.set_velocity([0, -0.11])
    enemy1.print_info()
    enemy_flights.add(enemy1)
    enemy2 = EnemyFlight([0.8, 0.8], [13, 10], settings, screen, rotate_angle=math.pi/100)
    enemy2.set_velocity([0, 0.11])
    enemy2.print_info()
    enemy_flights.add(enemy2)
    enemy3 = EnemyFlight([0.8, 0.8], [2, 18], settings, screen, rotate_angle=math.pi/100)
    enemy3.set_velocity([0, -0.11])
    enemy3.print_info()
    enemy_flights.add(enemy3)
    enemy4 = EnemyFlight([0.8, 0.8], [13, 18], settings, screen, rotate_angle=math.pi/100)
    enemy4.set_velocity([0, 0.11])
    enemy4.print_info()
    enemy_flights.add(enemy4)


    person = Person([0.8, 0.8], [7.5, 0.9], settings, screen)
    boxes = Boxes(settings, screen)

    pygame.display.set_caption("Explore Reactor Room")
    tfunc.update_screen(settings, screen, team_flights, enemy_flights, person, boxes, passwd, sbd)

    follow_status = False

    while True:
        start_time = time.time()
        period_timeout = True

        if settings.reset_request:  # game reset
            settings.reset_request = False
            settings.paused = False
            settings.init_game_args()
            if settings.game_mode != 0:  # set enemy mode according to game mode
                settings.enemy_status = settings.game_mode + 3
            person.reinit([0.8, 0.8], [7.5, 0.9])
            boxes.reinit()
            team1.reinit([0.8, 0.8], [3.5, 0.5], [1.5, 1.5], [1.5, 26])
            team2.reinit([0.8, 0.8], [5.5, 0.5], [5.5, 1.5], [5.5, 26])
            team3.reinit([0.8, 0.8], [9.5, 0.5], [9.5, 1.5], [9.5, 26])
            team4.reinit([0.8, 0.8], [11.5, 0.5], [13.5, 1.5], [13.5, 26])
            enemy1.reinit([0.8, 0.8], [2, 10], rotate_angle=math.pi/100)
            enemy1.set_velocity([0, -0.11])
            enemy2.reinit([0.8, 0.8], [13, 10], rotate_angle=math.pi/100)
            enemy2.set_velocity([0, 0.11])
            enemy3.reinit([0.8, 0.8], [2, 18], rotate_angle=math.pi/100)
            enemy3.set_velocity([0, -0.11])
            enemy4.reinit([0.8, 0.8], [13, 18], rotate_angle=math.pi/100)
            enemy4.set_velocity([0, 0.11])
            settings.enemy_status_changed = True
            passwd.generate_passwd()


        if settings.run_active and not settings.paused:
            # 帧开始，执行每一帧的预处理
            settings.timer = settings.timer + settings.time_period  # 计算时间
            if settings.clock_1 > 0:  # 计算clock1时间
                settings.clock_1 -= 1
            else:
                settings.clock_1 = 30
                settings.change_font_color()

            n_flights = len(team_flights.sprites()) + len(enemy_flights.sprites())  #包含自己一共的飞机数
            p_all = [[0, 0] for i in range(n_flights)]
            p_all_direction = [0 for i in range(n_flights)]
            index = 0
            for team in team_flights.sprites():
                p_all[index] = team.get_info()[0]
                p_all_direction[index] = 0
                index = index + 1
            for enemy in enemy_flights.sprites():
                p_all[index] = enemy.get_info()[0]
                p_all_direction[index] = enemy.get_direction()
                index = index + 1

            # 更新其它状态
            person.move()
            boxes.update_info(settings, person)
            settings.all_open = boxes.all_open()
            if settings.all_open and person.get_info()[0][1] <= 0.5 and not settings.failed:
                settings.complete = True
            elif (settings.timer > 480 or person.get_hp_info()[0] <= 0 or settings.out_times * settings.time_period >= 10.0) and not settings.complete:
                settings.failed = True
            if settings.complete and settings.game_mode != 0 and not settings.hiscore_recorded:
                settings.hiscore_recorded = True
                sbd.set_new_hiscore(settings.game_mode - 1, settings.complete_time)  # set hiscore
                sbd.write_hiscore()


            # 敌方无人机行动
            if settings.enemy_status == 0:  # 敌方无人机悬停
                for enemy in enemy_flights.sprites():
                    enemy.set_velocity([0, 0])
                    enemy.move()
                    if settings.enemy_status_changed:
                        enemy.set_attack_args(2.4, 5.0)
                    enemy.attack(person, boxes)

            elif settings.enemy_status == 1:  # 敌方无人机直线运动
                for enemy in enemy_flights.sprites():
                    enemy.move()
                    if settings.enemy_status_changed:
                        enemy.set_attack_args(2.4, 5.0)
                    enemy.attack(person, boxes)

            elif settings.enemy_status == 2:  # 敌方无人机圆周运动
                for enemy in enemy_flights.sprites():
                    enemy.move_circle()
                    if settings.enemy_status_changed:
                        enemy.set_attack_args(2.4, 5.0)
                    enemy.attack(person, boxes)

            elif settings.enemy_status == 3:  # 敌方无人机逼近己方无人机
                for enemy, team in zip(enemy_flights.sprites(), team_flights.sprites()):
                    team_p_flight = team.get_info()[0]
                    enemy_p_flight = enemy.get_info()[0]
                    team_p_flight = [team_p_flight[0] + random.random()*4 - 2, team_p_flight[1] + 1.5 + random.random()*4 - 2]
                    [vx, vy] = apf.compute_next_step(settings, enemy_p_flight, team_p_flight, [], 0, [], is_team=False)
                    enemy.set_max_v(settings.enemy_mission_args[1][3])  # medium velocity
                    enemy.set_velocity([vx/1.5, vy/1.5])
                    enemy.move()
                    if settings.enemy_status_changed:
                        enemy.set_attack_args(2.4, 5.0)
                    enemy.attack(person, boxes)

            elif settings.enemy_status >= 4 and settings.enemy_status <= 6:  # 执行任务状态
                difficulty = settings.enemy_status - 4  # 0:简单  1:中等  2:困难
                enemy_mission_args = settings.enemy_mission_args[difficulty]
                is_first = True
                flight_index = 0
                p_offset = [[0, enemy_mission_args[6]], [enemy_mission_args[6], 0], [-enemy_mission_args[6], 0], [0, -enemy_mission_args[6]]]
                if boxes.is_in_protect_box(person.get_info()[0]):  # 在保护区域内，一架逼近人，三架逼近己方无人机
                    for enemy, team in zip(enemy_flights.sprites(), team_flights.sprites()):
                        if is_first:
                            is_first = False
                            person_p_flight = person.get_info()[0]
                            enemy_p_flight = enemy.get_info()[0]
                            person_p_flight = [person_p_flight[0] + random.random()*4 - 2, person_p_flight[1] + 2 + random.random()*2*enemy_mission_args[1] - enemy_mission_args[1]]
                            [vx, vy] = apf.compute_next_step(settings, enemy_p_flight, person_p_flight, [], 0, [], is_team=False)
                        else:
                            team_p_flight = team.get_info()[0]
                            enemy_p_flight = enemy.get_info()[0]
                            team_p_flight = [team_p_flight[0] + random.random()*4 - 2, team_p_flight[1] + 1.5 + random.random()*2*enemy_mission_args[1] - enemy_mission_args[1]]
                            [vx, vy] = apf.compute_next_step(settings, enemy_p_flight, team_p_flight, [], 0, [], is_team=False)
                        enemy.set_max_v(enemy_mission_args[3])
                        enemy.set_velocity([vx * enemy_mission_args[0], vy * enemy_mission_args[0]])
                        enemy.move()
                        if settings.enemy_status_changed:
                            enemy.set_attack_args(enemy_mission_args[4], enemy_mission_args[5])
                        enemy.attack(person, boxes)
                else:  # 在保护区域外，四架逼近人
                    for enemy, team in zip(enemy_flights.sprites(), team_flights.sprites()):
                        person_p_flight = person.get_info()[0]
                        enemy_p_flight = enemy.get_info()[0]
                        person_p_flight = [person_p_flight[0] + p_offset[flight_index][0] + random.random()*2*enemy_mission_args[2] - enemy_mission_args[2], person_p_flight[1] + p_offset[flight_index][1] + random.random()*2*enemy_mission_args[2] - enemy_mission_args[2]]
                        flight_index = flight_index + 1
                        [vx, vy] = apf.compute_next_step(settings, enemy_p_flight, person_p_flight, [], 0, [], is_team=False)
                        enemy.set_max_v(enemy_mission_args[3])
                        enemy.set_velocity([vx * enemy_mission_args[0], vy * enemy_mission_args[0]])
                        enemy.move()
                        if settings.enemy_status_changed:
                            enemy.set_attack_args(enemy_mission_args[4], enemy_mission_args[5])
                        enemy.attack(person, boxes)

            settings.enemy_status_changed = False


            # 己方无人机行动
            all_reach_final_goal = True  # 假定都达到了密码箱位置(final pos)
            if follow_status:
                # 跟随主飞机模式
                is_first = True
                index = 0
                for team in team_flights.sprites():
                    if not team.reach_final_goal():
                        all_reach_final_goal = False

                    if is_first:
                        is_first = False
                        p_flight = team.get_info()[0]
                        if p_flight[1] >= 26.1:  #达成目标，恢复原队形
                            follow_status = False
                            p_goal = [1.5, 26]
                            team.set_goal(p_goal)
                            continue
                        p_leader = p_flight
                        p_goal = [tcmd_temp_line, 27.1]
                        team.set_goal(p_goal)
                    else:
                        if not follow_status:  #恢复现场
                            p_goal[0] = p_goal[0] + 4
                            team.set_goal(p_goal)
                            continue
                        p_flight = team.get_info()[0]
                        team.set_goal([p_leader[0], p_leader[1] - index])
                        index = index + tcmd_follow_length
                        p_goal = team.get_goal()
                    
                    [vx, vy] = apf.compute_next_step(settings, p_flight, p_goal, p_all, n_flights, p_all_direction, is_team=True)
                    [vx, vy] = [vx + random.random() * 0.02 - 0.01, vy + random.random() * 0.01 - 0.005]  # 速度扰动
                    team.set_velocity([vx, vy])
                    team.move()
                    team.heal(person, boxes)

            else:
                # 独立模式
                for team in team_flights.sprites():
                    if not team.reach_final_goal():
                        all_reach_final_goal = False

                    p_flight = team.get_info()[0]
                    p_goal = team.get_goal()
                    [vx, vy] = apf.compute_next_step(settings, p_flight, p_goal, p_all, n_flights, p_all_direction, is_team=True)
                    [vx, vy] = [vx + random.random() * 0.02 - 0.01, vy + random.random() * 0.01 - 0.005]  # 速度扰动
                    team.set_velocity([vx, vy])
                    team.move()
                    team.heal(person, boxes)

            if not settings.crack_qrcode:
                boxes.crack(all_reach_final_goal)  # 全部到达目的地，破译密码


            # 获取终端指令
            if not q.empty():
                try:
                    [cmd_content, cmd_args] = q.get().split(' ', 1)
                    if cmd_content == "thenextcontentisthepassword":
                        # 玩家输入密码
                        try:
                            tcmd_passwd = cmd_args
                            if passwd.check_passwd(tcmd_passwd):
                                print("[Boxes] Password correct.")
                                settings.get_key = True
                            else:
                                print("[Boxes] Password error, try again.")
                        except:
                            print("[Boxes] Password input error.")

                    elif cmd_content == "y":
                        # 更改己方飞机目标点（Y轴平齐）策略
                        try:
                            [cmd_arg_1, cmd_arg_2] = cmd_args.split(' ')
                            new_goal = float(cmd_arg_1)
                            interval = float(cmd_arg_2)
                        except:
                            new_goal = float(cmd_args)
                            interval = 4.0
                        x_offset = 7.5 - interval * 1.5
                        print("[Team] Move team flights to Y-line %.3f m with interval %.3f m ." % (new_goal, interval))
                        for team in team_flights.sprites():
                            team.set_goal([x_offset, new_goal])
                            x_offset += interval
                    elif cmd_content == "f":
                        # 跟随主飞机运动策略
                        [cmd_arg_1, cmd_arg_2] = cmd_args.split(' ')
                        tcmd_temp_line = float(cmd_arg_1)
                        tcmd_follow_length = float(cmd_arg_2)
                        print("[Team] Follow the leader team flight with X-line %.3f m and interval %.3f m ." % (tcmd_temp_line, tcmd_follow_length))
                        follow_status = True
                    elif cmd_content == "s":
                        # 即刻在前方悬停策略
                        follow_status = False
                        ahead_length = float(cmd_args)
                        print("[Team] Hover at %.3f m ahead ." % (ahead_length))
                        for team in team_flights.sprites():
                            temp_goal = team.get_info()[0]
                            team.set_goal([temp_goal[0], temp_goal[1] + ahead_length])
                    else:
                        print("[Team] Unknown command.")
                except:
                    print("[Team] Command error.")

            if settings.crack_qrcode and not settings.get_key:
                cmd_thread.input_passwd_request()  # input the password in tcmd


        tfunc.update_screen(settings, screen, team_flights, enemy_flights, person, boxes, passwd, sbd)
        
        # Watch update frame time (for test)
        #if updated_frame:
        #    updated_frame = False
        #    print("Update time: %.3fs" % (time.time() - start_time))


        # 等待更新时间
        while period_timeout:
            tfunc.check_events(settings, screen, cmd_thread, team_flights, enemy_flights, person, sbd)
            if time.time() - start_time >= 0.04:
                period_timeout = False
                updated_frame = True



def main():
    q = Queue()
    cmd_thread = tcmd.MyThread(q)
    process(q, cmd_thread)


if __name__ == '__main__':
    main()
