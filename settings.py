
class Settings():
    """存储所有设置的类"""

    def __init__(self):
        """初始化静态设置"""
        # 屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # 飞船的设置
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10
        # 外星人下移设置
        self.fleet_drop_speed = 5

        # 游戏节奏
        self.speedup_scale = 1.1
        # 得分增加比例
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """动态设置"""
        # 飞船移动速度
        self.ship_speed_factor = 1.5
        # 子弹速度
        self.bullet_speed_factor = 1
        # 外星人移动速度、移动方向
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        # 得分
        self.alien_points = 50

    def increase_speed(self):
        """提速"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        # 得分增加
        self.alien_points = int(self.alien_points * self.score_scale)