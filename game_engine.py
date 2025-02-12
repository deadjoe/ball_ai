import pygame
from pygame.math import Vector2
from config import GAME_CONFIG
from game_objects import Ball, Hexagon
import math
from utils import point_in_polygon, get_closest_point_on_line
from logger import GameLogger
from typing import Optional

logger = GameLogger.get_logger()

class GameState:
    def __init__(self):
        self.running = True
        self.paused = False
        self.frame_count = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

class PhysicsEngine:
    def __init__(self, gravity: Vector2, elasticity: float, friction: float):
        self.gravity = gravity
        self.elasticity = elasticity
        self.friction = friction
        self.state = GameState()  # 添加状态引用
        
    def update(self, ball: Ball, hexagon: Optional[Hexagon]) -> bool:
        try:
            if not ball:
                return False
                
            if not self.state.paused:
                # 速度限制
                if ball.velocity.length() > GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED']:
                    ball.velocity = (ball.velocity.normalize() * 
                                   GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED'])
                
                # 计算向心力
                centripetal_force = Vector2(0, 0)  # 默认无向心力
                if hexagon:  # 只在有六边形时计算向心力
                    centripetal_force = self._calculate_centripetal_force(
                        ball.position, 
                        hexagon.rotation_speed
                    )
                
                # 更新球的物理状态
                ball.update(self.gravity + centripetal_force, self.friction)
                
                # 再次检查速度限制（因为更新可能导致速度变化）
                if ball.velocity.length() > GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED']:
                    ball.velocity = (ball.velocity.normalize() * 
                                   GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED'])
                
                # 只在有六边形时进行碰撞检测
                if hexagon:
                    return self._handle_collision(ball, hexagon)
                
            return True
                
        except Exception as e:
            logger.error(f"Physics update error: {e}")
            return False
        
    def _calculate_centripetal_force(self, pos, rotation_speed):
        """计算向心力"""
        from config import GAME_CONFIG
        
        hex_center = Vector2(GAME_CONFIG['WINDOW']['WIDTH'] // 2, 
                            GAME_CONFIG['WINDOW']['HEIGHT'] // 2)
        r = pos - hex_center
        r_length = r.length()
        if r_length == 0:
            return Vector2(0, 0)
        
        angular_velocity = math.radians(abs(rotation_speed))
        centripetal_acc = (angular_velocity ** 2) * r_length
        return -r.normalize() * centripetal_acc * 0.1
        
    def _handle_collision(self, ball, hexagon):
        """处理碰撞"""
        from config import GAME_CONFIG
        
        next_pos = ball.position + ball.velocity
        hex_points = hexagon.get_points()
        
        if not point_in_polygon((next_pos.x, next_pos.y), hex_points):
            min_dist = float('inf')
            closest_point = None
            normal = None
            
            for i in range(len(hex_points)):
                line_start = Vector2(hex_points[i])
                line_end = Vector2(hex_points[(i + 1) % len(hex_points)])
                
                closest = get_closest_point_on_line((next_pos.x, next_pos.y), 
                                                  line_start, line_end)
                dist = (next_pos - closest).length()
                
                if dist < min_dist:
                    min_dist = dist
                    closest_point = closest
                    wall_vec = line_end - line_start
                    normal = Vector2(-wall_vec.y, wall_vec.x).normalize()

            if closest_point is not None:
                hex_center = Vector2(GAME_CONFIG['WINDOW']['WIDTH'] // 2, 
                                   GAME_CONFIG['WINDOW']['HEIGHT'] // 2)
                radius_vec = closest_point - hex_center
                
                if radius_vec.length() == 0:
                    return False
                    
                tangential_speed = (math.radians(abs(hexagon.rotation_speed)) * 
                                  radius_vec.length() * 
                                  (hexagon.rotation_speed / abs(hexagon.rotation_speed)))
                tangent = Vector2(-radius_vec.y, radius_vec.x).normalize()
                wall_vel = tangent * tangential_speed
                
                rel_vel = ball.velocity - wall_vel
                reflection = rel_vel.reflect(normal)
                ball.velocity = wall_vel + reflection * self.elasticity
                
                if ball.velocity.length() > GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED']:
                    ball.velocity = (ball.velocity.normalize() * 
                                   GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED'])
                
                collision_buffer = ball.radius + 4  # HEX_BORDER_WIDTH/2
                push_distance = collision_buffer - min_dist
                if push_distance > 0:
                    ball.position = next_pos + normal * push_distance
                    
                return True
                
        return False

class Renderer:
    def __init__(self, screen_size: tuple, render_scale: int):
        self.screen_size = screen_size
        self.render_scale = render_scale
        self.screen = pygame.display.set_mode(screen_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.drawing_surface = pygame.Surface(
            (screen_size[0] * render_scale, screen_size[1] * render_scale),
            pygame.SRCALPHA
        )
        
    def clear(self):
        self.drawing_surface.fill((0, 0, 0, 0))
        self.screen.fill(GAME_CONFIG['COLORS']['BACKGROUND'])
        
    def render(self, game_objects: list):
        self.clear()
        
        # 渲染所有游戏对象
        for obj in game_objects:
            obj.draw(self.drawing_surface)
            
        # 最终缩放和显示
        scaled_surface = pygame.transform.smoothscale(
            self.drawing_surface, 
            self.screen_size
        )
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip() 