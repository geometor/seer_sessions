```python
import numpy as np

"""
The transformation completes a symmetrical pattern within the grid.
1. Identify all non-white (non-zero color) pixels in the input grid.
2. If no non-white pixels exist, return the input grid unchanged.
3. Determine the bounding box containing all non-white pixels (minimum and maximum row and column indices).
4. Calculate the symmetry center based on the bounding box. The reflection calculations use the sum of the min and max coordinates for each axis (center_sum_r = min_r + max_r, center_sum_c = min_c + max_c).
5. Create a copy of the input grid to serve as the output grid.
6. For each non-white pixel (r, c) with color clr in the input grid:
    a. Calculate the coordinates of its reflection across the horizontal axis of symmetry: (center_sum_r - r, c).
    b. Calculate the coordinates of its reflection across the vertical axis of symmetry: (r, center_sum_c - c).
    c. Calculate the coordinates of its reflection through the center point: (center_sum_r - r, center_sum_c - c).
7. For each calculated reflected coordinate that falls within the grid boundaries, set the pixel at that coordinate in the output grid to the color clr of the original pixel. This ensures that the original pixel and all its symmetrical counterparts exist and have the same color in the output.
8. Return the completed output grid.
"""

def transform(input_grid):
    """
    Completes a symmetrical pattern based on existing non-white pixels.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid with completed symmetry.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Find coordinates of all non-white pixels
    non_white_coords = np.argwhere(input_np > 0)

    # If there are no non-white pixels, return the original grid
    if non_white_coords.shape[0] == 0:
        return input_grid

    # Calculate the bounding box of non-white pixels
    min_r, min_c = non_white_coords.min(axis=0)
    max_r, max_c = non_white_coords.max(axis=0)

    # Calculate the sums needed for reflection calculations
    # reflected_row = min_r + max_r - original_row
    # reflected_col = min_c + max_c - original_col
    center_sum_r = min_r + max_r
    center_sum_c = min_c + max_c

    # Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)

    # Iterate through each non-white pixel found
    for r, c in non_white_coords:
        # Get the color of the current pixel
        clr = input_np[r, c]

        # Calculate potential reflected coordinates
        # Horizontal reflection (across center horizontal line)
        r_h = center_sum_r - r
        c_h = c
        # Vertical reflection (across center vertical line)
        r_v = r
        c_v = center_sum_c - c
        # Point reflection (through center)
        r_p = center_sum_r - r
        c_p = center_sum_c - c

        # Apply reflections to the output grid if coordinates are valid
        # Check bounds and update for horizontal reflection
        if 0 <= r_h < height and 0 <= c_h < width:
            output_np[r_h, c_h] = clr

        # Check bounds and update for vertical reflection
        if 0 <= r_v < height and 0 <= c_v < width:
            output_np[r_v, c_v] = clr

        # Check bounds and update for point reflection
        if 0 <= r_p < height and 0 <= c_p < width:
            output_np[r_p, c_p] = clr
            
        # Ensure the original pixel itself is present (redundant if iterating through input pixels, but safe)
        # output_np[r, c] = clr 

    # Convert the result back to a list of lists
    return output_np.tolist()

```