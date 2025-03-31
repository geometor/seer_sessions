```python
import numpy as np

"""
Create a 3x3 blue frame around each gray pixel found in the input grid, preserving the gray pixel itself at the center of the frame. White pixels within the frame become blue, while other pixels (gray centers and background white outside frames) remain unchanged.
"""

def find_pixels_by_color(grid, color_value):
    """Finds all coordinates of pixels with a specific color."""
    coordinates = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_value:
                coordinates.append((r, c))
    return coordinates

def transform(input_grid):
    """
    Transforms the input grid by drawing a 3x3 blue frame around each gray pixel.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid
    # This preserves background white and the gray pixels initially
    output_grid = np.copy(input_np)
    
    # Define the color values
    GRAY = 5
    BLUE = 1
    
    # Find the coordinates of all gray pixels in the input grid
    gray_pixel_coords = find_pixels_by_color(input_np, GRAY)
    
    # Iterate through each found gray pixel coordinate
    for gr, gc in gray_pixel_coords:
        # Iterate through the 3x3 neighborhood centered at (gr, gc)
        for nr in range(gr - 1, gr + 2):
            for nc in range(gc - 1, gc + 2):
                # Check if the neighbor coordinate (nr, nc) is within the grid bounds
                is_within_bounds = (0 <= nr < height) and (0 <= nc < width)
                
                # Check if the neighbor coordinate is not the center gray pixel itself
                is_not_center = (nr != gr) or (nc != gc)
                
                # If the neighbor is within bounds and is not the center pixel,
                # set the corresponding pixel in the output grid to blue
                if is_within_bounds and is_not_center:
                    output_grid[nr, nc] = BLUE
                    
    return output_grid.tolist() # Return as list of lists as per common ARC format
```