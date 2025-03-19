"""
1.  **Identify the Cross-Shaped Object:** Locate the contiguous blocks of color that form the horizontal and vertical lines, excluding the surrounding border of a different color.
2.  **Extract the Primary Shape Color**: Determine the color of the cross shape that is *not* the border.
3. **Create the Output:** Generate a new grid filled entirely with the extracted color from step 2. The size of this new grid is equal to the height and width of the shape. The height of the shape is the number of horizontal lines filled with this color in input grid, and the width of the shape is equal to the number of vertical lines filled with this color.
"""

import numpy as np

def get_cross_color(grid):
    # Find the most frequent color, excluding borders
    border_colors = set()
    border_colors.add(grid[0, 0])
    border_colors.add(grid[0, -1])
    border_colors.add(grid[-1, 0])
    border_colors.add(grid[-1, -1])
    
    # Flatten the grid and count color occurrences.
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    
    # Find the color with maximum count and is not a border color.
    max_count = 0
    cross_color = -1
    for color,count in color_counts.items():
        if color not in border_colors:
            if count > max_count:
              max_count = count
              cross_color = color
    return cross_color

def get_cross_dimensions(grid, cross_color):
    # Get the rows and cols that contains the color
    rows = np.any(grid == cross_color, axis=1)
    cols = np.any(grid == cross_color, axis=0)

    # Count contiguous blocks
    height = np.sum(rows)
    width = np.sum(cols)
    return height, width
    

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Identify the cross-shaped object's color.
    cross_color = get_cross_color(grid)
    
    # Get cross shape dimensions
    height, width = get_cross_dimensions(grid, cross_color)

    # Create the output grid filled with cross color.
    output_grid = np.full((height, width), cross_color, dtype=int)
    
    return output_grid.tolist()