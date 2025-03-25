```python
"""
Transforms an input grid by applying a fixed, position-independent color mapping to each pixel. The mapping swaps specific pairs of colors: Blue (1) <-> Gray (5), Red (2) <-> Magenta (6), Green (3) <-> Yellow (4), and Azure (8) <-> Maroon (9). Colors not involved in these pairs (White (0) and Orange (7)) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a pixel-wise color substitution based on a predefined mapping.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Define the color mapping rules
    color_map = {
        1: 5,  # Blue -> Gray
        5: 1,  # Gray -> Blue
        2: 6,  # Red -> Magenta
        6: 2,  # Magenta -> Red
        3: 4,  # Green -> Yellow
        4: 3,  # Yellow -> Green
        8: 9,  # Azure -> Maroon
        9: 8   # Maroon -> Azure
        # 0 (White) and 7 (Orange) map to themselves by default
    }

    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid as a copy of the input grid
    # This handles the default case where colors map to themselves
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Get the input color value
            input_color = input_grid[r, c]
            # Apply the mapping if the color is in the map
            if input_color in color_map:
                output_grid[r, c] = color_map[input_color]
            # Otherwise, the color remains unchanged (already handled by copying)

    return output_grid
```