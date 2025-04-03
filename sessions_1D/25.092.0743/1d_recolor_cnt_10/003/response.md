```python
"""
Recolors contiguous horizontal blocks of magenta pixels (6) in a single-row 
(1xN) input grid based on their length. Blocks of length 1 become yellow (4), 
length 2 become azure (8), and length 3 become red (2). Other pixels, 
including the white (0) background, remain unchanged.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by recoloring magenta blocks based on length.

    Args:
        input_grid (np.ndarray): A 2D NumPy array of shape (1, N) 
                                 representing the input grid.

    Returns:
        np.ndarray: A 2D NumPy array of shape (1, N) representing the 
                    transformed grid.
    """
    # Ensure input is a 2D NumPy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
        raise TypeError("Input grid must be a 2D NumPy array.")
    
    # Expecting a single row grid
    if input_grid.shape[0] != 1:
         # Handle potential multi-row case gracefully if needed, 
         # but based on examples, assume 1 row.
         # For now, let's just copy and process the first row if multiple exist,
         # or raise an error if that's inappropriate.
         # Sticking to the observed pattern: assume input is always (1, N).
         pass # Assume correct input shape based on ARC examples

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Get the dimensions (height should be 1, width is N)
    height, width = output_grid.shape
    
    # Define the color mapping based on block length
    # length -> output_color_code
    color_map = {
        1: 4,  # yellow
        2: 8,  # azure
        3: 2   # red
    }
    
    # Define the target color to look for and modify
    target_color = 6 # magenta

    # Iterate through the columns of the single row
    c = 0 # current column index
    while c < width:
        # Check if the current pixel is the target color
        if output_grid[0, c] == target_color:
            # Found the start of a potential block
            start_col = c
            
            # Find the end of the contiguous block of the target color
            j = c
            while j < width and output_grid[0, j] == target_color:
                j += 1
            end_col = j # end_col is the index *after* the last target pixel
            
            # Calculate the length of the block
            block_length = end_col - start_col
            
            # Determine the output color based on the block length using the map
            # Use .get() with target_color as default if length not in map
            output_color = color_map.get(block_length, target_color) 
            
            # Recolor the block in the output grid using slicing
            output_grid[0, start_col:end_col] = output_color
                
            # Move the main index past the processed block
            c = end_col 
        else:
            # Move to the next pixel if it's not the target color
            c += 1
            
    return output_grid
```