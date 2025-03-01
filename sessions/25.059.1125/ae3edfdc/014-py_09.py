"""
1.  **Identify Objects:** Locate all orange (7) pixels and blue (1) pixels within the input grid. Empty cells are represented by 0.
2.  **Orange Expansion:** Orange pixels expand into adjacent (up, down, left, right) empty (0) pixels, *but only if that empty pixel lies on a direct horizontal or vertical path between the expanding orange pixel and a blue pixel*.
3.  **Expansion Target:** The expansion of orange pixels is directed towards blue pixels.
4.  **Stopping Condition:** Orange expansion continues until *every* blue pixel has at least one orange pixel adjacent to it (horizontally or vertically).
5.  **Immovable Objects:** Blue pixels, and any other non-orange and non-empty pixels, do not change their positions or colors. Orange pixels will grow *around* these obstacles.
6. **Prioritization:** If an empty cell is adjacent to more than one orange pixel, each of which could lead toward a blue pixel on distinct paths, all such orange will grow.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def is_on_path(orange_pixel, blue_pixel, empty_pixel):
    """Checks if the empty pixel is on a direct path between orange and blue."""
    # Check if they are in the same row or column
    if (orange_pixel[0] == blue_pixel[0] and orange_pixel[0] == empty_pixel[0]) or \
       (orange_pixel[1] == blue_pixel[1] and orange_pixel[1] == empty_pixel[1]):
        
        # Check if empty_pixel is between orange_pixel and blue_pixel
        if orange_pixel[0] == blue_pixel[0]:  # Same row
            col_min = min(orange_pixel[1], blue_pixel[1])
            col_max = max(orange_pixel[1], blue_pixel[1])
            return col_min < empty_pixel[1] < col_max
        else:  # Same column
            row_min = min(orange_pixel[0], blue_pixel[0])
            row_max = max(orange_pixel[0], blue_pixel[0])
            return row_min < empty_pixel[0] < row_max
    return False



def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)
    orange_pixels = find_pixels(input_grid, 7)
    blue_pixels = find_pixels(input_grid, 1)

    # Create a set for efficient checking of orange pixel locations
    orange_set = set(tuple(p) for p in orange_pixels)

    # Continue expanding until no more changes occur
    while True:
        new_orange_set = set(orange_set)  # Copy for iteration
        expansion_occurred = False

        for blue_pixel in blue_pixels:
            # Check for adjacent empty cells to this blue pixel
            for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Adjacent positions
                adj_row, adj_col = blue_pixel[0] + r, blue_pixel[1] + c

                # Check bounds and if the adjacent cell is empty
                if 0 <= adj_row < output_grid.shape[0] and 0 <= adj_col < output_grid.shape[1] and \
                   output_grid[adj_row, adj_col] == 0:

                    # Check if there's an *existing* orange pixel next to *this* empty AND on the path
                    for orow, ocol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        neighbor_row, neighbor_col = adj_row + orow, adj_col + ocol
                        neighbor_pixel = (neighbor_row, neighbor_col)

                        if neighbor_pixel in orange_set and is_on_path(neighbor_pixel, blue_pixel, (adj_row, adj_col)):
                          #Found a neighbor, set it to orange
                          new_orange_set.add((adj_row,adj_col))
                          output_grid[adj_row, adj_col] = 7
                          expansion_occurred = True

        orange_set = new_orange_set
        if not expansion_occurred:
            break
    return output_grid