```python
import numpy as np
from collections import defaultdict

"""
Identifies all distinct non-background colored pixel groups in the input grid.
For each color group (all pixels of a specific color), determines a horizontal 
movement direction: Red (2) and Green (3) move left, Blue (1) and Yellow (4) 
move right.
Calculates the necessary horizontal shift to move the entire color group such 
that its leftmost pixel reaches column 0 (for left movement) or its rightmost 
pixel reaches the last column (for right movement).
Applies this shift to all pixels of that color group and places them onto a 
new grid, preserving their original vertical positions and relative horizontal 
arrangement. The final output grid contains all shifted color groups against 
the original background color.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Moves groups of pixels horizontally based on their color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid_np = np.zeros_like(input_np)  # Initialize with background (0)

    # 1. Identify all pixels for each non-background color
    color_pixels = defaultdict(list)
    unique_colors = np.unique(input_np)
    non_background_colors = unique_colors[unique_colors != 0]

    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:
                color_pixels[color].append((r, c))

    # 2. Process each color group
    for color, pixels in color_pixels.items():
        if not pixels:
            continue

        # 3a. Determine movement direction
        direction = None
        if color in [2, 3]:  # Red, Green
            direction = 'left'
        elif color in [1, 4]:  # Blue, Yellow
            direction = 'right'
        else:
            # If color has no defined movement, keep original position (or handle differently)
            # For this task, based on examples, only 1,2,3,4 move.
            # If other colors appear, they would stay put under this logic.
             direction = None # or 'stay'

        # 3b. Calculate target horizontal position shift
        cols = [c for r, c in pixels]
        min_col = min(cols)
        max_col = max(cols)
        dx = 0  # Default shift is 0 (no movement)

        if direction == 'left':
            dx = -min_col  # Shift needed to move min_col to 0
        elif direction == 'right':
            dx = (width - 1) - max_col  # Shift needed to move max_col to width-1

        # 3c. Calculate new coordinates and place on output grid
        for r, c in pixels:
            new_c = c + dx
            # Ensure the new position is within grid bounds (should be by calculation logic)
            if 0 <= new_c < width:
                 # 3d. Place the object pixel onto the output grid
                output_grid_np[r, new_c] = color

    # 4. Return the final output grid
    return output_grid_np.tolist()
```