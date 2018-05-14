
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    # 创建一个屏幕对象

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建play按钮
    play_button = Button(ai_settings, screen, "PLAY")
    # 创建统计游戏信息的实例、计分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建子弹编组
    bullets = Group()
    # 创建外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # main
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens)

        if stats.game_active:
            # 刷新飞船
            ship.update()
            # 刷新子弹
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb)
            # 刷新外星人
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets)

        # 刷新屏幕
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb)

run_game()
