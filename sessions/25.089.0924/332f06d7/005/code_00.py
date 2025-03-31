import numpy as np
from scipy.ndimage import label, generate_binary_structure

"""
Transforms the input grid based on the connectivity of Blue (1) pixels.

The transformation rule depends on whether all Blue (1) pixels in the input grid
form a single contiguous object when considering only 4-way (horizontal and vertical)
connections.

1. Identify all distinct groups (objects) of Blue pixels using 4-way connectivity.
2. Count the number of these distinct Blue objects.
3. Check the condition: Is the number of Blue objects exactly 1?

4. If the condition is TRUE (exactly one 4-way connected Blue object):
    - Change all White pixels (0) to Blue (1).
    - Change all Blue pixels (1) to White (0).
    - Keep Red pixels (2) and all other colors unchanged.
5. If the condition is FALSE (more than one 4-way connected Blue object):
    - Change all Red pixels (2) to White (0).
    - Change all White pixels (0) to Blue (1).
    - Keep Blue pixels (1) and all other colors unchanged.
"""

def count_objects_4way(grid, color):
    """
    Counts the number of distinct objects of a specific color using 4-way connectivity.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to find objects for.

    Returns:
        int: The number of distinct objects found.
    """
    # Create a binary mask where True indicates the target color
    mask = (grid == color)
    # If no pixels of the target color exist, return 0 objects
    if not np.any(mask):
        return 0
    # Define 4-connectivity structure (no diagonals)
    structure = generate_binary_structure(2, 1) 
    # Label connected components in the mask
    labeled_array, num_features = label(mask, structure=structure)
    # Return the count of distinct objects found
    return num_features

def transform(input_grid):
    """
    Applies the conditional color transformation based on the 4-way connectivity
    of Blue pixels.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # --- Determine the condition ---
    # Count the number of distinct Blue(1) objects using 4-way connectivity
    num_blue_objects = count_objects_4way(input_np, 1) # Blue color = 1
    
    # Condition check: Is there exactly one Blue object?
    is_single_blue_object = (num_blue_objects == 1)
    
    # --- Apply the transformation ---
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    
    if is_single_blue_object:
        # Apply Rule B: White -> Blue, Blue -> White
        # Find pixels that are White (0) in the input
        white_pixels_mask = (input_np == 0)
        # Find pixels that are Blue (1) in the input
        blue_pixels_mask = (input_np == 1)
        
        # Change White pixels to Blue in the output grid
        output_grid[white_pixels_mask] = 1 
        # Change Blue pixels to White in the output grid
        output_grid[blue_pixels_mask] = 0 
        # Red and other colors remain unchanged (already copied)
    else:
        # Apply Rule A: Red -> White, White -> Blue
        # Find pixels that are Red (2) in the input
        red_pixels_mask = (input_np == 2)
        # Find pixels that are White (0) in the input
        white_pixels_mask = (input_np == 0)
        
        # Change Red pixels to White in the output grid
        output_grid[red_pixels_mask] = 0
        # Change White pixels to Blue in the output grid
        output_grid[white_pixels_mask] = 1
        # Blue and other colors remain unchanged (already copied)
        
    # Convert the final NumPy array back to a list of lists for the output format
    return output_grid.tolist()