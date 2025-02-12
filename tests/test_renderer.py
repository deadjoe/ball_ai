import unittest
import pygame
from game_engine import Renderer
from game_objects import Ball, Hexagon
from pygame.math import Vector2

class TestRenderer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.renderer = Renderer((800, 600), 2)
        
    def tearDown(self):
        pygame.quit()
        
    def test_renderer_init(self):
        """测试渲染器初始化"""
        self.assertEqual(self.renderer.screen_size, (800, 600))
        self.assertEqual(self.renderer.render_scale, 2)
        
    def test_clear(self):
        """测试清空屏幕"""
        self.renderer.clear()
        
        # 验证绘图表面是否被正确清空
        surface_empty = True
        for x in range(0, 10, 2):  # 采样检查部分像素
            for y in range(0, 10, 2):
                if self.renderer.drawing_surface.get_at((x, y))[3] != 0:
                    surface_empty = False
                    break
        self.assertTrue(surface_empty)
        
    def test_render_objects(self):
        """测试渲染游戏对象"""
        ball = Ball(Vector2(400, 300), 10, (255, 0, 0))
        hex = Hexagon(Vector2(400, 300), 200, (200, 200, 255))
        
        self.renderer.render([hex, ball])
        
        # 验证是否成功渲染（检查特定位置的像素）
        self.assertNotEqual(
            self.renderer.screen.get_at((400, 300))[:3], 
            (0, 0, 0)
        ) 

    def test_render_scale(self):
        """测试渲染缩放"""
        # 创建一个小尺寸的渲染器
        small_renderer = Renderer((400, 300), 1)
        ball = Ball(Vector2(200, 150), 10, (255, 0, 0))
        
        # 比较不同缩放下的渲染结果
        small_renderer.render([ball])
        self.renderer.render([ball])
        
        # 验证高分辨率渲染表面尺寸是否正确
        expected_size = (800 * 2, 600 * 2)  # RENDER_SCALE = 2
        self.assertEqual(self.renderer.drawing_surface.get_size(), expected_size)
        
    def test_render_effects(self):
        """测试特效渲染"""
        ball = Ball(Vector2(400, 300), 10, (255, 0, 0))
        
        # 清空屏幕
        self.renderer.clear()
        
        # 渲染球体
        self.renderer.render([ball])
        
        # 检查发光效果
        # 检查中心点及其周围的像素
        center_color = self.renderer.screen.get_at((400, 300))
        outer_color = self.renderer.screen.get_at((410, 300))
        
        # 中心应该比外围更亮
        self.assertGreater(sum(center_color[:3]), sum(outer_color[:3])) 