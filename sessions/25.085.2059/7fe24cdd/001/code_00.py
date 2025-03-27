"""
This module transforms an input grid into an output grid twice the height and width.
The output grid is composed of four quadrants, each containing a rotated version of the input grid:
- Top-Left: Input grid (0 degrees rotation).
- Top-Right: Input grid rotated 90 degrees clockwise.
- Bottom-Left: Input grid rotated 270 degrees clockwise (90 degrees counter-clockwise).
- Bottom-Right: Input grid rotated 180 degrees.
"""

import numpy as np

def rotate_grid(grid, degrees_clockwise):
    """Rotates a grid clockwise by a specified number of degrees (must be multiple of 90)."""
    if degrees_clockwise == 0:
        return grid
    elif degrees_clockwise == 90:
        # np.rot90 rotates counter-clockwise, k=1 is 90 deg CCW.
        # So k=-1 is 90 deg CW.
        return np.rot90(grid, k=-1)
    elif degrees_clockwise == 180:
        return np.rot90(grid, k=-2)
    elif degrees_clockwise == 270:
        return np.rot90(grid, k=-3) # Equivalent to k=1 (90 deg CCW)
    else:
        raise ValueError("Degrees must be 0, 90, 180, or 270")

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of rotated versions.
    
    Args:
        input_grid (list of lists or numpy array): The input grid.
        
    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Create a new output grid with dimensions 2H x 2W, initialized with zeros
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)
    
    # Calculate the rotated versions of the input grid
    rotated_90_cw = rotate_grid(input_np, 90)
    rotated_180 = rotate_grid(input_np, 180)
    rotated_270_cw = rotate_grid(input_np, 270) # Same as 90 deg counter-clockwise
    
    # Populate the Top-Left Quadrant (0 degrees rotation)
    output_grid[0:H, 0:W] = input_np
    
    # Populate the Top-Right Quadrant (90 degrees clockwise rotation)
    output_grid[0:H, W:2*W] = rotated_90_cw
    
    # Populate the Bottom-Left Quadrant (270 degrees clockwise rotation)
    output_grid[H:2*H, 0:W] = rotated_270_cw
    
    # Populate the Bottom-Right Quadrant (180 degrees rotation)
    output_grid[H:2*H, W:2*W] = rotated_180
    
    return output_grid
