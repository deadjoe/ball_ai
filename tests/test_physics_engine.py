import unittest
from pygame.math import Vector2
from game_engine import PhysicsEngine
from game_objects import Ball, Hexagon
from config import GAME_CONFIG

class TestPhysicsEngine(unittest.TestCase):
    def setUp(self):
        self.physics = PhysicsEngine(
            Vector2(0, 0.5),  # gravity
            0.8,              # elasticity
            0.99              # friction
        )
        
    def test_physics_init(self):
        """测试物理引擎初始化"""
        self.assertEqual(self.physics.gravity, Vector2(0, 0.5))
        self.assertEqual(self.physics.elasticity, 0.8)
        self.assertEqual(self.physics.friction, 0.99)
        
    def test_centripetal_force(self):
        """测试向心力计算"""
        pos = Vector2(500, 300)  # 偏离中心的位置
        rotation_speed = 2.0
        
        force = self.physics._calculate_centripetal_force(pos, rotation_speed)
        
        # 验证向心力方向和大小
        self.assertIsInstance(force, Vector2)
        self.assertNotEqual(force.length(), 0)
        
    def test_collision_detection(self):
        """测试碰撞检测"""
        ball = Ball(Vector2(400, 100), 10, (255, 0, 0))
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        
        # 设置球体速度，使其向六边形移动
        ball.velocity = Vector2(0, 5)
        
        # 进行多次更新，直到发生碰撞
        collision_occurred = False
        for _ in range(50):  # 限制迭代次数
            collision = self.physics.update(ball, hex)
            if collision:
                collision_occurred = True
                break
                
        self.assertTrue(collision_occurred) 

    def test_collision_response(self):
        """测试碰撞响应"""
        ball = Ball(Vector2(400, 100), 10, (255, 0, 0))
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        
        # 设置球体向下运动
        ball.velocity = Vector2(0, 5)
        initial_velocity = ball.velocity.copy()
        
        # 运行直到发生碰撞
        collision_detected = False
        for _ in range(50):
            if self.physics.update(ball, hex):
                collision_detected = True
                break
                
        self.assertTrue(collision_detected)
        self.assertNotEqual(ball.velocity, initial_velocity)
        
    def test_edge_cases(self):
        """测试边界情况"""
        ball = Ball(Vector2(400, 100), 10, (255, 0, 0))
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        
        # 测试高速碰撞
        ball.velocity = Vector2(0, 50)  # 设置一个很大的速度
        self.physics.state.paused = False  # 确保物理引擎未暂停
        self.physics.update(ball, hex)
        self.assertLessEqual(
            ball.velocity.length(), 
            GAME_CONFIG['PHYSICS']['MAX_BALL_SPEED']
        )
        
    def test_physics_stability(self):
        """测试物理系统稳定性"""
        ball = Ball(Vector2(400, 100), 10, (255, 0, 0))
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        
        # 长时间运行测试
        for _ in range(100):
            self.physics.update(ball, hex)
            
            # 验证球体始终在合理范围内
            self.assertLess(abs(ball.position.x - 400), 300)
            self.assertLess(abs(ball.position.y - 300), 300) 