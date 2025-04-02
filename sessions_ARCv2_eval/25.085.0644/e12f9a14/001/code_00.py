"""
Transforms an input grid by identifying "source" pixels (colors other than azure 8 or green 3) 
and projecting their color outwards in the four cardinal directions (up, down, left, right) 
until the grid boundaries are reached. The projected colors overwrite existing pixels in the output grid.
The output grid starts as a copy of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the color projection transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid_np.copy()
    
    # Get grid dimensions
    height, width = input_grid_np.shape

    # Define background and container colors
    background_color = 8
    container_color = 3

    # Identify source pixels
    source_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            if color != background_color and color != container_color:
                source_pixels.append({'row': r, 'col': c, 'color': color})

    # Process each source pixel and project its color
    for source in source_pixels:
        r, c, color = source['row'], source['col'], source['color']

        # Project Up: Iterate from r-1 down to 0
        for row_idx in range(r - 1, -1, -1):
            output_grid[row_idx, c] = color

        # Project Down: Iterate from r+1 up to height-1
        for row_idx in range(r + 1, height):
            output_grid[row_idx, c] = color

        # Project Left: Iterate from c-1 down to 0
        for col_idx in range(c - 1, -1, -1):
            output_grid[r, col_idx] = color

        # Project Right: Iterate from c+1 up to width-1
        for col_idx in range(c + 1, width):
            output_grid[r, col_idx] = color
            
    # Return the modified output grid (converted back to list of lists if needed, though numpy array is often preferred)
    # Keeping it as a numpy array as per ARC conventions usually.
    return output_grid.tolist()
