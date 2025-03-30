import numpy as np

"""
Draw L-shaped lines from each non-white pixel to its two nearest cardinal edges.
The vertical segment extends from the pixel's row to the nearest horizontal edge (top or bottom).
The horizontal segment extends from the pixel's column to the nearest vertical edge (left or right).
If distances to opposite edges are equal, the top/left edge is chosen.
The lines inherit the color of the source pixel.
If multiple source pixels exist, their resulting L-shapes are overlaid on the output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by drawing L-shaped lines from each non-white pixel
    towards the two nearest cardinal edges.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape

    # Initialize the output grid with the background color (white, 0)
    output_array = np.zeros_like(input_array)

    # Find the coordinates and colors of all non-white source pixels
    source_pixels = []
    for r in range(H):
        for c in range(W):
            color = input_array[r, c]
            if color != 0:
                source_pixels.append(((r, c), color))

    # Process each source pixel
    for (r, c), color in source_pixels:
        # Determine the nearest horizontal edge (top or bottom)
        dist_top = r
        dist_bottom = H - 1 - r
        if dist_top <= dist_bottom:
            r_target = 0  # Target is the top edge
        else:
            r_target = H - 1 # Target is the bottom edge

        # Determine the nearest vertical edge (left or right)
        dist_left = c
        dist_right = W - 1 - c
        if dist_left <= dist_right:
            c_target = 0  # Target is the left edge
        else:
            c_target = W - 1 # Target is the right edge

        # Draw the vertical line segment in the output array
        # Ensure correct slicing regardless of whether r or r_target is smaller
        row_start = min(r, r_target)
        row_end = max(r, r_target)
        output_array[row_start : row_end + 1, c] = color

        # Draw the horizontal line segment in the output array
        # Ensure correct slicing regardless of whether c or c_target is smaller
        col_start = min(c, c_target)
        col_end = max(c, c_target)
        output_array[r, col_start : col_end + 1] = color

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid