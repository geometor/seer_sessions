import numpy as np

"""
Transforms a 3x3 input grid into a 9x9 output grid by tiling transformed versions of the input.

1.  Define the 3x3 input grid as the "original grid".
2.  Create three transformed versions of the original grid:
    a.  "Vertically Flipped": Flip the original grid top-to-bottom.
    b.  "Horizontally Flipped": Flip the original grid left-to-right.
    c.  "Combined Flip": Flip the original grid both top-to-bottom and left-to-right.
3.  Initialize an empty 9x9 output grid.
4.  Assemble the output grid by placing the original grid and its transformed versions 
    into nine 3x3 subgrid positions according to the following pattern:
    
    | Combined Flip    | Vertically Flipped | Combined Flip    |
    |------------------|--------------------|------------------|
    | Horizontally Flipped | Original Grid      | Horizontally Flipped |
    |------------------|--------------------|------------------|
    | Combined Flip    | Vertically Flipped | Combined Flip    |
    
5.  The assembled 9x9 grid is the final output.
"""

def vertical_flip(grid):
    """Flips a grid vertically (top-to-bottom)."""
    return np.flipud(grid)

def horizontal_flip(grid):
    """Flips a grid horizontally (left-to-right)."""
    return np.fliplr(grid)

def combined_flip(grid):
    """Flips a grid both vertically and horizontally."""
    # Equivalent to rotating 180 degrees
    return np.rot90(grid, 2)
    # Alternatively: return vertical_flip(horizontal_flip(grid))

def transform(input_grid):
    """
    Applies the tiling and reflection transformation to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    original_grid = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid (should be 3x3)
    input_height, input_width = original_grid.shape
    
    # Calculate the dimensions of the output grid (3 times the input)
    output_height = input_height * 3
    output_width = input_width * 3
    
    # Create the transformed versions of the input grid
    vf_grid = vertical_flip(original_grid)
    hf_grid = horizontal_flip(original_grid)
    cf_grid = combined_flip(original_grid)
    
    # Initialize the output grid with zeros (or any placeholder)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Define the subgrid size
    sub_h, sub_w = input_height, input_width

    # Assemble the output grid by placing the subgrids according to the pattern
    
    # Row 0
    output_grid[0*sub_h : 1*sub_h, 0*sub_w : 1*sub_w] = cf_grid  # Top-Left: Combined Flip
    output_grid[0*sub_h : 1*sub_h, 1*sub_w : 2*sub_w] = vf_grid  # Top-Mid: Vertical Flip
    output_grid[0*sub_h : 1*sub_h, 2*sub_w : 3*sub_w] = cf_grid  # Top-Right: Combined Flip
    
    # Row 1
    output_grid[1*sub_h : 2*sub_h, 0*sub_w : 1*sub_w] = hf_grid  # Mid-Left: Horizontal Flip
    output_grid[1*sub_h : 2*sub_h, 1*sub_w : 2*sub_w] = original_grid # Mid-Center: Original
    output_grid[1*sub_h : 2*sub_h, 2*sub_w : 3*sub_w] = hf_grid  # Mid-Right: Horizontal Flip

    # Row 2
    output_grid[2*sub_h : 3*sub_h, 0*sub_w : 1*sub_w] = cf_grid  # Bottom-Left: Combined Flip
    output_grid[2*sub_h : 3*sub_h, 1*sub_w : 2*sub_w] = vf_grid  # Bottom-Mid: Vertical Flip
    output_grid[2*sub_h : 3*sub_h, 2*sub_w : 3*sub_w] = cf_grid  # Bottom-Right: Combined Flip

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()