# 31aa019c • 006 • refine_coder

---
```python
"""
The transformation identifies colored object(s) in the input, calculates a reference position based on their combined locations, and replaces them with a 3x3 red square with a yellow center on a white background.
"""

import numpy as np

def find_colored_pixels(grid):
    """Finds coordinates of all non-white pixels."""
    colored_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                colored_pixels.append((row_idx, col_idx))
    return colored_pixels

def calculate_reference_position(colored_pixels):
    """Calculates a reference position (approximate center) based on colored pixel coordinates."""
    if not colored_pixels:
        return (0, 0)

    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')

    for row, col in colored_pixels:
        min_row = min(min_row, row)
        min_col = min(min_col, col)
        max_row = max(max_row, row)
        max_col = max(max_col, col)

    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    return (center_row, center_col)

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Find colored pixels in the input grid
    colored_pixels = find_colored_pixels(input_grid)

    # Calculate the reference position (center of bounding box)
    reference_row, reference_col = calculate_reference_position(colored_pixels)

    # Initialize output grid as all white (0) with same dimensions as input
    output_grid = np.zeros_like(input_grid)

    # Create the 3x3 red square (2)
    block_start_row = reference_row - 1
    block_start_col = reference_col - 1

    for i in range(3):
        for j in range(3):
            row = block_start_row + i
            col = block_start_col + j
            # Check bounds
            if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                output_grid[row, col] = 2

    # Change center pixel to yellow (4)
    center_block_row = block_start_row + 1
    center_block_col = block_start_col + 1
    # Check bounds
    if 0 <= center_block_row < output_grid.shape[0] and 0 <= center_block_col < output_grid.shape[1]:
        output_grid[center_block_row, center_block_col] = 4

    return output_grid
```
