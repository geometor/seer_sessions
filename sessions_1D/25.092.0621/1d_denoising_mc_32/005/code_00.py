"""
Transforms the input grid (represented as a 1D list of integers) by first identifying the most frequent non-white (0) color, termed the "main color". 
It then creates an output grid where all non-white pixels that are *not* the "main color" are replaced with the "main color". 
White pixels (0) and pixels already matching the "main color" remain unchanged. 
If the input grid contains only white pixels, it is returned unchanged.
"""

import numpy as np
from collections import Counter

def _find_main_color(grid_np):
    """
    Finds the most frequent non-white color in the grid.

    Args:
        grid_np (np.array): The input grid as a numpy array.

    Returns:
        int or None: The value of the most frequent non-white color,
                     or None if no non-white colors are found.
    """
    # Filter out white pixels (value 0)
    non_white_pixels = grid_np[grid_np != 0]

    # Handle case where the grid is all white or empty
    if non_white_pixels.size == 0:
        return None # Indicate no main color found

    # Count frequencies of non-white colors
    color_counts = Counter(non_white_pixels)

    # Find the color with the highest frequency
    # most_common returns a list of (element, count) tuples
    if not color_counts: # Should not happen if non_white_pixels.size > 0, but safety check
        return None 
        
    main_color = color_counts.most_common(1)[0][0]
    # Ensure the return type is a standard Python int, not a numpy type
    return int(main_color) 

def transform(input_grid):
    """
    Transforms the input grid by replacing less frequent non-white colors
    with the most frequent non-white color.

    Args:
        input_grid (list): A list of integers representing the input grid pixels.

    Returns:
        list: A list of integers representing the transformed output grid pixels.
    """
    # Convert input list to a numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Analyze the input grid to find the main color
    main_color = _find_main_color(input_grid_np)

    # If there's no main color (grid is all white or empty), return the original grid
    if main_color is None:
        return input_grid # Return original list

    # Initialize the output grid as a copy of the input
    output_grid_np = input_grid_np.copy()

    # Identify pixels that are non-white AND not the main color (impurity pixels)
    # Create a boolean mask for these pixels
    impurity_mask = (output_grid_np != 0) & (output_grid_np != main_color)
    
    # Replace the impurity pixels with the main color using the mask
    output_grid_np[impurity_mask] = main_color

    # Convert the result back to a list for the final output
    return output_grid_np.tolist()