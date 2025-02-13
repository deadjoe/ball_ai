# 导入必要的模块
import pygame
import math
import random
from pygame.math import Vector2

pygame.init()

# 设置窗口和渲染参数
RENDER_SCALE = 2  # 渲染精度倍数，用于实现抗锯齿效果：将所有图形放大2倍绘制后再缩小，从而获得更平滑的边缘
WIDTH = 800        # 窗口宽度（像素）
HEIGHT = 600      # 窗口高度（像素）
# 使用硬件加速表面(HWSURFACE)和双缓冲(DOUBLEBUF)来优化性能
FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS)
pygame.display.set_caption("动态旋转六边形与弹跳球")

# 创建一个高分辨率的绘图表面用于抗锯齿
# 将所有图形在这个表面上以2倍大小绘制，最后缩放回原始大小，实现抗锯齿效果
# SRCALPHA 标志支持 Alpha 通道，实现透明效果
drawing_surface = pygame.Surface((WIDTH * RENDER_SCALE, HEIGHT * RENDER_SCALE), pygame.SRCALPHA)

# 颜色定义，使用RGB格式，范围0-255
WHITE = (255, 255, 255)
BLACK = (20, 31, 31)  # 深蓝灰色背景
BALL_COLORS = [
   (255, 0, 0),      # 红色
   (0, 255, 0),      # 绿色
   (0, 0, 255),      # 蓝色
   (255, 255, 0),    # 黄色
   (255, 0, 255),    # 紫色
   (0, 255, 255),    # 青色
   (255, 128, 0),    # 橙色
   (255, 0, 128),    # 粉色
]
current_ball_color = BALL_COLORS[0]  # 初始球体颜色设为第一个颜色
HEX_COLOR = (200, 200, 255)  # 淡蓝色，用于六边形

