"""
1. Identify Unique Colors: Examine the input grid and create a list of the unique colors present, *excluding* white (0).
2. Create Output Grid: Create a 2x2 output grid. Fill the grid as follows:
   - Top-left: The first unique color found (excluding white)
   - Top-right: The first unique color.
   - Bottom-left: The first unique color
   - Bottom-right: The second unique color (or the first if only one exists, excluding white)
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid into a 2x2 output grid based on unique colors."""

    # Convert input grid to a NumPy array for easier processing.
    input_array = np.array(input_grid)

    # 1. Identify Unique Colors (excluding white/0).
    unique_colors = np.unique(input_array)
    filtered_colors = [color for color in unique_colors if color != 0]

    # 2. Create Output Grid (2x2).
    output_grid = np.zeros((2, 2), dtype=int)

    # Ensure we have at least one color to work with.
    if len(filtered_colors) > 0:
        first_color = filtered_colors[0]

        # Fill top-left, top-right, and bottom-left with the first color.
        output_grid[0, 0] = first_color
        output_grid[0, 1] = first_color
        output_grid[1, 0] = first_color

        # Fill bottom-right with the second color, or the first if only one exists.
        if len(filtered_colors) > 1:
            second_color = filtered_colors[1]
            output_grid[1, 1] = second_color
        else:
            output_grid[1, 1] = first_color

    return output_grid.tolist()