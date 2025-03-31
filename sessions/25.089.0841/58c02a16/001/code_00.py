"""
Identifies a pattern in the top-left corner of the input grid, defined by the smallest bounding box containing all non-background colors anchored at (0,0). Then, it tiles this pattern across the entire output grid, which has the same dimensions as the input grid. The background color is determined as the most frequent color in the input grid.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    if grid.size == 0:
        return 0 # Default background color if grid is empty
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default if counter is empty (e.g., empty grid passed somehow)
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_pattern_bounds(grid, background_color):
    """Finds the bounds (max_row, max_col) of the non-background pattern."""
    max_r, max_c = -1, -1
    non_background_found = False
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                max_r = max(max_r, r)
                max_c = max(max_c, c)
                non_background_found = True

    # If no non-background color is found, the pattern is just the top-left 1x1 cell
    if not non_background_found:
        return 0, 0
        
    return max_r, max_c

def transform(input_grid):
    """
    Tiles the top-left pattern of the input grid to fill the output grid.
    
    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    if input_np.size == 0:
        return np.array([[]], dtype=int) # Handle empty input

    H, W = input_np.shape

    # 1. Determine the background color
    background_color = find_background_color(input_np)

    # 2. Find the maximum row and column index of non-background colors
    max_r, max_c = find_pattern_bounds(input_np, background_color)

    # 3. Define the pattern dimensions
    pattern_h = max_r + 1
    pattern_w = max_c + 1

    # 4. Extract the pattern
    # Ensure indices are valid even if pattern_h/w are 0 (though handled by find_pattern_bounds returning 0,0)
    pattern = input_np[0:pattern_h, 0:pattern_w] 
    
    # Handle case where pattern extraction might yield an empty array if input was e.g., 0xN or Nx0
    # This shouldn't happen with ARC constraints but good practice.
    if pattern.size == 0: 
         # If pattern is empty (e.g., due to 0 pattern height/width derived from empty input)
         # Re-evaluate: maybe just return an empty grid of correct dims or based on input?
         # For ARC, input dimensions >= 1x1. If all background, pattern is 1x1 of background.
         if H > 0 and W > 0: #Ensure input wasn't totally empty
             pattern = np.array([[input_np[0,0]]]) # Default to top-left 1x1
             pattern_h, pattern_w = 1, 1
         else: # Truly empty input grid case
             return np.array([[]], dtype=int)


    # 5. Create the output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_np)

    # 6. Tile the pattern onto the output grid
    for r in range(H):
        for c in range(W):
            # Use modulo arithmetic to repeat the pattern
            # Ensure pattern dimensions are not zero before modulo
            if pattern_h > 0 and pattern_w > 0:
                output_grid[r, c] = pattern[r % pattern_h, c % pattern_w]
            # else: # Should be covered by earlier checks, but as a failsafe
            #    output_grid[r, c] = background_color # Or some default

    return output_grid.tolist() # Return as list of lists as per ARC standard format if needed, otherwise return np.array
