import os
import unittest
import pygame
from map import cell_to_pixel, trace_segment, build_path_cells, pixel_to_cell

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
        self.assertIn((4, 0), cells)


class TestBuildPathCells(unittest.TestCase):
    def test_return_ordered_list_and_set(self):
        waypoints = [(0,0), (3, 0)]
        ordered, seen = build_path_cells(waypoints)
        self.assertIsInstance(ordered, list)
        self.assertIsInstance(seen, set)

    def test_no_duplicates(self):
        waypoints = [(0, 0), (3, 0), (3, 3)]
        ordered, _ = build_path_cells(waypoints)
        self.assertEqual(len(ordered), len(set(ordered)))

    def test_correct_cell_count(self):
        waypoints = [(0, 0), (3, 0)]
        ordered, _ = build_path_cells(waypoints)
        self.assertEqual(len(ordered), 4)

    def test_set_matches_list(self):
        waypoints = [(0, 0), (3, 0), (3, 3)]
        ordered, seen = build_path_cells(waypoints)
        self.assertEqual(set(ordered), seen)
    

class TestCellToPixel(unittest.TestCase):
    def test_origin_cell(self):
        self.assertEqual(cell_to_pixel(0, 0), (24, 24))

    def test_second_col(self):
        self.assertEqual(cell_to_pixel(1, 0), (72, 24))

    def test_second_row(self):
        self.assertEqual(cell_to_pixel(0, 1), (24, 72))

    def test_returns_center(self):
        x, y = cell_to_pixel(2, 3)
        self.assertEqual(x, 2 * 48 + 24)
        self.assertEqual(y, 3 * 48 + 24)


class PixelToCell(unittest.TestCase):
    def test_origin(self):
        self.assertEqual(pixel_to_cell(0, 0), (0, 0))

    def test_center_of_first_cell(self):
        self.assertEqual(pixel_to_cell(24, 24), (0, 0))

    def test_second_cell(self):
        self.assertEqual(pixel_to_cell(72, 24), (1, 0))



if __name__ == '__main__':
    unittest.main()
