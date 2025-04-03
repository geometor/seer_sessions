"""
Identifies the first and last non-white pixels in a 1D input grid (row).
Creates an output grid of the same size, initialized to white (0).
Places the color of the first identified non-white pixel at its original position in the output.
Places the color of the last identified non-white pixel at its original position in the output.
All other pixels in the output remain white.
If the input contains only white pixels, the output is also all white.
If the input non-white segment has length 1, the first and last pixels are the same, resulting in one non-white pixel in the output.
"""

import numpy as np

def transform(input_grid_list):
    """
    Transforms a 1D input grid list based on the first and last non-white pixels.

    Args:
        input_grid_list: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Convert input list to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Get the dimensions (length) of the input grid
    width = input_grid.shape[0]
    
    # 1. Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    
    # 2. Find the indices of all non-white pixels (value != 0)
    non_white_indices = np.where(input_grid != 0)[0]
    
    # 3. Check if any non-white pixels were found
    if non_white_indices.size > 0:
        # Find the index of the first non-white pixel (minimum index)
        first_idx = np.min(non_white_indices)
        
        # Find the index of the last non-white pixel (maximum index)
        last_idx = np.max(non_white_indices)
        
        # Get the color of the non-white segment (all non-white pixels have the same color)
        # We can pick the color from the first non-white pixel found
        color = input_grid[first_idx]
        
        # 4. Place the color of the first non-white pixel at its original index in the output grid
        output_grid[first_idx] = color
        
        # 5. Place the color of the last non-white pixel at its original index in the output grid
        # Note: If first_idx == last_idx (segment length 1), this overwrites the same pixel, which is correct.
        output_grid[last_idx] = color
        
    # 6. Return the modified output grid as a list (to match expected output format if needed)
    return output_grid.tolist()
