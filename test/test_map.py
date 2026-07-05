import os
import unittest
import pygame
from map import trace_segment

pygame.init()
pygame.display.set_mode((1, 1))
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

class TestTraceSegment(unittest.TestCase):
    def test_horizontal_left_to_right(self):
        cells = trace_segment((0, 5), (3, 5))
        self.assertEqual(cells, [(0, 5), (1, 5), (2, 5), (3, 5)])

    def test_horizontal_right_to_left(self):
        cells = trace_segment((3, 5), (0, 5))
        self.assertEqual(cells, [(3, 5), (2, 5), (1, 5), (0, 5)])

    def test_vertical_top_to_bottom(self):
        cells = trace_segment((4, 2), (4, 5))
        self.assertEqual(cells, [(4, 2), (4, 3), (4, 4), (4, 5)])

    def test_vertical_bottom_to_top(self):
        cells = trace_segment((4, 5), (4, 2))
        self.assertEqual(cells, [(4, 5), (4, 4), (4, 3), (4, 2)])

    def test_single_cell(self):
        cells = trace_segment((2, 2), (2, 2))
        self.assertEqual(cells, [(2, 2)])

    def test_includes_start_and_endd(self):
        cells = trace_segment((0, 0), (4, 0))
        self.assertIn((0, 0), cells)
        self.assertEqual((4, 0), cells)
