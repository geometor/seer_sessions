import numpy as np

"""
Determine the target color based on the counts of yellow (4) and orange (7) pixels in the input grid. 
If the counts are equal, the target color is azure (8). Otherwise, it's gray (5).
Create the output grid by replacing all yellow (4) and orange (7) pixels in the input grid with the determined target color, leaving other pixels (background white 0) unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the counts of yellow and orange pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    
    # Count the number of yellow (4) pixels
    count_yellow = np.count_nonzero(grid == 4)
    
    # Count the number of orange (7) pixels
    count_orange = np.count_nonzero(grid == 7)
    
    # Determine the target color based on the counts
    if count_yellow == count_orange:
        target_color = 8  # Azure
    else:
        target_color = 5  # Gray
        
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(grid)
    
    # Find the locations of yellow (4) pixels
    yellow_mask = (grid == 4)
    # Find the locations of orange (7) pixels
    orange_mask = (grid == 7)
    
    # Combine the masks to find all pixels that need replacement
    replacement_mask = yellow_mask | orange_mask
    
    # Replace the identified pixels with the target color in the output grid
    output_grid[replacement_mask] = target_color
    
    # Convert the NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()
