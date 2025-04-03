import numpy as np
from collections import Counter

def find_dominant_non_white_color(grid):
    """
    Finds the most frequent non-white color in a grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        int or None: The most frequent non-white color, or None if no non-white colors exist.
    """
    non_white_pixels = grid[grid != 0]
    if non_white_pixels.size == 0:
        return None  # No non-white pixels found
    
    color_counts = Counter(non_white_pixels)
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by performing the following steps:
    1. Identifies all non-white pixels in the input grid.
    2. Counts the occurrences of each distinct non-white color.
    3. Determines the non-white color that occurs most frequently (the "dominant color").
    4. Creates an output grid of the same dimensions as the input.
    5. Populates the output grid:
       - White pixels (0) from the input remain white (0) in the output.
       - All non-white pixels from the input are replaced with the dominant color in the output.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # Find the dominant non-white color
    dominant_color = find_dominant_non_white_color(input_np)
    
    # If there are no non-white pixels, return the input grid as is
    if dominant_color is None:
        return input_np.tolist()
        
    # Initialize the output grid with the same shape as the input, filled with 0s (white)
    output_grid = np.zeros_like(input_np)
    
    # Iterate through each pixel of the input grid
    for r in range(input_np.shape[0]):
        for c in range(input_np.shape[1]):
            # If the input pixel is white (0), keep it white in the output
            if input_np[r, c] == 0:
                output_grid[r, c] = 0
            # If the input pixel is non-white, replace it with the dominant color
            else:
                output_grid[r, c] = dominant_color
                
    return output_grid.tolist()