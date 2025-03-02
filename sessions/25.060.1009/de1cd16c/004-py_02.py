"""
1. Divide the input grid into four roughly equal quadrants: top-left, top-right, bottom-left, and bottom-right.
2. Select the bottom-left quadrant.
3. Identify the dominant color of the bottom-left quadrant. This color will fill all the cells in the lower-left quadrant. Ignore the other colors.
4. Output the identified color as the result. The output is 1x1 grid with the color of the lower left quadrant.
"""

import numpy as np

def get_quadrant(grid, quadrant_name):
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant_name == "top-left":
        return grid[:mid_row, :mid_col]
    elif quadrant_name == "top-right":
        return grid[:mid_row, mid_col:]
    elif quadrant_name == "bottom-left":
        return grid[mid_row:, :mid_col]
    elif quadrant_name == "bottom-right":
        return grid[mid_row:, mid_col:]
    else:
        raise ValueError("Invalid quadrant name")

def get_dominant_color(grid):
    # Flatten the grid and count the occurrences of each color
    unique, counts = np.unique(grid, return_counts=True)
    
    # Create a dictionary of color counts, excluding the background
    color_counts = dict(zip(unique, counts))
    
    #find max
    max_color = 0
    max_count = 0
    
    for color, count in color_counts.items():
        if(count > max_count):
            max_count = count
            max_color = color
            
    return max_color


def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Get the bottom-left quadrant
    bottom_left_quadrant = get_quadrant(input_grid, "bottom-left")

    # Identify the dominant color in the bottom-left quadrant
    dominant_color = get_dominant_color(bottom_left_quadrant)

    # Create a 1x1 output grid with the dominant color
    output_grid = np.array([[dominant_color]])

    return output_grid