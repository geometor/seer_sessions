"""
The transformation takes an input grid of size N x M and produces an output grid of size 2N x 2M. 
The output grid is composed of four quadrants, each the size of the input grid.
- The top-left quadrant is a copy of the original input grid.
- The top-right quadrant is the input grid rotated 90 degrees clockwise.
- The bottom-left quadrant is the input grid rotated 90 degrees counter-clockwise.
- The bottom-right quadrant is the input grid rotated 180 degrees.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of the input grid and its rotations.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists of integers.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    n, m = input_np.shape
    
    # Create the output grid with double the dimensions, initialized with zeros
    output_grid = np.zeros((2 * n, 2 * m), dtype=int)
    
    # Calculate the rotated versions of the input grid
    # Note: np.rot90 rotates counter-clockwise by default
    original = input_np                                   # 0 degrees rotation
    rotated_90_cw = np.rot90(input_np, k=-1)             # 90 degrees clockwise (k=-1 or k=3)
    rotated_90_ccw = np.rot90(input_np, k=1)            # 90 degrees counter-clockwise (k=1)
    rotated_180 = np.rot90(input_np, k=2)               # 180 degrees rotation (k=2)
    
    # Place the original and rotated grids into the four quadrants of the output grid
    
    # Top-left quadrant: original input grid
    output_grid[0:n, 0:m] = original
    
    # Top-right quadrant: input grid rotated 90 degrees clockwise
    output_grid[0:n, m:2*m] = rotated_90_cw
    
    # Bottom-left quadrant: input grid rotated 90 degrees counter-clockwise
    output_grid[n:2*n, 0:m] = rotated_90_ccw
    
    # Bottom-right quadrant: input grid rotated 180 degrees
    output_grid[n:2*n, m:2*m] = rotated_180
    
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()