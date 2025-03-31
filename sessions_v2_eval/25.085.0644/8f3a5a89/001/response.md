```python
import numpy as np

"""
Transforms an input grid by changing azure (8) pixels to orange (7) if they are adjacent (horizontally, vertically, or diagonally) to any blue (1) or magenta (6) pixels in the input grid. Other pixels retain their original color.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Define the offsets for the 8 neighbors (including diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is azure (8)
            if input_grid_np[r, c] == 8:
                # Check if any neighbor is blue (1) or magenta (6)
                found_trigger_neighbor = False
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_grid_np[nr, nc]
                        # Check if the neighbor color is a trigger color
                        if neighbor_color == 1 or neighbor_color == 6:
                            found_trigger_neighbor = True
                            break # No need to check other neighbors
                
                # If a trigger neighbor was found, change the pixel in the output grid to orange (7)
                if found_trigger_neighbor:
                    output_grid[r, c] = 7
            
            # If the pixel is not azure (8), or it is azure (8) but has no trigger neighbors,
            # its color in the output grid remains unchanged (already handled by the initial copy).

    # Convert back to list of lists if necessary for the environment
    return output_grid.tolist()
```