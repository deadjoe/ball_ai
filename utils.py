import math
import random
import pygame
from pygame.math import Vector2
from config import GAME_CONFIG
from functools import lru_cache
from typing import List, Tuple, Dict, Optional

def get_hex_points(angle):
    """获取旋转后的六边形顶点"""
    points = []
    hex_center = Vector2(GAME_CONFIG['WINDOW']['WIDTH'] // 2, 
                        GAME_CONFIG['WINDOW']['HEIGHT'] // 2)
    hex_radius = 200  # 保持原有的六边形半径
    
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = hex_center.x + hex_radius * math.cos(theta)
        y = hex_center.y + hex_radius * math.sin(theta)
        points.append((x, y))
    return points

def point_in_polygon(point, vertices):
    """检查点是否在多边形内部"""
    x, y = point
    n = len(vertices)
    inside = False
    p1x, p1y = vertices[0]
    for i in range(n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_closest_point_on_line(point, line_start, line_end):
    """获取点到线段的最近点"""
    line_vec = Vector2(line_end[0] - line_start[0], line_end[1] - line_start[1])
    point_vec = Vector2(point[0] - line_start[0], point[1] - line_start[1])
    line_length = line_vec.length()
    if line_length == 0:
        return Vector2(line_start)
    
    t = max(0, min(1, point_vec.dot(line_vec) / (line_length * line_length)))
    return Vector2(line_start[0] + t * line_vec.x, line_start[1] + t * line_vec.y)

def draw_smooth_hexagon(surface, color, points, width):
    """增强平滑效果的六边形绘制"""
    render_scale = GAME_CONFIG['WINDOW']['RENDER_SCALE']
    points = [(x * render_scale, y * render_scale) for x, y in points]
    width = width * render_scale
    
    # 绘制多层渐变边框
    for i in range(3):
        outer_width = width + (2-i) * render_scale
        alpha = 100 + i * 50
        pygame.draw.polygon(surface, (*color[:3], alpha), points, outer_width)
    
    # 主轮廓
    pygame.draw.polygon(surface, (*color[:3], 255), points, width)
    
    # 增强顶点平滑
    for point in points:
        for r in range(3):
            radius = (width // 2 - r) * render_scale
            alpha = 150 + r * 35
            pygame.draw.circle(surface, (*color[:3], alpha), 
                             (int(point[0]), int(point[1])), 
                             radius)

# 缓存发光球体的表面
class GlowSurfaceCache:
    _surfaces: Dict[Tuple[int, Tuple[int, int, int], int], pygame.Surface] = {}
    
    @classmethod
    def get_surface(cls, radius: int, color: Tuple[int, int, int], 
                   alpha: int) -> pygame.Surface:
        key = (radius, color, alpha)
        if key not in cls._surfaces:
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*color, alpha), 
                             (radius, radius), radius)
            cls._surfaces[key] = surface
        return cls._surfaces[key]

def draw_glowing_circle(surface: pygame.Surface, color: Tuple[int, int, int],
                       position: Tuple[int, int], radius: int) -> None:
    """优化的发光球体绘制"""
    render_scale = GAME_CONFIG['WINDOW']['RENDER_SCALE']
    position = (position[0] * render_scale, position[1] * render_scale)
    radius = radius * render_scale

    # 使用缓存的发光表面
    for i in range(8):
        alpha = 120 - i * 15
        radius_offset = i * 1.5
        glow_radius = int(radius + radius_offset * render_scale)
        glow_surface = GlowSurfaceCache.get_surface(glow_radius, color, alpha)
        surface.blit(glow_surface,
                    (position[0] - glow_radius, position[1] - glow_radius),
                    special_flags=pygame.BLEND_ALPHA_SDL2) 