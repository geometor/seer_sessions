```python
import numpy as np
from collections import defaultdict

"""
Identifies a reflection axis (blue line: 1) which can be horizontal, vertical, or diagonal (y=-x+k).
Finds all distinct objects (contiguous pixels of colors other than background (azure: 8) or axis (blue: 1)).
Counts the total number of pixels for each object color.
Selects the object color with the minimum total pixel count. If there's a tie, the color with the lower numerical value is chosen.
Reflects all pixels of the selected minimum-count color across the identified axis.
The reflection is drawn onto the output grid only if the target pixel is the background color (azure: 8).
The final output grid contains the original input grid elements plus the newly drawn reflected pixels.
"""

def transform(input_grid):
    """
    Applies a reflection transformation based on the object color with the minimum pixel count.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    axis_color = 1
    bg_color = 8

    # --- 1. Find the reflection axis ---
    # Locate all pixels belonging to the axis color
    axis_pixels = np.argwhere(input_grid == axis_color)
    
    # If no axis pixels are found, return the original grid
    if not axis_pixels.size > 0:
        return output_grid

    axis_type = None
    axis_param = None # Stores the constant value (row index, col index, r+c sum, or r-c diff)

    # Determine axis orientation based on the coordinates of axis pixels
    # Check for horizontal line (all axis pixels have the same row index)
    if len(np.unique(axis_pixels[:, 0])) == 1:
        axis_type = 'h'
        axis_param = axis_pixels[0, 0] # The constant row index
    # Check for vertical line (all axis pixels have the same column index)
    elif len(np.unique(axis_pixels[:, 1])) == 1:
        axis_type = 'v'
        axis_param = axis_pixels[0, 1] # The constant column index
    # Check for diagonal line y = -x + k (all axis pixels have the same r + c sum)
    elif len(np.unique(axis_pixels[:, 0] + axis_pixels[:, 1])) == 1:
        axis_type = 'd1' # Represents y = -x + k type diagonal
        axis_param = axis_pixels[0, 0] + axis_pixels[0, 1] # The constant sum k
    # Check for diagonal line y = x + k (all axis pixels have the same r - c difference)
    elif len(np.unique(axis_pixels[:, 0] - axis_pixels[:, 1])) == 1:
        axis_type = 'd2' # Represents y = x + k type diagonal
        axis_param = axis_pixels[0, 0] - axis_pixels[0, 1] # The constant difference k

    # If the axis doesn't fit one of the simple line types, return original grid
    if axis_type is None:
         # This handles cases where the blue pixels don't form a clear straight line
         # or form a different kind of shape.
         return output_grid

    # --- 2. Find objects and count pixels per color ---
    # Use defaultdict to store lists of coordinates for each color
    object_pixels_by_color = defaultdict(list)
    # Use defaultdict to store pixel counts for each color
    pixel_counts_by_color = defaultdict(int)

    # Iterate through the grid to find object pixels
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            # Check if the pixel belongs to an object (not background or axis)
            if color != bg_color and color != axis_color:
                object_pixels_by_color[color].append((r, c))
                pixel_counts_by_color[color] += 1

    # If no objects are found, return the original grid
    if not object_pixels_by_color:
        return output_grid

    # --- 3. Find the color with the minimum pixel count ---
    min_count = float('inf')
    reflection_color = -1 # Initialize with an invalid color

    # Sort the colors found by their numerical value for deterministic tie-breaking
    sorted_colors = sorted(pixel_counts_by_color.keys())

    # Iterate through sorted colors to find the one with the minimum count
    for color in sorted_colors:
        count = pixel_counts_by_color[color]
        if count < min_count:
            min_count = count
            reflection_color = color

    # If no reflection color was selected (shouldn't happen if objects exist), return original
    if reflection_color == -1:
         return output_grid

    # --- 4. Identify pixels of the selected color to reflect ---
    pixels_to_reflect = object_pixels_by_color[reflection_color]

    # --- 5. Reflect each pixel and update output grid ---
    for r, c in pixels_to_reflect:
        r_reflected, c_reflected = -1, -1 # Initialize reflected coordinates as invalid

        # Calculate reflected coordinates based on the axis type and parameter
        if axis_type == 'h':
            # Reflect across horizontal line r = axis_param
            r_reflected = 2 * axis_param - r
            c_reflected = c
        elif axis_type == 'v':
            # Reflect across vertical line c = axis_param
            r_reflected = r
            c_reflected = 2 * axis_param - c
        elif axis_type == 'd1': # axis r + c = k (axis_param)
            # Reflected point (r', c') = (k - c, k - r)
            r_reflected = axis_param - c
            c_reflected = axis_param - r
        elif axis_type == 'd2': # axis r - c = k (axis_param)
             # Reflected point (r', c') = (c + k, r - k)
             r_reflected = c + axis_param
             c_reflected = r - axis_param

        # --- 6. Update output grid if reflected point is valid and lands on background ---
        # Check if the calculated reflected coordinates are within the grid bounds
        if 0 <= r_reflected < rows and 0 <= c_reflected < cols:
            # Check if the target cell for the reflection is currently the background color
            # This prevents overwriting existing objects or the axis itself with the reflection.
            if output_grid[r_reflected, c_reflected] == bg_color:
                 output_grid[r_reflected, c_reflected] = reflection_color

    # Return the modified grid
    return output_grid
```