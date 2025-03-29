```python
import numpy as np

"""
Transformation Rule:

1.  Identify all white (0) pixels in the input grid.
2.  For each white pixel, examine its 8 neighbors (horizontal, vertical, and diagonal).
3.  If any neighbor is an azure (8) pixel, change the white pixel to yellow (4) in the output grid.
4.  All other pixels (including the original azure pixels and white pixels not adjacent to azure) retain their original color.
5.  The output grid has the same dimensions as the input grid.
"""

def transform(input_grid):
    """
    Applies a transformation to the input grid where white pixels adjacent (8-connectivity)
    to azure pixels are changed to yellow.

    Args:
        input_grid (list of lists or np.array): The input grid containing integer color codes.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Get the dimensions of the grid
    height, width = input_np.shape
    
    # Define the 8 neighbor offsets (including diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    
    # Define the colors involved
    background_color = 0  # white
    primary_object_color = 8  # azure
    added_object_color = 4  # yellow

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is the background color
            if input_np[r, c] == background_color:
                # Check its 8 neighbors
                found_primary_neighbor = False
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is the primary object color
                        if input_np[nr, nc] == primary_object_color:
                            found_primary_neighbor = True
                            break # Stop checking neighbors once one is found
                            
                # If a primary object color neighbor was found, change the cell in the output grid
                if found_primary_neighbor:
                    output_grid[r, c] = added_object_color

    return output_grid.tolist() # Return as list of lists if needed, or keep as np.array

```