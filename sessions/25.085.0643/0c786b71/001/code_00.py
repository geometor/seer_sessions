"""
Create a larger grid by arranging four transformed versions of the input grid.
The output grid's dimensions are double the input grid's dimensions (2H x 2W).
The output grid is composed of four quadrants, each the size of the input grid (H x W).
- Top-Left Quadrant: Input grid flipped horizontally and vertically.
- Top-Right Quadrant: Input grid flipped vertically.
- Bottom-Left Quadrant: Input grid flipped horizontally.
- Bottom-Right Quadrant: The original input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 tiled grid of flipped versions.
    
    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.
        
    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it's not already
    input_grid = np.array(input_grid)
    
    # Get the dimensions of the input grid
    H, W = input_grid.shape

    # Create the four transformed versions of the input grid
    original = input_grid
    flipped_h = np.fliplr(input_grid)  # Flipped horizontally (left-to-right)
    flipped_v = np.flipud(input_grid)  # Flipped vertically (top-to-bottom)
    flipped_hv = np.fliplr(np.flipud(input_grid)) # Flipped both horizontally and vertically

    # Initialize the output grid with dimensions 2H x 2W
    # Use the same dtype as the input grid to preserve color values
    output_grid = np.zeros((2 * H, 2 * W), dtype=input_grid.dtype)

    # Assemble the output grid by placing the transformed grids into the four quadrants
    # Top-left quadrant: flipped_hv
    output_grid[0:H, 0:W] = flipped_hv
    
    # Top-right quadrant: flipped_v
    output_grid[0:H, W:2*W] = flipped_v
    
    # Bottom-left quadrant: flipped_h
    output_grid[H:2*H, 0:W] = flipped_h
    
    # Bottom-right quadrant: original
    output_grid[H:2*H, W:2*W] = original

    return output_grid
