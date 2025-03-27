```python
import numpy as np
from collections import defaultdict

"""
Identifies all unique non-white colors in the input grid. For each color, calculates its total count (size) and the minimum row index where it appears. Sorts these colors first by size in descending order, and then by minimum row index in ascending order as a tiebreaker. The output is a single-column grid containing the sorted colors.
"""

def calculate_properties(grid, color):
    """
    Calculates the size and minimum row index for a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to calculate properties for.

    Returns:
        tuple: (size, min_row) for the given color. Returns (0, -1) if color not found.
    """
    indices = np.where(grid == color)
    if len(indices[0]) == 0:
        return 0, -1  # Color not found
    
    size = len(indices[0])
    min_row = np.min(indices[0])
    return size, min_row

def transform(input_grid):
    """
    Transforms the input grid based on color properties and sorting.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        np.array: A 3x1 numpy array containing the sorted colors.
    """
    grid = np.array(input_grid)
    
    # 1. Identify all unique colors present in the input grid, ignoring the background color (white, 0).
    unique_colors = np.unique(grid)
    non_white_colors = [color for color in unique_colors if color != 0]
    
    color_data = []
    
    # 2. For each unique non-white color found:
    for color in non_white_colors:
        # a. Count the total number of pixels of that color (size).
        # b. Find the minimum row index (min_row).
        size, min_row = calculate_properties(grid, color)
        if size > 0: # Ensure the color actually exists
             color_data.append({'color': color, 'size': size, 'min_row': min_row})

    # 4. Sort this list of colors based on the following criteria:
    #    a. Primarily, sort in descending order of their 'size'.
    #    b. Secondarily, if two colors have the same 'size', sort them in ascending order of their 'min_row'.
    #    Using a lambda function for the sorting key: (-size, min_row) sorts by size descending, then min_row ascending.
    sorted_color_data = sorted(color_data, key=lambda x: (-x['size'], x['min_row']))
    
    # Extract the sorted colors
    sorted_colors = [item['color'] for item in sorted_color_data]

    # 5. Construct the output grid as a single column (assuming 3x1 based on examples)
    # Ensure the output is always 3x1 as per the examples
    if len(sorted_colors) != 3:
         # This case shouldn't happen based on the provided examples, but handle defensively
         # Maybe pad with 0 or raise an error? Based on task, 3 colors always exist.
         # We'll assume the number of unique non-white colors is always 3 for this task.
         pass
         
    output_grid = np.array(sorted_colors).reshape(-1, 1) # Reshape into a column vector

    return output_grid.tolist() # Return as list of lists as per standard ARC format if needed, or np.array
```