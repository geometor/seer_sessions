```python
"""
The transformation takes a 7x7 input grid and produces a 6x6 output grid.
The output grid contains a subset of the colors from the input grid, with colors 2 (red), 6 (magenta), and 7 (orange) removed. The counts of the remaining colors are preserved exactly. The spatial arrangement is not considered, only the color presence and counts.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Define colors to be removed
    colors_to_remove = [2, 6, 7]

    # Create a dictionary to store color counts from the input grid
    input_color_counts = {}
    for color in np.unique(input_grid):
        input_color_counts[color] = np.sum(input_grid == color)

    # Create a dictionary to store output color counts based on the rules.
    output_color_counts = {}
    for color, count in input_color_counts.items():
        if color not in colors_to_remove:
          output_color_counts[color] = count

    # Initialize the output grid with an arbitrary color (e.g., 0 which is white), we will fill later based on color and count only
    output_grid = np.zeros((6, 6), dtype=int)
    
    # Flatten the output grid to simplify filling
    output_grid_flat = output_grid.flatten()

    # Fill the flattened output grid with the correct colors and counts
    index = 0
    for color, count in output_color_counts.items():
        for _ in range(count):
            if index < len(output_grid_flat):
                output_grid_flat[index] = color
                index += 1

    # Reshape the flattened array back into the 6x6 output grid
    output_grid = output_grid_flat.reshape((6, 6))

    return output_grid.tolist()
```