"""
Transforms a grid based on the locations of gray pixels (5).
The output grid has the same dimensions as the input.
Identify the two distinct colors in the input grid: gray (5) and another color ('target_color').
Initialize an output grid filled with white (0).
Iterate through the input grid. If a cell contains gray (5), set the corresponding cell in the output grid to the 'target_color'. Otherwise, the output cell remains white (0).
"""

import numpy as np

def find_target_color(input_grid):
    """Finds the non-gray color in the input grid."""
    unique_colors = np.unique(input_grid)
    for color in unique_colors:
        if color != 5: # 5 is gray
            return color
    # Should not happen based on task description, but handle defensively
    # Maybe return a default or raise an error if only gray is found or no colors
    # For now, assuming the task constraints hold.
    return 0 # Default to white if something unexpected happens

def transform(input_grid):
    """
    Transforms the input grid based on the location of gray pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Get grid dimensions
    height, width = input_grid_np.shape

    # Initialize output_grid with white (0)
    output_grid = np.zeros((height, width), dtype=int) # 0 is white

    # Identify the target color (the non-gray color)
    target_color = find_target_color(input_grid_np)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the input cell's color is gray (5)
            if input_grid_np[r, c] == 5: # 5 is gray
                # If it's gray, set the corresponding output cell to the target_color
                output_grid[r, c] = target_color
            # If the input cell is not gray, the output cell remains white (0)
            # (already initialized)

    return output_grid.tolist() # Return as list of lists to match ARC standard if needed
