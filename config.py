from pygame.math import Vector2
from game_types import GameConfig, WindowConfig, PhysicsConfig, ColorsConfig, HexagonConfig

GAME_CONFIG: GameConfig = {
    'WINDOW': {
        'WIDTH': 800,
        'HEIGHT': 600,
        'RENDER_SCALE': 2,
        'FPS': 60
    },
    'PHYSICS': {
        'GRAVITY': Vector2(0, 0.5),
        'ELASTICITY': 0.8,
        'FRICTION': 0.99,
        'MAX_BALL_SPEED': 20.0,
        'COLLISION_BUFFER': 14
    },
    'COLORS': {
        'BACKGROUND': (20, 31, 31),
        'HEXAGON': (200, 200, 255),
        'BALL_COLORS': [
            (255, 0, 0),      # 红色
            (0, 255, 0),      # 绿色
            (0, 0, 255),      # 蓝色
            (255, 255, 0),    # 黄色
            (255, 0, 255),    # 紫色
            (0, 255, 255),    # 青色
            (255, 128, 0),    # 橙色
            (255, 0, 128),    # 粉色
        ]
    },
    'HEXAGON': {
        'MIN_ROTATION_SPEED': 0.5,
        'MAX_ROTATION_SPEED': 5.0,
        'ROTATION_ACCELERATION': 0.1,
        'SPEED_CHANGE_INTERVAL': 60,
        'INITIAL_SPEED': 2.0
    }
} 