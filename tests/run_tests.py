import os
import sys
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入所有测试模块
from test_game_objects import TestGameObjects
from test_physics_engine import TestPhysicsEngine
from test_renderer import TestRenderer
from test_game_state import TestGameState
from test_integration import TestGameIntegration

def run_tests():
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestGameObjects,
        TestPhysicsEngine,
        TestRenderer,
        TestGameState,
        TestGameIntegration
    ]
    
    for test_class in test_classes:
        test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == '__main__':
    run_tests() 