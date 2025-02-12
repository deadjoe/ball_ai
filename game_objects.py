from pygame.math import Vector2
from config import GAME_CONFIG
from typing import Tuple, Optional
import pygame

class GameObject:
    position: Vector2

    def __init__(self, position: Vector2) -> None:
        self.position = position
        
    def update(self) -> None:
        pass
        
    def draw(self, surface: pygame.Surface) -> None:
        pass

class Ball(GameObject):
    velocity: Vector2
    radius: float
    color: Tuple[int, int, int]

    def __init__(self, position: Vector2, radius: float, color: Tuple[int, int, int]) -> None:
        super().__init__(position)
        self.velocity = Vector2(0, 0)
        self.radius = radius
        self.color = color
        
    def update(self, gravity: Vector2, friction: float) -> None:
        self.velocity += gravity
        self.velocity *= friction
        
        # 使用配置的速度限制
        if self.velocity.length() > GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED']:
            self.velocity = (self.velocity.normalize() * 
                           GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED'])
            
        self.position += self.velocity
        
    def draw(self, surface: pygame.Surface) -> None:
        from utils import draw_glowing_circle
        draw_glowing_circle(surface, self.color, 
                          (int(self.position.x), int(self.position.y)), 
                          self.radius)

class Hexagon(GameObject):
    radius: float
    color: Tuple[int, int, int]
    rotation: float
    rotation_speed: float
    target_rotation_speed: float
    frame_count: int

    def __init__(self, center: Vector2, radius: float, color: Tuple[int, int, int]) -> None:
        super().__init__(center)
        self.radius = radius
        self.color = color
        self.rotation = 0
        self.rotation_speed = GAME_CONFIG['HEXAGON']['INITIAL_SPEED']
        self.target_rotation_speed = self.rotation_speed
        self.frame_count = 0
        
    def update(self, acceleration: float):
        # 更新帧计数
        self.frame_count += 1
        if self.frame_count >= GAME_CONFIG['HEXAGON']['SPEED_CHANGE_INTERVAL']:
            self.frame_count = 0
            self.target_rotation_speed = self._get_random_rotation_speed()
        
        # 平滑过渡到目标速度
        speed_diff = self.target_rotation_speed - self.rotation_speed
        self.rotation_speed += speed_diff * GAME_CONFIG['HEXAGON']['ROTATION_ACCELERATION']
        
        # 更新旋转角度
        self.rotation = (self.rotation + self.rotation_speed) % 360
        
    def _get_random_rotation_speed(self):
        """获取随机旋转速度和方向"""
        import random
        speed = random.uniform(
            GAME_CONFIG['HEXAGON']['MIN_ROTATION_SPEED'],
            GAME_CONFIG['HEXAGON']['MAX_ROTATION_SPEED']
        )
        direction = random.choice([-1, 1])
        return speed * direction
        
    def get_points(self):
        from utils import get_hex_points
        return get_hex_points(self.rotation)
        
    def draw(self, surface):
        from utils import draw_smooth_hexagon
        draw_smooth_hexagon(surface, self.color, self.get_points(), 4)  # HEX_BORDER_WIDTH = 4 