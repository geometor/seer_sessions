"""
1.  **Identify the Magenta Object:** Locate the contiguous region of magenta (color 6) pixels.

2.  **Expand Magenta:** Expand the magenta object by one pixel in all four cardinal directions (up, down, left, and right).

3. **Identify adjacent objects:** locate all objects adjacent to the magenta object, before and after expansion.

4.  **Move Combined Object:** Shift the expanded magenta object, and any objects that were adjacent to the *original* magenta object, upwards by one row. Pixels of the objects retain their original color.

5.  **Preserve Unmoved:** Any pixels not part of the moved objects should retain their original color and position in the output grid.
"""

import numpy as np

def find_object(grid, color):
    """Finds coordinates of pixels with the specified color."""
    return np.argwhere(grid == color)

def expand_object(grid, object_coords):
    """Expands the object by one pixel in all directions."""
    expanded_coords = set()
    for r, c in object_coords:
        expanded_coords.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            expanded_coords.add((r + dr, c + dc))
    return list(expanded_coords)

def find_adjacent_pixels(grid, object_coords):
    """Finds all pixels adjacent to the given object coordinates."""
    adjacent_pixels = set()
    for r, c in object_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                adjacent_pixels.add((nr, nc))
    return adjacent_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Identify the Magenta Object
    magenta_coords = find_object(input_grid, 6)
    if magenta_coords.size == 0:
        return output_grid

    # 2. Expand Magenta
    expanded_magenta_coords = expand_object(input_grid, magenta_coords)

    # 3. Identify adjacent objects (before expansion)
    adjacent_to_original = find_adjacent_pixels(input_grid, magenta_coords)
    adjacent_colors_original = set()
    for r, c in adjacent_to_original:
        if (r,c) not in magenta_coords:
            adjacent_colors_original.add((input_grid[r,c],(r,c))) # store the color

    # Create a mask for moving objects (expanded magenta + original adjacent)
    move_mask = np.zeros_like(input_grid, dtype=bool)
    # expanded magenta
    for r, c in expanded_magenta_coords:
        if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
            move_mask[r, c] = True
    # originally adjacent pixels, but not magenta
    for color, (r,c) in adjacent_colors_original:
        move_mask[r,c] = True

    # 4. Move Combined Object Upwards
    moved_grid = np.zeros_like(input_grid)
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if move_mask[r, c]:
                if 0 <= r - 1 < input_grid.shape[0]:
                    if (r,c) in expanded_magenta_coords:
                        moved_grid[r-1,c] = 6  # magenta
                    else:
                        for color, (orow, ocol) in adjacent_colors_original:
                            if r == orow and c == ocol:
                              moved_grid[r-1,c] = color


    # 5. Preserve Unmoved and Combine
    output_grid = np.where(moved_grid != 0, moved_grid, output_grid)

    return output_grid