```python
import numpy as np
from collections import Counter

"""
1. Determine the background color (most frequent) of the input grid.
2. Identify all unique colors present in the input grid that are not the background color.
3. For each unique non-background color, find the minimum row index (topmost row) where it appears.
4. Sort these unique non-background colors based on their minimum row index (ascending).
5. Create a 5x3 output grid.
6. Fill the top (5 - N) rows with the background color, where N is the number of unique non-background colors.
7. Fill the subsequent N rows (from row 5-N down to row 4) with the sorted colors, one color per row, filling the entire row.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # If grid is empty or has only one color, that's the background
    if not counts:
        return 0 # Default to white if grid is empty? Or handle error? Assuming non-empty based on ARC.
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Transforms the input grid by identifying unique non-background colors,
    sorting them by their first appearance row, and creating a 5x3 output grid
    with rows filled by these colors (bottom-up) and padded with the background color.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_height = 5
    output_width = 3

    # 1. Determine the background color
    background_color = find_background_color(input_np)

    # 2. & 3. Identify unique non-background colors and their minimum row index
    color_first_row = {}
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != background_color:
                if color not in color_first_row:
                    color_first_row[color] = r

    # 4. Sort the unique non-background colors by their minimum row index
    # Sort items by row index (value), then extract colors (key)
    sorted_colors = [color for color, row in sorted(color_first_row.items(), key=lambda item: item[1])]
    
    num_unique_colors = len(sorted_colors)

    # 5. Create a 5x3 output grid, initialized with a placeholder (e.g., -1) or background
    output_np = np.full((output_height, output_width), background_color, dtype=int) # Initialize with background

    # 6. & 7. Fill the output grid
    # Calculate the starting row index for the sorted colors
    start_row = output_height - num_unique_colors

    # Fill the bottom N rows with the sorted colors
    for i in range(num_unique_colors):
        row_index = start_row + i
        color_to_fill = sorted_colors[i]
        output_np[row_index, :] = color_to_fill

    # The top rows are already filled with background_color due to initialization

    # Convert back to list of lists for the expected output format
    output_grid = output_np.tolist()

    return output_grid
```