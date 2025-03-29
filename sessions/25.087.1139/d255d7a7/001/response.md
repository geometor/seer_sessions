```python
import numpy as np

"""
Identifies the cluster of non-background (non-orange/7) pixels in the input grid.
Determines the primary edge this cluster is located against (bottom, top, right, or left, prioritized in that order).
Moves the entire cluster (preserving its internal structure) to the corresponding opposite edge of the grid.
The output grid is initialized with the background color, and then the moved cluster's pixels are placed onto it.

Example:
- If the cluster is primarily against the left edge, it's moved to the right edge.
- If the cluster is primarily against the bottom edge, it's moved to the top edge.

The cluster is defined by all pixels that are not orange (7).
The movement is calculated based on the bounding box of the cluster.
"""

def transform(input_grid):
    """
    Moves a cluster of non-background pixels from one edge to the opposite edge.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    input_arr = np.array(input_grid, dtype=int)
    H, W = input_arr.shape
    background_color = 7

    # Find coordinates of all non-background pixels
    object_pixels_coords = list(zip(*np.where(input_arr != background_color)))

    # If there are no object pixels, return the original grid
    if not object_pixels_coords:
        return input_grid

    # Determine the bounding box of the object pixels
    rows, cols = zip(*object_pixels_coords)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Determine edge affiliation
    is_left = (min_c == 0)
    is_right = (max_c == W - 1)
    is_top = (min_r == 0)
    is_bottom = (max_r == H - 1)

    # Calculate the translation vector (dr, dc) based on edge priority: Bottom > Top > Right > Left
    dr, dc = 0, 0
    if is_bottom and not is_top:
        # Move to top edge
        dr = 0 - min_r  # Target min_r is 0
    elif is_top and not is_bottom:
        # Move to bottom edge
        dr = (H - 1) - max_r # Target max_r is H - 1
    elif is_right and not is_left:
        # Move to left edge
        dc = 0 - min_c  # Target min_c is 0
    elif is_left and not is_right:
        # Move to right edge
        dc = (W - 1) - max_c # Target max_c is W - 1
    # else: handles cases touching opposite sides, fully contained, or corners where priority doesn't select one edge.
    # In these cases, dr, dc remain 0, effectively no move according to this logic.

    # Initialize the output grid with the background color
    output_arr = np.full((H, W), background_color, dtype=int)

    # Copy the object pixels to their new locations
    for r, c in object_pixels_coords:
        color = input_arr[r, c]
        nr, nc = r + dr, c + dc

        # Ensure the new coordinates are within the grid bounds
        if 0 <= nr < H and 0 <= nc < W:
            output_arr[nr, nc] = color

    # Convert back to list of lists for the expected output format
    return output_arr.tolist()
```