class GameStats():
    """有些信息"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        # 游戏初始为非活动状态
        self.game_active = False

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0 