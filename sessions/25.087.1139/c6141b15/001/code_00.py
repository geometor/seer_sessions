import numpy as np
from collections import Counter

"""
The transformation identifies the background color (the most frequent color) and the two other distinct colors present in the input grid. 
It then creates an output grid of the same dimensions where the positions of the two non-background colors are swapped, while the background color remains unchanged.
"""

def transform(input_grid):
    """
    Swaps the positions of the two non-background colors in the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the output grid with colors swapped.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=np.int8)
    
    # Find unique colors and their counts in the grid
    unique_colors, counts = np.unique(grid, return_counts=True)
    
    # Identify the background color as the most frequent color
    background_color_index = np.argmax(counts)
    background_color = unique_colors[background_color_index]
    
    # Identify the two non-background colors
    # These are the unique colors that are not the background color
    non_background_colors = [c for c in unique_colors if c != background_color]
    
    # Ensure exactly two non-background colors are found, as per observed examples
    # If not, return the original grid (or handle as an error, though examples suggest this won't happen)
    if len(non_background_colors) != 2:
        # This case is not expected based on the training data
        # Returning the input grid might be a safe default if the pattern doesn't hold
        return input_grid 
        
    color1 = non_background_colors[0]
    color2 = non_background_colors[1]
    
    # Create the output grid as a copy of the input grid initially
    output_grid = grid.copy()
    
    # Get the dimensions of the grid
    height, width = grid.shape
    
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # If the current cell has color1, change it to color2 in the output grid
            if grid[r, c] == color1:
                output_grid[r, c] = color2
            # If the current cell has color2, change it to color1 in the output grid
            elif grid[r, c] == color2:
                output_grid[r, c] = color1
            # If the current cell has the background color, it remains unchanged (already copied)
            
    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()
