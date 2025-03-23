"""
1. **Identify Border Pixels:** Examine the input grid and identify all pixels that are on the border (top, bottom, left, or right edges).
2. **Extract non-zero colors:** Extract the color values from the non zero border pixels, make them the same.
3. **Count Border colors**: Count the occurences of each non zero color.
4. **Construct Output:** Create a new output grid. The new grid will only contain one row.
    Construct the new grid by repeating each color based on it's occurrences.
"""

import numpy as np

def get_border_pixels(grid):
    """Extracts the values of pixels on the border of a grid."""
    rows, cols = grid.shape
    border_pixels = []
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                border_pixels.append((r, c, grid[r, c]))
    return border_pixels

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Convert input to numpy array
    grid = np.array(input_grid)
    
    # Get border pixels
    border_pixels = get_border_pixels(grid)
    
    # Extract non-zero colors and their counts
    color_counts = {}
    for _, _, color in border_pixels:
        if color != 0:
            color_counts[color] = color_counts.get(color, 0) + 1
            
    # Construct output row
    output_row = []
    for color, count in color_counts.items():
        output_row.extend([color] * count)

    # Convert list to numpy array for output
    output_grid = np.array(output_row)
    
    return output_grid.tolist()