import unittest
import pygame
from pygame.math import Vector2
from game import Game
from game_objects import Ball, Hexagon
from game_engine import PhysicsEngine, Renderer, GameState

class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()
        
    def tearDown(self):
        pygame.quit()
        
    def test_game_initialization(self):
        """测试游戏完整初始化"""
        self.assertIsNotNone(self.game.state)
        self.assertIsNotNone(self.game.physics)
        self.assertIsNotNone(self.game.renderer)
        self.assertIsNotNone(self.game.ball)
        self.assertIsNotNone(self.game.hexagon)
        
    def test_game_physics_integration(self):
        """测试物理系统集成"""
        initial_pos = self.game.ball.position.copy()
        initial_vel = self.game.ball.velocity.copy()
        
        # 模拟一帧物理更新
        self.game.physics.update(self.game.ball, self.game.hexagon)
        
        # 验证物理更新是否生效
        self.assertNotEqual(self.game.ball.position, initial_pos)
        self.assertNotEqual(self.game.ball.velocity, initial_vel)
        
    def test_game_state_transitions(self):
        """测试游戏状态转换"""
        # 测试暂停
        self.game.state.paused = True
        initial_pos = self.game.ball.position.copy()
        self.game.physics.state = self.game.state  # 同步状态
        self.game.physics.update(self.game.ball, self.game.hexagon)
        self.assertEqual(self.game.ball.position, initial_pos) 