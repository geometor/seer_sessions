"""
Accept a 3x3 input grid (InputGrid).
Create a new 6x6 output grid (OutputGrid).
Tile the OutputGrid with four 3x3 grids derived from the InputGrid:
- Top-Left quadrant: A direct copy of the InputGrid.
- Top-Right quadrant: A horizontally flipped version of the InputGrid.
- Bottom-Left quadrant: A vertically flipped version of the InputGrid.
- Bottom-Right quadrant: A version of the InputGrid flipped both horizontally and vertically.
Return the completed 6x6 OutputGrid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 6x6 output grid by tiling it with
    the original grid and its reflections.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    h, w = input_np.shape
    
    # Create the output grid with double the dimensions, initialized with zeros
    output_h = h * 2
    output_w = w * 2
    output_grid = np.zeros((output_h, output_w), dtype=int)
    
    # 1. Copy the InputGrid directly into the Top-Left quadrant.
    output_grid[0:h, 0:w] = input_np
    
    # 2. Create a horizontally flipped version and place it in the Top-Right quadrant.
    flipped_horizontal = np.fliplr(input_np)
    output_grid[0:h, w:output_w] = flipped_horizontal
    
    # 3. Create a vertically flipped version and place it in the Bottom-Left quadrant.
    flipped_vertical = np.flipud(input_np)
    output_grid[h:output_h, 0:w] = flipped_vertical
    
    # 4. Create a version flipped both horizontally and vertically and place it in the Bottom-Right quadrant.
    #    This is equivalent to rotating 180 degrees.
    flipped_both = np.fliplr(flipped_vertical) # Or np.flipud(flipped_horizontal) or np.rot90(input_np, 2)
    output_grid[h:output_h, w:output_w] = flipped_both
    
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
