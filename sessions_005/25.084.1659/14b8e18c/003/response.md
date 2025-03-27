```python
import copy

"""
Transforms the input grid by changing specific orange (7) pixels to red (2).
An orange pixel at (r, c) is changed to red if it has exactly one non-orange neighbor 
(considering only the four cardinal neighbors: up, down, left, right). 
All other pixels retain their original color.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of list of int): The input grid representing colors.

    Returns:
        list of list of int: The transformed output grid.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of input_grid
    # This ensures that pixels not matching the condition retain their original color
    output_grid = copy.deepcopy(input_grid)

    # Define relevant colors
    background_color = 7 # orange
    target_color = 2     # red

    # Define neighbor offsets for cardinal directions (up, down, left, right)
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is the background color (orange)
            if input_grid[r][c] == background_color:
                
                # Count non-background neighbors in cardinal directions
                non_background_neighbor_count = 0
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is NOT the background color
                        if input_grid[nr][nc] != background_color:
                            non_background_neighbor_count += 1
                            
                # If exactly one non-background neighbor was found, change the pixel color
                if non_background_neighbor_count == 1:
                    output_grid[r][c] = target_color

    # Return the modified grid
    return output_grid
```