from typing import Dict, List, Tuple, Protocol
from pygame.math import Vector2

# 使用 Protocol 而不是 TypedDict 来避免循环导入
class WindowConfig(Protocol):
    WIDTH: int
    HEIGHT: int
    RENDER_SCALE: int
    FPS: int

class PhysicsConfig(Protocol):
    GRAVITY: Vector2
    ELASTICITY: float
    FRICTION: float
    MAX_BALL_SPEED: float
    COLLISION_BUFFER: int

class HexagonConfig(Protocol):
    MIN_ROTATION_SPEED: float
    MAX_ROTATION_SPEED: float
    ROTATION_ACCELERATION: float
    SPEED_CHANGE_INTERVAL: int
    INITIAL_SPEED: float

class ColorsConfig(Protocol):
    BACKGROUND: Tuple[int, int, int]
    HEXAGON: Tuple[int, int, int]
    BALL_COLORS: List[Tuple[int, int, int]]

class GameConfig(Protocol):
    WINDOW: WindowConfig
    PHYSICS: PhysicsConfig
    COLORS: ColorsConfig
    HEXAGON: HexagonConfig 