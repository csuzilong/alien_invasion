import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def fire_bullet(ai_settings, screen, ship, bullets):
    # 空格时创建子弹，并加入编组中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """key down"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """key up"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship):
    """响应play按钮"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 在点击按钮且游戏状态为非活动时响应
    if button_clicked and not stats.game_active:
        # 重新开始 重置动态设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏信息
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建新外星人和飞船
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb):
    """更新屏幕"""
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 飞船
    ship.blitme()
    # 外星人
    aliens.draw(screen)
    # 计分牌
    sb.show_score()

    # 绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 刷新屏幕
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    # 刷新子弹
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship, stats, sb)


def check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship, stats, sb):
    """检查子弹和外星人碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    # 检查外星人是否全部消失
    if len(aliens) == 0:
        bullets.empty()
        # 提速
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)


def get_number_aliens_x(ai_settings, alien_width):
    """计算一行外星人的数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算外星人行数"""
    available_space_y = ai_settings.screen_height - 3*alien_height - ship_height
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)

    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2*alien_width*alien_number

    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2*alien_height*row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    """创建外星人"""

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens, ship, stats, screen, bullets):
    """判断外星人是否到边缘，是则改变方向"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 外星人与飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, aliens, ship, stats, screen, bullets)

    # 外星人到达屏幕底端
    check_aliens_bottom(ai_settings, aliens, ship, stats, screen, bullets)


def check_aliens_bottom(ai_settings, aliens, ship, stats, screen, bullets):
    """响应外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, aliens, ship, stats, screen, bullets)
            break


def ship_hit(ai_settings, aliens, ship, stats, screen, bullets):
    """响应外星人与飞船碰撞"""
    if stats.ship_left > 0:
        # 飞船减1
        stats.ship_left -= 1
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 创建新外星人和飞船
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        # 暂停0.5s
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
