# -*- coding: utf-8 -*-
import pygame
import random
import qrcode
from io import BytesIO

class Password():
    def __init__(self, settings, screen):
        """ Initialize information. """
        self.settings = settings
        self.screen = screen
        self._passwd = ""
        self._passwd_str = ""
        self._qrimg = None
        self._bound_status = True
        self._bound_change_time = 10

        self.text_image1 = self.settings.title_font2.render("The QR code was cracked.", True, settings.title_color, None)
        self.text_image1_rect = self.text_image1.get_rect()
        self.text_image2 = self.settings.title_font2.render("Scan it to get the password.", True, settings.title_color, None)
        self.text_image2_rect = self.text_image2.get_rect()


    def make_code(self, text):
        # version：是二维码的尺寸，数字大小决定二维码的密度
        # error_correction：是指误差
        # box_size：用来控制二维码的每个单元(box)格有多少像素点
        # border：用控制每条边有多少个单元格(默认值是4，这是规格的最小值)
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=2)
        # 添加数据
        qr.add_data(text)
        # 生成二维码
        qr.make(fit=True)
        qrimg = qr.make_image()

        imgstream = BytesIO()
        qrimg.save(imgstream)
        self._qrimg = pygame.image.load(BytesIO(imgstream.getvalue()))
        self._qrimg = pygame.transform.scale(self._qrimg, (int(3.5 * self.settings.screen_scale), int(3.5 * self.settings.screen_scale)))
        imgstream.close()

    def generate_passwd(self):
        self._passwd = ""
        for i in range(4):
            self._passwd = self._passwd + str(random.randint(0, 9))
        self._passwd_str = "Password: [ " + self._passwd + " ]"
        #print("Password: %s" % self._passwd)
        self.make_code(self._passwd_str)

    def check_passwd(self, passwd):
        if passwd == self._passwd:
            return True
        else:
            return False
    
    def draw_qrcode(self, pos):
        """ Draw the image in the specific position """
        # draw QR code
        self.rect = self._qrimg.get_rect()
        self.rect.centerx = pos[0] * self.settings.screen_scale + self.settings.screen_offset
        self.rect.centery = pos[1] * self.settings.screen_scale + self.settings.screen_offset
        self.screen.blit(self._qrimg, self.rect)

        # draw bound
        if self._bound_change_time > 0:
            self._bound_change_time -= 1
        else:
            self._bound_change_time = 20
            self._bound_status = not self._bound_status
        if self._bound_status:
            pygame.draw.rect(self.screen, self.settings.font_color_1, self.rect, 2)
        else:
            pygame.draw.rect(self.screen, self.settings.font_color_2, self.rect, 2)

        # draw text
        self.text_image1_rect.center = self.rect.center
        self.text_image1_rect.centery -= 2.5 * self.settings.screen_scale
        self.screen.blit(self.text_image1, self.text_image1_rect)

        self.text_image2_rect.center = self.rect.center
        self.text_image2_rect.centery += 2.5 * self.settings.screen_scale
        self.screen.blit(self.text_image2, self.text_image2_rect)

