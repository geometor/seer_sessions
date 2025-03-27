import numpy as np
from collections import Counter

"""
Identifies two non-background colors in the input grid. One color appears exactly once (the 'indicator color'), and the other forms a larger object (the 'original color'). The transformation recolors all pixels of the 'original color' to the 'indicator color' and changes the single pixel of the 'indicator color' to the background color (0).
"""

def transform(input_grid):
    """
    Recolors the main object based on the color of a single indicator pixel.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Define background color
    background_color = 0
    
    # Find all unique colors and their counts, excluding the background
    colors, counts = np.unique(grid[grid != background_color], return_counts=True)
    
    indicator_color = -1
    original_color = -1
    indicator_location = None
    
    # Identify the indicator color (appears once) and the original object color
    for color, count in zip(colors, counts):
        if count == 1:
            indicator_color = color
            # Find the location of the indicator pixel
            loc = np.where(grid == indicator_color)
            # Ensure only one location is found, extract row and column
            if len(loc[0]) == 1:
                 indicator_location = (loc[0][0], loc[1][0])
            else:
                # Handle edge case/error: more than one pixel found, though count was 1 (should not happen with np.unique logic)
                # Or potentially the indicator color wasn't found if counts were wrong.
                # For now, assume input follows the observed pattern.
                pass 
        else:
            # Assume the other non-background color is the original object color
            original_color = color
            
    # Check if both colors were successfully identified
    if indicator_color == -1 or original_color == -1 or indicator_location is None:
        # If the pattern isn't matched (e.g., not exactly two non-background colors, 
        # or no color appears exactly once), return the original grid or handle error.
        # For this task, based on examples, we assume the pattern holds.
        # If necessary, add more robust error handling here.
        print("Warning: Could not identify indicator and/or original color based on expected pattern.")
        return input_grid # Return original grid if pattern fails

    # Create the output grid as a copy of the input grid
    output_grid = np.copy(grid)
    
    # Recolor the object: find all pixels with the original color and change them to the indicator color
    output_grid[output_grid == original_color] = indicator_color
    
    # Change the original indicator pixel location to the background color
    if indicator_location:
        output_grid[indicator_location] = background_color
        
    # Convert the result back to a list of lists
    return output_grid.tolist()
