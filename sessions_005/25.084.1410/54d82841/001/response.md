```python
"""
Identify U-shaped objects (3 pixels wide, 2 high, with a central gap in the bottom row) 
in the input grid. For each U-shape found, place a yellow pixel (4) in the last 
row of the output grid, directly below the central gap of the U-shape. 
The original grid content, including the U-shapes, remains unchanged in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the identified U-shapes.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input grid to a numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_np = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    last_row = height - 1

    # Iterate through each possible top-left corner (r, c) of a 3x2 bounding box
    # Need to stop at height-2 for rows and width-3 for columns to fit the 3x2 shape
    for r in range(height - 1):
        for c in range(width - 2):
            # Extract the potential 3x2 area
            # Check coordinates:
            # (r, c),   (r, c+1),   (r, c+2)
            # (r+1, c), (r+1, c+1), (r+1, c+2)

            # Check if the pattern forms a U-shape
            # 1. Get the potential color of the U-shape from the top-left pixel
            u_color = input_np[r, c]

            # 2. Skip if the top-left is white (background)
            if u_color == 0:
                continue

            # 3. Check if the surrounding pixels match the U-shape color
            is_u_shape_color = (
                input_np[r, c+1] == u_color and
                input_np[r, c+2] == u_color and
                input_np[r+1, c] == u_color and
                input_np[r+1, c+2] == u_color
            )

            # 4. Check if the central gap pixel is white
            is_gap_white = (input_np[r+1, c+1] == 0)

            # 5. If both conditions are met, it's a U-shape
            if is_u_shape_color and is_gap_white:
                # Identify the column index of the central gap
                gap_col = c + 1
                
                # Place a yellow pixel (4) in the output grid at (last_row, gap_col)
                # Ensure the column index is within bounds (though it should be by loop definition)
                if 0 <= gap_col < width:
                    output_np[last_row, gap_col] = 4

    # Convert the numpy array back to a list of lists for the return value
    return output_np.tolist()

```