```python
import numpy as np

"""
Expands isolated single non-white pixels in a 1D horizontal grid into horizontal 1x3 blocks of the same color.

The transformation identifies non-white pixels (color != 0) in the input grid. 
For each such pixel, it checks its immediate horizontal neighbors (left and right). 
If both neighbors are white (color == 0) or are outside the grid boundaries, the pixel is considered 'isolated'.
Each isolated pixel in the input is expanded into a 1x3 block of its original color in the output grid. 
This 1x3 block is centered at the original pixel's column position. 
Pixels that are not isolated (i.e., part of a larger horizontal structure or background pixels) are copied directly from the input to the output grid without modification.
Grid boundaries are respected; the expansion does not go beyond the grid's width.
"""

def is_white_or_boundary(grid, r, c):
    """Checks if the cell at (r, c) is white (0) or outside grid boundaries."""
    height, width = grid.shape
    if r < 0 or r >= height or c < 0 or c >= width:
        return True  # Treat boundary as white
    return grid[r, c] == 0

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by expanding isolated non-white pixels into 1x3 blocks.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input_grid
    # This handles the background and non-isolated pixels automatically
    output_grid = np.copy(input_grid)

    # Iterate through each cell in the grid (though height is always 1 here)
    for r in range(height): # Loop will run only for r=0
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_grid[r, c]

            # Check if the pixel is non-white
            if pixel_color != 0:
                # Check if the pixel is isolated horizontally
                is_left_neighbor_white = is_white_or_boundary(input_grid, r, c - 1)
                is_right_neighbor_white = is_white_or_boundary(input_grid, r, c + 1)

                if is_left_neighbor_white and is_right_neighbor_white:
                    # This is an isolated pixel, expand it in the output grid
                    
                    # Set the center pixel (already done by copy, but explicit)
                    output_grid[r, c] = pixel_color
                    
                    # Set the left pixel if within bounds
                    if c > 0:
                        output_grid[r, c - 1] = pixel_color
                        
                    # Set the right pixel if within bounds
                    if c < width - 1:
                        output_grid[r, c + 1] = pixel_color

    return output_grid.tolist() # Return as list of lists per ARC standard format

```