"""
1.  **Identify Background and Outer Frame:** The background is the most prevalent color in the input grid. The outer frame is usually, but not always, the color of the corners/edges of the input grid. We will assume it is the color of pixel (0,0).

2.  **Identify Inner Object:**  Find the largest contiguous rectangular block of a single color that is fully enclosed by the outer frame color *and* is not touching the edges of the input grid. The "inner object" should have a uniform color.

3.  **Find Largest Inner Square:** Within this inner object, find the largest possible square region of uniform color.

4.  **Create Output Grid:** Create a new, empty square grid.  The side length of this grid is equal to the side length of the largest inner square found in step 3, plus 2 (for the frame).

5.  **Frame the Output:** Fill the entire output grid with the "outer frame" color (from Step 1).

6.  **Paste Inner Square:**  Copy the largest inner square (from Step 3) into the center of the output grid. The inner square should be inset by one pixel on all sides, creating the frame. If no inner object is found, return an empty grid.
"""

import numpy as np

def get_outer_frame_color(grid):
    """Gets the outer frame color, assumed to be at (0, 0)."""
    return grid[0, 0]

def find_inner_object(grid):
    """Finds the largest enclosed rectangular object, excluding the edge color."""
    rows, cols = grid.shape
    outer_frame_color = get_outer_frame_color(grid)
    inner_colors = {}

    # Identify all potential inner objects and their bounds
    for r in range(1, rows - 1):  # Exclude edges
        for c in range(1, cols - 1):  # Exclude edges
            color = grid[r, c]
            if color != outer_frame_color:
                if color not in inner_colors:
                    inner_colors[color] = {
                        'min_r': rows, 'max_r': -1,
                        'min_c': cols, 'max_c': -1
                    }
                inner_colors[color]['min_r'] = min(inner_colors[color]['min_r'], r)
                inner_colors[color]['max_r'] = max(inner_colors[color]['max_r'], r)
                inner_colors[color]['min_c'] = min(inner_colors[color]['min_c'], c)
                inner_colors[color]['max_c'] = max(inner_colors[color]['max_c'], c)

    largest_object = None
    largest_area = 0

    # Check for enclosure and find the largest
    for color, bounds in inner_colors.items():
        is_enclosed = True
        # Check top and bottom
        for c in range(bounds['min_c'], bounds['max_c'] + 1):
            if grid[bounds['min_r'] - 1, c] != outer_frame_color or grid[bounds['max_r'] + 1, c] != outer_frame_color:
                is_enclosed = False
                break
        if is_enclosed:
          #check left and right
          for r in range(bounds['min_r'], bounds['max_r'] + 1):
            if grid[r, bounds['min_c'] - 1] != outer_frame_color or grid[r, bounds['max_c'] + 1] != outer_frame_color:
                is_enclosed = False
                break

        if is_enclosed:
            width = bounds['max_c'] - bounds['min_c'] + 1
            height = bounds['max_r'] - bounds['min_r'] + 1
            area = width * height
            if area > largest_area:
                largest_area = area
                largest_object = (color, bounds)

    return largest_object

def find_largest_inner_square(grid, object_bounds):
    """Finds the largest square within the inner object."""
    if not object_bounds:
        return None

    color, bounds = object_bounds
    max_side = min(bounds['max_c'] - bounds['min_c'] + 1, bounds['max_r'] - bounds['min_r'] + 1)

    for side in range(max_side, 0, -1):  # Iterate from largest possible side down
        for r_start in range(bounds['min_r'], bounds['max_r'] - side + 2):
            for c_start in range(bounds['min_c'], bounds['max_c'] - side + 2):
                # Check if square of this size is uniform
                is_uniform = True
                for r in range(r_start, r_start + side):
                    for c in range(c_start, c_start + side):
                        if grid[r,c] != color:
                          is_uniform = False
                          break
                    if not is_uniform:
                      break;

                if is_uniform:
                    return {
                        'min_r': r_start,
                        'max_r': r_start + side - 1,
                        'min_c': c_start,
                        'max_c': c_start + side - 1,
                        'side': side
                    }

    return None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    outer_frame_color = get_outer_frame_color(input_grid)
    inner_object = find_inner_object(input_grid)

    if not inner_object:
        return []  # Return empty grid if no inner object

    inner_square = find_largest_inner_square(input_grid, inner_object)
    if not inner_square:
        return []
    inner_color = inner_object[0]

    output_side = inner_square['side'] + 2
    output_grid = np.full((output_side, output_side), outer_frame_color)

    for r in range(inner_square['side']):
        for c in range(inner_square['side']):
            output_grid[r + 1, c + 1] = input_grid[inner_square['min_r'] + r, inner_square['min_c'] + c]

    return output_grid.tolist()