import numpy as np
from collections import Counter
import math

"""
Identify a single unique pixel (trigger pixel) in the input grid, distinct from the background color (most frequent color).
Determine the quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) of the grid where the trigger pixel resides by comparing its position to the grid's center.
Create an output grid initialized as a copy of the input grid.
Fill a rectangular region in the output grid with the trigger pixel's color. The rectangle's boundaries are determined by the quadrant:
- Top-Left: From top-left corner (0,0) to the trigger pixel's position (row, col), inclusive.
- Top-Right: From top edge (row 0) to trigger pixel row, and from trigger pixel column to right edge (W-1), inclusive.
- Bottom-Left: From trigger pixel row to bottom edge (H-1), and from left edge (col 0) to trigger pixel column, inclusive.
- Bottom-Right: From trigger pixel row to bottom edge (H-1), and from trigger pixel column to right edge (W-1), inclusive.
"""

def find_background_and_trigger(grid):
    """Finds the background color and the single trigger pixel."""
    colors = grid.flatten()
    color_counts = Counter(colors)
    
    # Background color is the most frequent one
    background_color = color_counts.most_common(1)[0][0]
    
    trigger_pixel_color = None
    trigger_pixel_pos = None
    
    # Find the single pixel that is not the background color
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != background_color:
                trigger_pixel_color = grid[r, c]
                trigger_pixel_pos = (r, c)
                # Assuming only one trigger pixel per grid based on examples
                return background_color, trigger_pixel_color, trigger_pixel_pos
                
    # Should not happen based on task description, but handle edge case
    return background_color, None, None 

def transform(input_grid):
    """
    Transforms the input grid by finding a unique pixel and filling a quadrant
    based on its position with its color.
    """
    # Convert input list of lists to a numpy array
    input_np = np.array(input_grid, dtype=int)
    
    # Get grid dimensions
    H, W = input_np.shape
    
    # Find the background color and the trigger pixel's color and position
    background_color, trigger_color, trigger_pos = find_background_and_trigger(input_np)
    
    if trigger_pos is None:
        # If no trigger pixel found (e.g., grid is all one color), return input
        return input_grid 
        
    trigger_row, trigger_col = trigger_pos
    
    # Initialize output_grid as a copy of the input grid
    output_np = input_np.copy()
    
    # Determine the grid center (using float division for comparison)
    center_row = H / 2.0
    center_col = W / 2.0

    # Determine the quadrant based on the trigger pixel's position
    # Note: Numpy slicing uses exclusive upper bounds, so ranges need adjustment.
    if trigger_row < center_row and trigger_col < center_col:
        # Top-Left Quadrant
        # Fill rows 0 to trigger_row (inclusive), columns 0 to trigger_col (inclusive)
        output_np[0:trigger_row + 1, 0:trigger_col + 1] = trigger_color
    elif trigger_row < center_row and trigger_col >= center_col:
        # Top-Right Quadrant
        # Fill rows 0 to trigger_row (inclusive), columns trigger_col to W-1 (inclusive)
        output_np[0:trigger_row + 1, trigger_col:W] = trigger_color
    elif trigger_row >= center_row and trigger_col < center_col:
        # Bottom-Left Quadrant
        # Fill rows trigger_row to H-1 (inclusive), columns 0 to trigger_col (inclusive)
        output_np[trigger_row:H, 0:trigger_col + 1] = trigger_color
    else: # trigger_row >= center_row and trigger_col >= center_col
        # Bottom-Right Quadrant
        # Fill rows trigger_row to H-1 (inclusive), columns trigger_col to W-1 (inclusive)
        output_np[trigger_row:H, trigger_col:W] = trigger_color

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_np.tolist()
    
    return output_grid