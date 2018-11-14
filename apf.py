#-*- coding: utf-8 -*-
import numpy as np
import math

def compute_angle(p_flight, p_all, p_goal, n_flights):
    # 本机位置，障碍位置，目标位置，障碍个数
    """ 计算引力和斥力用的角度，和目标之间的与X轴之间的夹角，统一规定角度为逆时针方向 """

    delta_x = p_goal[0] - p_flight[0]
    delta_y = p_goal[1] - p_flight[1]
    distance = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    if delta_y >= 0:  #引力角度计算
        angle_att = math.acos(delta_x / distance)
    else:
        angle_att = - math.acos(delta_x / distance)
    
    if n_flights == 0:
        return angle_att

    angle_rep = np.zeros(n_flights, dtype=float)

    for i in range(n_flights):  #对每个障碍进行斥力角度计算
        delta_x = p_all[i][0] - p_flight[0]
        delta_y = p_all[i][1] - p_flight[1]
        distance = np.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
        if distance < 0.02:  #是自己
            angle_rep[i] = 0
        else:
            if delta_y >= 0:
                angle_rep[i] = math.pi + math.acos(delta_x / distance)  #保存每个角度向量里面，表示与障碍的角度
            else:
                angle_rep[i] = math.pi - math.acos(delta_x / distance)
    angle_rep = angle_rep.tolist()

    return [angle_att, angle_rep]

#print(compute_angle([-8, -10], [[-9, -11], [-9, -10]], [0, 0], 2))



def compute_attract(settings, p_flight, p_goal, angle_att):
    """ 计算引力值的大小和分量 """

    k_att = settings.k_att
    d_at = math.sqrt( pow(p_flight[0] - p_goal[0], 2) + pow(p_flight[1] - p_goal[1], 2) );  #当前点和目标的距离
    f_attx = k_att * d_at * math.cos(angle_att)
    f_atty = k_att * d_at * math.sin(angle_att)

    return [f_attx, f_atty]



def compute_repulsion(settings, p_flight, p_all, p_goal, angle_rep, n_flights, p_all_direction):
    """ 计算斥力值的大小和分量 """

    k_rep = settings.k_rep
    d_o = settings.d_o
    d_dr = settings.d_dr
    adv_length = settings.adv_length
    k_mvrep = settings.k_mvrep
    angle_multi = settings.angle_multi

    f_rep = np.zeros(n_flights, dtype=float)
    p_all_adv = np.array(p_all, dtype=float)
    d_ao = np.zeros(n_flights, dtype=float)
    delta_angle = np.zeros(n_flights, dtype=float)

    p_all_adv[:,0] = p_all_adv[:,0] + adv_length * np.array(list(map(math.cos, p_all_direction)))  #斥力点中心超前处理
    p_all_adv[:,1] = p_all_adv[:,1] + adv_length * np.array(list(map(math.sin, p_all_direction)))
    d_at = np.sqrt( pow(p_flight[0] - p_goal[0], 2) + pow(p_flight[1] - p_goal[1], 2) )  #当前点和目标点的距离
    d_ao = np.sqrt( (p_all_adv[:,0] - p_flight[0])**2 + (p_all_adv[:,1] - p_flight[1])**2 )  #当前点和障碍的距离
    for i in range(n_flights):
        delta_angle[i] = abs( abs(angle_rep[i]) - abs(p_all_direction[i]) )  #障碍物运动方向与障碍物当前点连线的夹角

    for i in range(n_flights):
        if d_ao[i] < d_o and d_ao[i] > d_dr:  #判断距离是否在障碍影响范围内，不在范围内则f_rep默认为0。且判断是否为自己，是的话计算为0。
            f_rep[i] = k_rep * (1 / (d_ao[i] - d_dr) - 1 / (d_o - d_dr)) * (1 / ( pow(d_ao[i] - d_dr, 2) )) * pow(d_at, 2)
            if delta_angle[i] <= angle_multi:  #判断是否需要斥力倍增
                f_rep[i] = f_rep[i] + k_mvrep * f_rep[i] * (angle_multi - delta_angle[i]) / angle_multi  #迎面方向的斥力倍增

    f_repx = 0
    f_repy = 0
    for i in range(n_flights):
        f_repx = f_repx + f_rep[i] * math.cos(angle_rep[i])  #计算并叠加斥力的分量
        f_repy = f_repy + f_rep[i] * math.sin(angle_rep[i])

    return [f_repx, f_repy]

#print(compute_repulsion([0,1], [[0,5], [5,0], [0,-5], [-5,0]], [3,3], 1, [1,1,2,2], 4, 6, 0.15, [0,1,2,3], 0.05, 1, math.pi/3))


def compute_next_step(settings, p_flight, p_goal, p_all, n_flights, p_all_direction, is_team=True):
    """ 计算下一步位置 """
    if is_team:  #己方无人机位置计算
        [angle_att, angle_rep] = compute_angle(p_flight, p_all, p_goal, n_flights)
        [f_attx, f_atty] = compute_attract(settings, p_flight, p_goal, angle_att)
        [f_repx, f_repy] = compute_repulsion(settings, p_flight, p_all, p_goal, angle_rep, n_flights, p_all_direction)

        f_sum_x = f_attx + f_repx  #x方向的合力
        f_sum_y = f_atty + f_repy  #y方向的合力

    else:  #敌方无人机位置计算
        angle_att = compute_angle(p_flight, [], p_goal, 0)
        [f_sum_x, f_sum_y] = compute_attract(settings, p_flight, p_goal, angle_att)

    return [f_sum_x * settings.k_force, f_sum_y * settings.k_force]




