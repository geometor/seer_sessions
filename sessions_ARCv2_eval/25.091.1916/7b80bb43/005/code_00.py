"""
Transforms the input grid by filling horizontal gaps of exactly three background 
pixels that are bounded by foreground pixels on the same row.

The transformation first identifies the background color (most frequent) and the 
foreground color (the other color present). Then, it iterates through each row 
of the input grid. Within each row, it searches for the specific pattern: 
Foreground Pixel, Background Pixel, Background Pixel, Background Pixel, Foreground Pixel. 
If this exact 5-pixel sequence is found, the three central background pixels 
in the corresponding positions of the output grid are changed to the foreground color. 
All other pixels retain their original color from the input grid.
"""

import numpy as np
from collections import Counter

def find_colors(grid):
    """
    Identifies the background (most frequent) and foreground (other) colors.

    Args:
        grid: A numpy array representing the grid.

    Returns:
        A tuple (background_color, foreground_color). 
        If only one color exists, foreground_color is None.
    """
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    # Handle edge case of a grid with only one color
    if len(counts) == 1:
        return list(counts.keys())[0], None 
    
    # Find the color with the highest count (background)
    background_color = counts.most_common(1)[0][0]
    
    # Find the other color (foreground)
    foreground_color = None
    for color in counts:
        if color != background_color:
            foreground_color = color
            break
            
    return background_color, foreground_color

def transform(input_grid):
    """
    Applies the 3-pixel horizontal gap filling transformation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy to modify, which will become the output grid
    output_np = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Determine the background and foreground colors
    background_color, foreground_color = find_colors(input_np)

    # If there's no foreground color (e.g., grid is uniform), no transformation needed
    if foreground_color is None:
        return output_np.tolist()

    # Iterate through each row of the grid
    for r in range(height):
        # Iterate through possible starting column indices 'c' for the 5-pixel pattern
        # The pattern is F B B B F, so it has length 5.
        # The loop needs to go up to width - 5 to allow checking c, c+1, c+2, c+3, c+4.
        for c in range(width - 4):
            # Check if the pixel at (r, c) is the foreground color
            is_pattern_start = input_np[r, c] == foreground_color
            # Check if the next three pixels are the background color
            is_gap_pixel1 = input_np[r, c + 1] == background_color
            is_gap_pixel2 = input_np[r, c + 2] == background_color
            is_gap_pixel3 = input_np[r, c + 3] == background_color
            # Check if the pixel after the gap is the foreground color
            is_pattern_end = input_np[r, c + 4] == foreground_color

            # If all conditions match the F B B B F pattern
            if is_pattern_start and is_gap_pixel1 and is_gap_pixel2 and is_gap_pixel3 and is_pattern_end:
                # Fill the 3-pixel gap in the output grid with the foreground color
                output_np[r, c + 1] = foreground_color
                output_np[r, c + 2] = foreground_color
                output_np[r, c + 3] = foreground_color

    # Convert the modified numpy array back to a list of lists for the final output
    return output_np.tolist()