```python
import numpy as np
from scipy.ndimage import label
import math

"""
Transformation Rule:

1. Identify all distinct connected objects composed of red pixels (color 2).
2. For each red object:
    a. Calculate its size 'L' (number of pixels).
    b. Determine a maximum Manhattan distance threshold 'k' using the formula: k = floor((L - 1) / 2).
    c. For every white pixel (color 0) in the grid, calculate its minimum Manhattan distance to any pixel within the current red object.
    d. If this minimum distance is greater than 0 and less than or equal to 'k', change the white pixel's color to azure (color 8).
3. Keep the original red pixels unchanged. Process each red object independently, updating the grid progressively.
"""

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (tuples or lists)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    For each red object, calculates a size-dependent Manhattan distance threshold 'k'.
    Colors white pixels azure if their minimum distance to that red object is > 0 and <= k.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Define colors
    red_color = 2
    white_color = 0
    azure_color = 8

    # Find connected components (objects) of red pixels.
    # Use 8-connectivity (diagonals included) by default.
    # structure = np.array([[1,1,1], [1,1,1], [1,1,1]]) # Explicit 8-connectivity
    # labeled_array, num_features = label(input_grid == red_color, structure=structure)
    # Default connectivity for label is sufficient here (usually type 2 which is 8-connectivity for 2D)
    labeled_array, num_features = label(input_grid == red_color)

    # If no red objects are found, return the original grid copy
    if num_features == 0:
        return output_grid

    # Iterate through each identified red object (labels are 1-based)
    for i in range(1, num_features + 1):
        # Get the coordinates of all pixels belonging to the current object
        object_pixels = np.argwhere(labeled_array == i)
        
        # Skip if somehow an empty object was labeled (shouldn't happen)
        if len(object_pixels) == 0: 
            continue

        # Calculate the size 'L' of the object
        L = len(object_pixels)
        
        # Calculate the Manhattan distance threshold 'k'
        k = math.floor((L - 1) / 2)

        # If k is less than 1, no azure pixels need to be added for this object
        if k < 1:
            continue

        # Iterate through every pixel in the grid
        for r in range(height):
            for c in range(width):
                # Check if the pixel in the *current state* of the output grid is white
                if output_grid[r, c] == white_color:
                    current_pos = (r, c)
                    min_dist = float('inf')
                    
                    # Calculate the minimum Manhattan distance from the current white pixel
                    # to any pixel within the *current* red object
                    for obj_pixel_coords in object_pixels:
                        # np.argwhere returns [row, col], compatible with manhattan_distance helper
                        dist = manhattan_distance(current_pos, obj_pixel_coords)
                        min_dist = min(min_dist, dist)
                        # Optimization: if min_dist becomes 1, we know it's the minimum possible > 0
                        # but k could be large, so finding the exact minimum is needed.
                        
                    # If the minimum distance is within the calculated threshold (and > 0),
                    # change the pixel color to azure in the output grid.
                    # Note: Check is > 0 to avoid coloring the object pixels themselves if they were somehow white.
                    if 0 < min_dist <= k:
                        output_grid[r, c] = azure_color

    # Return the modified grid
    return output_grid
```