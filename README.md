# 动态旋转六边形与弹跳球物理模拟

[![Python Application](https://github.com/deadjoe/ball_ai/actions/workflows/python-app.yml/badge.svg)](https://github.com/deadjoe/ball_ai/actions/workflows/python-app.yml)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Pygame Version](https://img.shields.io/badge/pygame-2.5.0-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/github/license/deadjoe/ball_ai)](https://github.com/deadjoe/ball_ai/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/deadjoe/ball_ai)](https://github.com/deadjoe/ball_ai/commits/main)
[![Issues](https://img.shields.io/github/issues/deadjoe/ball_ai)](https://github.com/deadjoe/ball_ai/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/deadjoe/ball_ai)](https://github.com/deadjoe/ball_ai/pulls)

这是一个基于Pygame的物理模拟项目，展示了一个在旋转六边形内部弹跳的发光球体。该项目结合了物理模拟、碰撞检测、粒子效果和平滑渲染等多个技术要素。
** Notice this code is totally written by Claude AI (Sonnet 3.5)

## 技术特点

### 1. 物理引擎实现
- 重力系统：模拟真实的重力加速度效果
- 向心力：基于旋转速度和距离计算向心力
- 摩擦力：实现速度衰减，模拟真实物理环境
- 碰撞检测：精确的多边形碰撞检测和响应
- 弹性碰撞：实现可配置的弹性系数

### 2. 渲染技术
- 抗锯齿处理：使用RENDER_SCALE实现高质量渲染
- 平滑渲染：多层次渐变边框和顶点平滑处理
- 发光效果：实现球体的动态光晕效果
- 双缓冲：使用pygame.DOUBLEBUF优化渲染性能
- 硬件加速：启用pygame.HWSURFACE提升性能

### 3. 动画效果
- 动态旋转：六边形的平滑旋转动画
- 速度变化：随机的旋转速度和方向变化
- 碰撞反馈：碰撞时的颜色变化效果
- 帧率控制：稳定的60FPS动画效果

### 4. 代码架构
- 模块化设计：功能清晰的函数划分
- 状态管理：完整的游戏状态控制
- 异常处理：完善的边界检查和异常处理
- 参数配置：易于调整的物理参数和视觉效果

## 核心功能模块

1. **物理计算模块**
   - `calculate_centripetal_force()`: 计算向心力
   - `check_ball_state()`: 状态检查和修正
   - `handle_collision()`: 碰撞检测和处理

2. **几何计算模块**
   - `get_hex_points()`: 计算六边形顶点
   - `point_in_polygon()`: 点在多边形内的检测
   - `get_closest_point_on_line()`: 点到线段距离计算

3. **渲染模块**
   - `draw_smooth_hexagon()`: 平滑六边形渲染
   - `draw_glowing_circle()`: 发光球体渲染

4. **游戏控制模块**
   - 事件处理
   - 状态更新
   - 帧率控制

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python ball.py
```

## 技术参数

- 窗口尺寸：800x600像素
- 渲染精度：2倍超采样
- 物理参数：
  - 重力加速度：0.5
  - 弹性系数：0.8
  - 摩擦系数：0.99
- 动画参数：
  - 帧率：60FPS
  - 旋转速度范围：0.5-5.0
  - 速度变化间隔：60帧

## 系统要求

- Python 3.x
- Pygame库
- 支持硬件加速的显示系统

## 优化特性

1. **性能优化**
   - 使用向量计算优化物理模拟
   - 硬件加速渲染
   - 优化的碰撞检测算法

2. **视觉优化**
   - 平滑抗锯齿处理
   - 多层次光晕效果
   - 动态颜色变化

3. **稳定性优化**
   - 完善的异常处理
   - 状态检查和修正
   - 防止数值不稳定

## 扩展性

该项目的模块化设计使其易于扩展，可以通过以下方式进行增强：

1. 添加新的物理效果
2. 自定义视觉效果
3. 增加交互功能
4. 修改游戏规则

## CI/CD

本项目使用 GitHub Actions 进行持续集成，包括：

- 自动化代码质量检查
- Python语法检查
- 依赖项安装测试

## 许可证

该项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

项目链接：[https://github.com/deadjoe/ball_ai](https://github.com/deadjoe/ball_ai)

## 贡献指南

1. Fork 该仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request
