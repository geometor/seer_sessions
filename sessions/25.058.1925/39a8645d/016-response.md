# 39a8645d • 016 • refine_coder

---
```python
"""
The transformation rule depends on the objects present in the input grid.

1.  If the input grid contains yellow pixels, extract only the yellow pixels and reconstruct their relative positions in the output grid. The output grid's dimensions are determined by the maximum row and column differences between the extracted pixels, plus one.
2.  If the input grid contains a large green object taking a significant portion of the space, extract the top-left 7x7 section of the input grid.
3. If there is a large red object surrounding a gray object, extract the gray object.
4. If the input contains a large green "C" shape, extract the upper-left 9x11 section of the input grid.
5.  Otherwise, create an empty 1x1 grid (all white pixels).
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specific color in the grid."""
    return np.argwhere(grid == color)

def extract_yellow_pixels(input_grid):
    """Extracts yellow pixels and preserves their relative positions."""
    yellow_pixels = find_pixels_by_color(input_grid, 4)
    if len(yellow_pixels) == 0:
        return np.zeros((1, 1), dtype=int)
    min_row = np.min(yellow_pixels[:, 0])
    max_row = np.max(yellow_pixels[:, 0])
    min_col = np.min(yellow_pixels[:, 1])
    max_col = np.max(yellow_pixels[:, 1])
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for r, c in yellow_pixels:
        output_grid[r - min_row, c - min_col] = 4
    return output_grid

def extract_green_section(input_grid):
    """Extracts the top-left 7x7 section of the input grid."""
    return input_grid[:7, :7]

def extract_inner_object(input_grid, outer_color, inner_color):
    """Extract gray object if it is inside a red object"""
    outer_pixels = find_pixels_by_color(input_grid, outer_color)
    inner_pixels = find_pixels_by_color(input_grid, inner_color)

    if len(outer_pixels) == 0 or len(inner_pixels) == 0:
        return np.zeros((1, 1), dtype=int)

    min_row_outer = np.min(outer_pixels[:, 0])
    max_row_outer = np.max(outer_pixels[:, 0])
    min_col_outer = np.min(outer_pixels[:, 1])
    max_col_outer = np.max(outer_pixels[:, 1])

    min_row_inner = np.min(inner_pixels[:, 0])
    max_row_inner = np.max(inner_pixels[:, 0])
    min_col_inner = np.min(inner_pixels[:, 1])
    max_col_inner = np.max(inner_pixels[:, 1])
    
    # Check if inner object is with the outer object
    if (min_row_inner > min_row_outer and max_row_inner < max_row_outer and
        min_col_inner > min_col_outer and max_col_inner < max_col_outer):
        output_height = max_row_inner - min_row_inner + 1
        output_width = max_col_inner - min_col_inner + 1
        output_grid = np.zeros((output_height, output_width), dtype=int)
        for r, c in inner_pixels:
            output_grid[r-min_row_inner,c-min_col_inner] = inner_color
        return output_grid
    else:
        return np.zeros((1,1), dtype=int)


def extract_green_c_section(input_grid):
    """Extract upper-left 9 x 11 section."""
    return input_grid[:9, :11]
    

def transform(input_grid):
    """Transforms input_grid based on a set of rules."""
    # initialize output_grid
    output_grid = np.zeros((1, 1), dtype=int) # Default 1x1 white grid

    # change output pixels
    # 1. If yellow pixels exist, extract them
    if np.any(input_grid == 4):
        output_grid = extract_yellow_pixels(input_grid)
    # 2. If a large green object exists, extract 7x7 section
    elif np.sum(input_grid == 3) > 40:  # Arbitrary threshold for "large"
        output_grid = extract_green_section(input_grid)
         # 4. If a large green "C" shape exists, extract 9 x 11 secion.
    elif np.sum(input_grid == 3) > 30:  # Check after large object, before inner
        output_grid = extract_green_c_section(input_grid)
    # 3.  If there is a large red object and an inner gray object, extract the inner object
    elif np.any(input_grid == 2) and np.any(input_grid == 5):
        output_grid = extract_inner_object(input_grid, 2, 5) #red=2, gray=5


    return output_grid
```