# 六边形参数
HEX_RADIUS = 200    # 六边形外接圆半径（像素）
HEX_CENTER = Vector2(WIDTH // 2, HEIGHT // 2)  # 六边形中心位置
MIN_ROTATION_SPEED = 0.5   # 最小旋转速度（度/帧）
MAX_ROTATION_SPEED = 5     # 最大旋转速度（度/帧）
ROTATION_ACCELERATION = 0.1 # 旋转加速度：速度变化的平滑系数
current_rotation_speed = 2.0  # 初始旋转速度
target_rotation_speed = 2.0   # 目标旋转速度
SPEED_CHANGE_INTERVAL = 60    # 改变旋转速度的帧数间隔
HEX_BORDER_WIDTH = 4          # 六边形边框宽度（像素）
rotation_direction = 1         # 旋转方向：1表示顺时针，-1表示逆时针

# 球参数
BALL_RADIUS = 10  # 球体半径（像素）
ball_pos = Vector2(HEX_CENTER.x, HEX_CENTER.y - 50)  # 球体初始位置：在六边形顶部中心
ball_vel = Vector2(0, 0)  # 球体初始速度：静止

# 物理参数设置
GRAVITY = Vector2(0, 0.5)  # 重力加速度向量
ELASTICITY = 0.8  # 碰撞弹性系数：0表示完全非弹性碰撞，1表示完全弹性碰撞
FRICTION = 0.99  # 摩擦系数：每帧速度衰减比例
COLLISION_BUFFER = BALL_RADIUS * 2 + HEX_BORDER_WIDTH  # 碰撞检测的缓冲距离，防止穿透
MAX_BALL_SPEED = 30.0  # 球体最大速度限制，防止速度过大导致穿透或不稳定

def reset_ball():
    """重置球的位置和速度
    
    将球重置到六边形顶部中心位置，速度归零
    
    Returns:
        tuple: (初始位置向量, 初始速度向量)
    """
    return (Vector2(HEX_CENTER.x, HEX_CENTER.y - 50),  # 位置
            Vector2(0, 0))  # 速度

def check_ball_state(pos, vel):
    """检查球的状态，如果异常则重置
    
    检查球的位置和速度是否在合理范围内，防止数值不稳定
    
    Args:
        pos: 球体位置向量
        vel: 球体速度向量
        
    Returns:
        tuple: (修正后的位置, 修正后的速度)
    """
    # 检查位置是否在合理范围内
    if (abs(pos.x - HEX_CENTER.x) > WIDTH/2 or 
        abs(pos.y - HEX_CENTER.y) > HEIGHT/2 or
        math.isnan(pos.x) or math.isnan(pos.y)):
        return reset_ball()
    
    # 检查速度是否在合理范围内
    if vel.length() > MAX_BALL_SPEED:
        vel = vel.normalize() * MAX_BALL_SPEED
    
    return pos, vel

def get_hex_points(angle):
    """获取旋转后的六边形顶点
    
    根据当前旋转角度计算六边形的六个顶点坐标
    
    Args:
        angle: 当前旋转角度（度）
        
    Returns:
        list: 包含六个顶点坐标的列表，每个坐标为(x, y)元组
    """
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = HEX_CENTER.x + HEX_RADIUS * math.cos(theta)
        y = HEX_CENTER.y + HEX_RADIUS * math.sin(theta)
        points.append((x, y))
    return points

def point_in_polygon(point, vertices):
    """检查点是否在多边形内部
    
    使用射线法判断点是否在多边形内部
    
    Args:
        point: 待检查的点坐标(x, y)
        vertices: 多边形顶点列表
        
    Returns:
        bool: True表示点在多边形内部，False表示在外部
    """
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
    """获取点到线段的最近点
    
    使用向量投影计算点到线段的最近点
    
    Args:
        point: 待计算的点坐标(x, y)
        line_start: 线段起点坐标(x, y)
        line_end: 线段终点坐标(x, y)
        
    Returns:
        Vector2: 最近点坐标
    """
    line_vec = Vector2(line_end[0] - line_start[0], line_end[1] - line_start[1])
    point_vec = Vector2(point[0] - line_start[0], point[1] - line_start[1])
    line_length = line_vec.length()
    if line_length == 0:
        return Vector2(line_start)
    
    t = max(0, min(1, point_vec.dot(line_vec) / (line_length * line_length)))
    return Vector2(line_start[0] + t * line_vec.x, line_start[1] + t * line_vec.y)

def calculate_centripetal_force(pos, rotation_speed):
    """计算向心力
    
    根据球体位置和六边形旋转速度计算向心力
    
    Args:
        pos: 球体当前位置向量
        rotation_speed: 六边形当前旋转速度
        
    Returns:
        Vector2: 向心力向量，大小与旋转速度的平方和到中心距离成正比
    """
    r = pos - HEX_CENTER
    r_length = r.length()
    if r_length == 0:
        return Vector2(0, 0)
    
    # 将角速度从度/帧转换为弧度/帧
    angular_velocity = math.radians(abs(rotation_speed))
    # 计算向心加速度：v²/r = ω²r
    centripetal_acc = (angular_velocity ** 2) * r_length
    # 返回向中心的力，乘以0.2作为力的缩放因子
    return -r.normalize() * centripetal_acc * 0.2

def is_ball_too_close_to_edge(ball_pos, hex_points):
    """检查球是否太靠近边缘
    
    检查球体是否距离六边形边缘过近
    
    Args:
        ball_pos: 球体当前位置向量
        hex_points: 六边形顶点列表
        
    Returns:
        bool: True表示球体太靠近边缘，False表示正常
    """
    for i in range(len(hex_points)):
        line_start = Vector2(hex_points[i])
        line_end = Vector2(hex_points[(i + 1) % len(hex_points)])
        
        closest = get_closest_point_on_line((ball_pos.x, ball_pos.y), line_start, line_end)
        dist = (ball_pos - closest).length()
        
        if dist < COLLISION_BUFFER:
            return True
    return False

def handle_collision(ball_pos, ball_vel, hex_points, rotation_speed):
    """改进的碰撞处理，考虑旋转方向和速度
    
    处理球体与六边形边缘的碰撞
    
    Args:
        ball_pos: 球体位置向量
        ball_vel: 球体速度向量
        hex_points: 六边形顶点列表
        rotation_speed: 六边形当前旋转速度
        
    Returns:
        tuple: (新位置, 新速度, 是否发生碰撞)
    """
    collision_occurred = False
   
    # 添加安全检查
    if (math.isnan(ball_pos.x) or math.isnan(ball_pos.y) or
        math.isnan(ball_vel.x) or math.isnan(ball_vel.y)):
        return reset_ball()[0], reset_ball()[1], False
   
    if not point_in_polygon((ball_pos.x, ball_pos.y), hex_points):
        min_dist = float('inf')
        closest_point = None
        normal = None
        
        for i in range(len(hex_points)):
            line_start = Vector2(hex_points[i])
            line_end = Vector2(hex_points[(i + 1) % len(hex_points)])
            
            closest = get_closest_point_on_line((ball_pos.x, ball_pos.y), line_start, line_end)
            dist = (ball_pos - closest).length()
            
            if dist < min_dist:
                min_dist = dist
                closest_point = closest
                wall_vec = line_end - line_start
                normal = Vector2(-wall_vec.y, wall_vec.x).normalize()

        if closest_point is not None:
            collision_occurred = True
            radius_vec = closest_point - HEX_CENTER
            # 添加安全检查
            if radius_vec.length() == 0:
                return reset_ball()[0], reset_ball()[1], False
                
            tangential_speed = math.radians(abs(rotation_speed)) * radius_vec.length() * (rotation_speed / abs(rotation_speed))
            tangent = Vector2(-radius_vec.y, radius_vec.x).normalize()
            wall_vel = tangent * tangential_speed
            
            rel_vel = ball_vel - wall_vel
            reflection = rel_vel.reflect(normal)
            ball_vel = wall_vel + reflection * ELASTICITY
            
            # 限制最大速度
            if ball_vel.length() > MAX_BALL_SPEED:
                ball_vel = ball_vel.normalize() * MAX_BALL_SPEED
            
            push_distance = COLLISION_BUFFER - min_dist
            if push_distance > 0:
                ball_pos = ball_pos + normal * push_distance

    return ball_pos, ball_vel, collision_occurred

def get_random_ball_color():
    """获取一个随机的球颜色，不同于当前颜色
    
    从预定义的颜色列表中随机选择一个颜色
    
    Returns:
        tuple: 随机颜色值
    """
    global current_ball_color
    available_colors = [c for c in BALL_COLORS if c != current_ball_color]
    return random.choice(available_colors)

def get_random_rotation_speed():
    """获取随机旋转速度和方向
    
    随机生成一个旋转速度和方向
    
    Returns:
        float: 随机旋转速度
    """
    speed = random.uniform(MIN_ROTATION_SPEED, MAX_ROTATION_SPEED)
    direction = random.choice([-1, 1])
    return speed * direction

def draw_smooth_hexagon(surface, color, points, width):
    """增强平滑效果的六边形绘制
    
    通过多层次渐变边框和顶点平滑处理，实现更柔和的视觉效果
    
    Args:
        surface: 绘制表面
        color: 六边形颜色
        points: 六边形顶点列表
        width: 边框宽度
    """
    points = [(x * RENDER_SCALE, y * RENDER_SCALE) for x, y in points]
    width = width * RENDER_SCALE
    
    # 绘制多层渐变边框
    for i in range(3):
        outer_width = width + (2-i) * RENDER_SCALE
        alpha = 100 + i * 50
        pygame.draw.polygon(surface, (*color[:3], alpha), points, outer_width)
    
    # 主轮廓
    pygame.draw.polygon(surface, (*color[:3], 255), points, width)
    
    # 增强顶点平滑
    for point in points:
        for r in range(3):
            radius = (width // 2 - r) * RENDER_SCALE
            alpha = 150 + r * 35
            pygame.draw.circle(surface, (*color[:3], alpha), 
                             (int(point[0]), int(point[1])), 
                             radius)

def draw_glowing_circle(surface, color, position, radius):
    """增强平滑效果的发光球体绘制
    
    通过多层次光晕和渐变效果，实现发光球体的视觉效果
    
    Args:
        surface: 绘制表面
        color: 球体颜色
        position: 球体位置
        radius: 球体半径
    """
    position = (position[0] * RENDER_SCALE, position[1] * RENDER_SCALE)
    radius = radius * RENDER_SCALE
    
    # 绘制更多层次的光晕
    for i in range(8):
        alpha = 120 - i * 15
        radius_offset = i * 1.5
        glow_radius = radius + radius_offset * RENDER_SCALE
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color[:3], alpha), 
                         (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface, 
                    (position[0] - glow_radius, position[1] - glow_radius), 
                    special_flags=pygame.BLEND_ALPHA_SDL2)
    
    # 主体绘制添加渐变效果
    for i in range(3):
        current_radius = radius - i * RENDER_SCALE
        alpha = 255 - i * 40
        pygame.draw.circle(surface, (*color[:3], alpha), 
                         (int(position[0]), int(position[1])), 
                         int(current_radius))

# 游戏主循环初始化
clock = pygame.time.Clock()  # 创建时钟对象，用于控制游戏帧率
angle = 0                   # 六边形当前旋转角度
frame_count = 0            # 帧计数器，用于控制旋转速度变化
running = True             # 游戏运行标志

while running:
    # 事件处理：检查是否退出游戏
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 更新旋转速度和方向
    frame_count += 1
    if frame_count >= SPEED_CHANGE_INTERVAL:  # 每隔一定帧数改变旋转速度
        frame_count = 0
        target_rotation_speed = get_random_rotation_speed()
    
    # 平滑过渡到目标速度，使用线性插值
    speed_diff = target_rotation_speed - current_rotation_speed
    current_rotation_speed += speed_diff * ROTATION_ACCELERATION
    
    # 更新旋转角度，保持在0-360度范围内
    angle = (angle + current_rotation_speed) % 360
    
    # 获取六边形当前旋转后的顶点坐标
    hex_points = get_hex_points(angle)
    
    # 计算作用于球体的向心力
    centripetal_force = calculate_centripetal_force(ball_pos, current_rotation_speed)
    
    # 更新球的物理状态：添加重力和向心力，应用摩擦力
    ball_vel += GRAVITY + centripetal_force
    ball_vel *= FRICTION
    
    # 状态检查和修正：确保球的位置和速度在合理范围内
    ball_pos, ball_vel = check_ball_state(ball_pos, ball_vel)
    
    # 预测下一个位置，用于碰撞检测
    next_pos = ball_pos + ball_vel
    
    # 碰撞检测和处理：检查球是否与六边形边界发生碰撞
    ball_pos, ball_vel, collision = handle_collision(next_pos, ball_vel, hex_points, current_rotation_speed)
    
    # 如果发生碰撞，随机改变球的颜色，增加视觉反馈
    if collision:
        current_ball_color = get_random_ball_color()
    
    # 额外的安全检查：确保球不会卡在边缘
    if is_ball_too_close_to_edge(ball_pos, hex_points):
        ball_pos, ball_vel, collision = handle_collision(ball_pos, ball_vel, hex_points, current_rotation_speed)
        if collision:
            current_ball_color = get_random_ball_color()
    
    # 渲染部分
    # 清空绘图表面，准备新一帧的绘制
    drawing_surface.fill((0, 0, 0, 0))  # 使用透明填充清空表面
    
    # 绘制平滑的六边形边框
    draw_smooth_hexagon(drawing_surface, HEX_COLOR, hex_points, HEX_BORDER_WIDTH)
    
    # 绘制带光晕效果的球体
    draw_glowing_circle(drawing_surface, current_ball_color, 
                       (int(ball_pos.x), int(ball_pos.y)), 
                       BALL_RADIUS)
    
    # 最终渲染：将高分辨率表面缩放并绘制到屏幕
    screen.fill(BLACK)  # 使用背景色清空屏幕
    scaled_surface = pygame.transform.smoothscale(drawing_surface, (WIDTH, HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    
    # 更新显示并维持帧率
    pygame.display.flip()  # 刷新屏幕显示
    clock.tick(60)        # 限制帧率为60FPS

# 清理并退出
pygame.quit()
