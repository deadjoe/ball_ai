import unittest
from pygame.math import Vector2
from game_objects import GameObject, Ball, Hexagon
from game_engine import PhysicsEngine
from config import GAME_CONFIG
import pygame

class TestGameObjects(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.test_surface = pygame.Surface((800, 600))
        
    def tearDown(self):
        pygame.quit()
        
    def test_game_object_init(self):
        """测试GameObject基类初始化"""
        pos = Vector2(100, 100)
        obj = GameObject(pos)
        self.assertEqual(obj.position, pos)
        
    def test_ball_init(self):
        """测试Ball类初始化"""
        pos = Vector2(100, 100)
        radius = 10
        color = (255, 0, 0)
        ball = Ball(pos, radius, color)
        
        self.assertEqual(ball.position, pos)
        self.assertEqual(ball.radius, radius)
        self.assertEqual(ball.color, color)
        self.assertEqual(ball.velocity, Vector2(0, 0))
        
    def test_ball_update(self):
        """测试球体物理更新"""
        ball = Ball(Vector2(100, 100), 10, (255, 0, 0))
        gravity = Vector2(0, 0.5)
        friction = 0.99
        
        initial_pos = ball.position.copy()
        ball.update(gravity, friction)
        
        # 验证位置和速度的变化
        self.assertNotEqual(ball.position, initial_pos)
        self.assertEqual(ball.velocity.y, gravity.y * friction)
        
    def test_ball_velocity_limit(self):
        """测试球体速度限制"""
        ball = Ball(Vector2(100, 100), 10, (255, 0, 0))
        
        # 设置一个很大的速度
        ball.velocity = Vector2(100, 100)
        
        # 应用重力和摩擦力
        gravity = Vector2(0, 0.5)
        friction = 0.99
        
        # 创建物理引擎来处理速度限制
        physics = PhysicsEngine(gravity, friction, 0.8)
        physics.state.paused = False
        physics.update(ball, None)  # 不需要六边形进行速度限制测试
        
        # 验证速度被限制在合理范围内
        self.assertLessEqual(ball.velocity.length(), GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED'])
        
    def test_hexagon_init(self):
        """测试六边形初始化"""
        center = Vector2(400, 300)
        radius = 200
        color = (200, 200, 255)
        hex = Hexagon(center, radius, color)
        
        self.assertEqual(hex.position, center)
        self.assertEqual(hex.radius, radius)
        self.assertEqual(hex.color, color)
        self.assertEqual(hex.rotation, 0)
        self.assertEqual(hex.rotation_speed, GAME_CONFIG['HEXAGON']['INITIAL_SPEED'])
        
    def test_hexagon_update(self):
        """测试六边形旋转更新"""
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        acceleration = 0.1
        initial_rotation = hex.rotation
        
        hex.update(acceleration)
        
        # 验证旋转角度的变化
        self.assertNotEqual(hex.rotation, initial_rotation)
        
    def test_hexagon_rotation_direction(self):
        """测试六边形旋转方向"""
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        
        # 测试顺时针旋转
        test_speed = GAME_CONFIG['HEXAGON']['INITIAL_SPEED']
        hex.rotation_speed = test_speed
        initial_rotation = hex.rotation
        hex.update(GAME_CONFIG['HEXAGON']['ROTATION_ACCELERATION'])
        self.assertGreater(hex.rotation, initial_rotation)
        
        # 测试逆时针旋转
        hex.rotation_speed = -test_speed
        initial_rotation = hex.rotation
        hex.update(GAME_CONFIG['HEXAGON']['ROTATION_ACCELERATION'])
        self.assertLess(hex.rotation, initial_rotation)
        
    def test_hexagon_get_points(self):
        """测试六边形顶点计算"""
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        points = hex.get_points()
        
        # 验证返回的顶点数量
        self.assertEqual(len(points), 6)
        
    def test_hexagon_rotation_speed_change(self):
        """测试六边形旋转速度变化"""
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        initial_speed = hex.rotation_speed
        
        # 运行足够的帧数触发速度变化
        for _ in range(GAME_CONFIG['HEXAGON']['SPEED_CHANGE_INTERVAL'] + 1):
            hex.update(GAME_CONFIG['HEXAGON']['ROTATION_ACCELERATION'])
        
        # 验证速度在合理范围内
        self.assertGreaterEqual(hex.rotation_speed, 
                               GAME_CONFIG['HEXAGON']['MIN_ROTATION_SPEED'] * -1)
        self.assertLessEqual(hex.rotation_speed, 
                            GAME_CONFIG['HEXAGON']['MAX_ROTATION_SPEED']) 