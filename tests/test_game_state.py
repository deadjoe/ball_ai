import unittest
import pygame
from game_engine import GameState
from pygame.locals import QUIT, KEYDOWN, K_SPACE

class TestGameState(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.state = GameState()
        
    def tearDown(self):
        pygame.quit()
        
    def test_game_state_init(self):
        """测试游戏状态初始化"""
        self.assertTrue(self.state.running)
        self.assertFalse(self.state.paused)
        self.assertEqual(self.state.frame_count, 0)
        
    def test_handle_quit_event(self):
        """测试退出事件处理"""
        event = pygame.event.Event(QUIT)
        pygame.event.post(event)
        self.state.handle_events()
        self.assertFalse(self.state.running)
        
    def test_handle_pause_event(self):
        """测试暂停事件处理"""
        event = pygame.event.Event(KEYDOWN, {'key': K_SPACE})
        pygame.event.post(event)
        
        initial_pause_state = self.state.paused
        self.state.handle_events()
        self.assertNotEqual(self.state.paused, initial_pause_state) 