import numpy as np
from scipy.ndimage import label, generate_binary_structure

"""
This transformation operates based on the number of distinct, contiguous objects 
of Red (2), White (0), and Blue (1) colors found in the input grid. 
Green (3) is treated as a background/separator color.

1. Identify and count the number of distinct objects for Red, White, and Blue.
2. Check if there is exactly one object of each color (Red=1, White=1, Blue=1).
3. If the condition (one of each) is TRUE:
    - Change all White pixels (0) to Blue (1).
    - Change all Blue pixels (1) to White (0).
    - Keep Red pixels (2) and all other colors unchanged.
4. If the condition is FALSE:
    - Change all Red pixels (2) to White (0).
    - Change all White pixels (0) to Blue (1).
    - Keep Blue pixels (1) and all other colors unchanged.
"""

def find_objects(grid, color):
    """
    Finds and counts the number of distinct contiguous objects of a specific color.
    
    Args:
        grid (np.array): The input grid.
        color (int): The color value to find objects for.
        
    Returns:
        int: The number of distinct objects of the specified color.
    """
    # Create a binary mask where True indicates the target color
    mask = (grid == color)
    # Define connectivity (8-connectivity allows diagonal connections)
    structure = generate_binary_structure(2, 2) 
    # Label connected components in the mask
    labeled_array, num_features = label(mask, structure=structure)
    # Return the count of distinct objects found
    return num_features

def transform(input_grid):
    """
    Applies a conditional color transformation based on the counts of Red, White, 
    and Blue objects in the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Count the number of distinct objects for Red, White, and Blue
    num_red_objects = find_objects(input_np, 2) # Red color = 2
    num_white_objects = find_objects(input_np, 0) # White color = 0
    num_blue_objects = find_objects(input_np, 1) # Blue color = 1
    
    # Check if the condition (exactly one object of each color) is met
    is_condition_met = (num_red_objects == 1 and 
                        num_white_objects == 1 and 
                        num_blue_objects == 1)
                        
    # Create a copy of the input grid to modify for the output
    output_grid = np.copy(input_np)
    
    # Apply the transformation rules based on the condition
    if is_condition_met:
        # Condition is TRUE: White -> Blue, Blue -> White
        # Find pixels that are White (0) in the input
        white_pixels = (input_np == 0)
        # Find pixels that are Blue (1) in the input
        blue_pixels = (input_np == 1)
        
        # Change White pixels to Blue in the output grid
        output_grid[white_pixels] = 1 
        # Change Blue pixels to White in the output grid
        output_grid[blue_pixels] = 0 
        # Red and other colors remain unchanged as they were copied initially
    else:
        # Condition is FALSE: Red -> White, White -> Blue
        # Find pixels that are Red (2) in the input
        red_pixels = (input_np == 2)
        # Find pixels that are White (0) in the input
        white_pixels = (input_np == 0)
        
        # Change Red pixels to White in the output grid
        output_grid[red_pixels] = 0
        # Change White pixels to Blue in the output grid
        output_grid[white_pixels] = 1
        # Blue and other colors remain unchanged as they were copied initially
        
    # Convert the final NumPy array back to a list of lists for the output
    return output_grid.tolist()