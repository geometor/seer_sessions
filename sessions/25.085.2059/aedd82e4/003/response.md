```python
"""
Iterate through each pixel in the input grid. If a pixel's color is red (2), 
check its 4 cardinal neighbors (up, down, left, right). If none of the 
existing cardinal neighbors are also red (2), change the pixel's color to 
blue (1) in the output grid. Otherwise, keep the original color. The output 
grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing red pixels to blue if they have no 
    adjacent (cardinal direction) red neighbors.
    
    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Define neighbor offsets (4 cardinal directions: up, down, left, right)
    neighbor_offsets = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is red (2)
            if input_np[r, c] == 2:
                has_adjacent_red = False # Assume no adjacent red neighbors initially
                
                # Check the 4 cardinal neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # If a cardinal neighbor exists and is red (2)
                        if input_np[nr, nc] == 2:
                            has_adjacent_red = True
                            break # Found an adjacent red neighbor, no need to check others
                
                # If the pixel is red and has NO adjacent red neighbors
                if not has_adjacent_red:
                    # Change the color of the pixel to blue (1) in the output grid
                    output_grid[r, c] = 1
            
            # If the pixel is not red, or it's red but has an adjacent red neighbor, 
            # its color remains unchanged (already handled by copying the input)

    # Return as list of lists as per ARC standard
    return output_grid.tolist() 
```