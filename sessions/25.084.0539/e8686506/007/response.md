```python
"""
The transformation condenses the input grid into a smaller output grid, preserving the counts of the key colors (non-background colors). The background color of the output grid can be different from the input grid. The goal is to create the smallest representation preserving counts.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    # Flatten the grid and count the occurrences of each color
    color_counts = Counter(grid.flatten())
    # Return the most common color (background color)
    return color_counts.most_common(1)[0][0]

def get_key_colors_and_counts(grid):
    background_color = get_background_color(grid)
    key_colors = {}
    for color, count in Counter(grid.flatten()).items():
        if color != background_color:
            key_colors[color] = count
    return key_colors

def calculate_output_dimensions(total_key_pixels):
    # Calculate output grid dimensions, aiming for a near-square shape.
    output_rows = int(np.ceil(np.sqrt(total_key_pixels)))
    output_cols = int(np.ceil(total_key_pixels / output_rows))
    return output_rows, output_cols

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Get key colors and their counts
    key_colors_counts = get_key_colors_and_counts(input_grid)

    # Calculate the total number of key pixels
    total_key_pixels = sum(key_colors_counts.values())

    # Calculate output dimensions
    output_rows, output_cols = calculate_output_dimensions(total_key_pixels)
    
    # Create an output grid filled initially with -1 (representing unassigned)
    output_grid = np.full((output_rows, output_cols), -1, dtype=int)

    # Create a list of key color pixels, repeating each color by its count
    output_list = []
    for color, count in key_colors_counts.items():
        output_list.extend([color] * count)

    # Fill the output grid with the key colors.
    output_index = 0
    for r in range(output_rows):
        for c in range(output_cols):
            if output_index < len(output_list):
                output_grid[r, c] = output_list[output_index]
                output_index += 1
            # No else needed as grid initialized with -1

    return output_grid.tolist()
```