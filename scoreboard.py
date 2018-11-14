# -*- coding: utf-8 -*-
import pygame
import base64

class ScoreBoard():
    """ Show the infomation of scores """

    def __init__(self, file_name):
        """ Init the options """
        self._file_name = file_name
        self._stats = []
        self._hiscore_string = ["" for i in range(6)]
        self.read_hiscore()
        self.update_hiscore_string()


    def get_hiscore_string(self):
        return self._hiscore_string


    def read_hiscore(self):
        """ Read hiscore to the stats, .csv file required. If not found, then create. """
        try:
            table_data = []
            line_index = 0
            with open(self._file_name, "r", encoding = "utf-8-sig") as f:
                for line in f:
                    encoded_strings = (line.strip() + ',').split(',')[:5]  #加逗号防止寻索引溢出
                    for index in range(5):
                        encoded_strings[index] = str(base64.b64decode(encoded_strings[index].encode('utf-8')), 'utf-8')  # base64解密
                        encoded_strings[index] = float(encoded_strings[index][::2])  # 切片取出数据
                    table_data.append(encoded_strings)
                    line_index += 1
                    if line_index >= 3:
                        break
            self._stats = table_data  # stats 3x5
        except:  # Did not find the csv file, create it.
            # check if it is empty
            if self._stats == []:
                self.clean_hiscore()
                self.write_hiscore()
                self.read_hiscore()


    def write_hiscore(self):
        """ Write hiscore to the file, .csv file required. """
        with open(self._file_name, "w", encoding = "utf-8-sig") as f:
            for line_index in range(3):
                encoded_strings = ["" for i in range(5)]
                for index in range(5):
                    temp_string = str(self._stats[line_index][index])
                    for i in range(len(temp_string)):
                        encoded_strings[index] = encoded_strings[index] + temp_string[i] + temp_string[i]  # 存入数据预先处理
                    encoded_strings[index] = str(base64.b64encode(encoded_strings[index].encode('utf-8')), 'utf-8')  # base64加密
                out_str = "{0:s},{1:s},{2:s},{3:s},{4:s},".format(encoded_strings[0], encoded_strings[1], encoded_strings[2], encoded_strings[3], encoded_strings[4])
                print(out_str, file=f)


    def clean_hiscore(self):
        """ Clean hiscore """
        self._stats = [[479.95, 479.96, 479.97, 479.98, 479.99] for i in range(3)]
        self.update_hiscore_string()


    def set_new_hiscore(self, level, score):
        """ Store new hiscore """
        # level  0: easy  1: medium  2: hard
        if self._stats[level][4] > score:
            self._stats[level][4] = score
            for index in range(4, 0, -1):
                if self._stats[level][index] < self._stats[level][index-1]:
                    temp = self._stats[level][index-1]
                    self._stats[level][index-1] = self._stats[level][index]
                    self._stats[level][index] = temp
                else:
                    break
        self.update_hiscore_string()


    def update_hiscore_string(self):
        self._hiscore_string[0] = " Easy                    Medium                    Hard "
        for index in range(1, 6):
            self._hiscore_string[index] = "No.{0:d}: {1:.2f}s         No.{0:d}: {2:.2f}s         No.{0:d}: {3:.2f}s".format(index, self._stats[0][index-1], self._stats[1][index-1], self._stats[2][index-1])

