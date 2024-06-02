class Settings:
    def __init__(self):
        # الإعدادات الخاصة بالشاشة
        self.screen_width = 1550
        self.screen_height = 880
        self.bg_color = (230, 230, 230)

        # إعدادات الروبوت
        self.robot_speed = 5

        # إعدادات الليزر
        self.laser_beam_speed = 30
        self.laser_beam_width = 4
        self.laser_beam_height = 20
        self.laser_beam_color = (255, 225, 225)
        self.laser_beams_allowed = 20

        # إعدادات الفيروسات
        self.base_virus_speed = 0.9
        self.max_viruses = 20
