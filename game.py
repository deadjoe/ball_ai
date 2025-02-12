import pygame
from pygame.math import Vector2
from config import GAME_CONFIG
from game_objects import Ball, Hexagon
from game_engine import GameState, PhysicsEngine, Renderer
import random

class Game:
    def __init__(self):
        pygame.init()
        self.state = GameState()
        self.renderer = Renderer(
            (GAME_CONFIG['WINDOW']['WIDTH'], GAME_CONFIG['WINDOW']['HEIGHT']),
            GAME_CONFIG['WINDOW']['RENDER_SCALE']
        )
        self.physics = PhysicsEngine(
            GAME_CONFIG['PHYSICS']['GRAVITY'],
            GAME_CONFIG['PHYSICS']['ELASTICITY'],
            GAME_CONFIG['PHYSICS']['FRICTION']
        )
        self.clock = pygame.time.Clock()
        
        # 初始化游戏对象
        self._init_game_objects()
        
    def _init_game_objects(self):
        window_config = GAME_CONFIG['WINDOW']
        self.ball = Ball(
            Vector2(window_config['WIDTH']//2, window_config['HEIGHT']//2 - 50),
            10,  # ball radius
            GAME_CONFIG['COLORS']['BALL_COLORS'][0]
        )
        self.hexagon = Hexagon(
            Vector2(window_config['WIDTH']//2, window_config['HEIGHT']//2),
            200,  # hex radius
            GAME_CONFIG['COLORS']['HEXAGON']
        )
        
    def run(self):
        while self.state.running:
            # 处理事件
            self.state.handle_events()
            
            # 只在非暂停状态更新物理
            if not self.state.paused:
                # 更新游戏状态
                self.hexagon.update(GAME_CONFIG['HEXAGON']['ROTATION_ACCELERATION'])
                collision = self.physics.update(self.ball, self.hexagon)
                
                # 处理碰撞后的颜色变化
                if collision:
                    self._handle_collision()
            
            # 渲染总是进行
            self.renderer.render([self.hexagon, self.ball])
            self.clock.tick(GAME_CONFIG['WINDOW']['FPS'])
            
        pygame.quit()
        
    def _handle_collision(self):
        """处理碰撞后的颜色变化"""
        current_color = self.ball.color
        available_colors = [c for c in GAME_CONFIG['COLORS']['BALL_COLORS'] 
                           if c != current_color]
        self.ball.color = random.choice(available_colors)

if __name__ == "__main__":
    game = Game()
    game.run() 