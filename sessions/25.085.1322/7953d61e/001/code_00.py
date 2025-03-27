import numpy as np

"""
The transformation constructs an output grid that is twice the height and twice the width of the input grid. 
The output grid is divided into four quadrants, each the size of the input grid.
- The top-left quadrant is an identical copy of the input grid.
- The top-right quadrant is the input grid transposed and then flipped vertically.
- The bottom-left quadrant is the input grid rotated 180 degrees.
- The bottom-right quadrant is the input grid rotated 90 degrees clockwise.
"""

def transform(input_grid):
    """
    Applies the described quadrant transformations to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get dimensions (not strictly needed if always 4x4 -> 8x8, but good practice)
    # H, W = input_np.shape 

    # 1. Calculate the four quadrants
    
    # Top-Left: Identity
    quadrant_tl = input_np 
    
    # Top-Right: Transpose then Flip Vertically (up-down)
    quadrant_tr = np.flipud(np.transpose(input_np))
    
    # Bottom-Left: Rotate 180 degrees
    quadrant_bl = np.rot90(input_np, k=2)
    
    # Bottom-Right: Rotate 90 degrees clockwise
    quadrant_br = np.rot90(input_np, k=-1) # k=-1 for clockwise

    # 2. Assemble the output grid
    
    # Stack top-left and top-right horizontally
    top_row = np.hstack((quadrant_tl, quadrant_tr))
    
    # Stack bottom-left and bottom-right horizontally
    bottom_row = np.hstack((quadrant_bl, quadrant_br))
    
    # Stack the top row and bottom row vertically
    output_np = np.vstack((top_row, bottom_row))

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
