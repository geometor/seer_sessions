"""
The transformation downscales the input grid by a factor of 2 along both height
and width. It preserves the colors 2, 3, and 5, placing them in the output grid
at locations corresponding to the downscaled coordinates of their presence in
the input grid.  If multiple pixels of the same color map to the same output
location, the color is preserved. It appears that the downscaling is object based
but the object centroid is not the determining placement factor.  Instead,
it seems that the downscaled coordinates of all input pixels are calculated, and if
a color is present at a downscaled location (even from multiple source pixels),
it is placed in the output.
"""

import numpy as np

def get_objects(grid, colors_to_keep):
    """
    Identifies contiguous regions (objects) of specified colors in the grid.
    Returns a dictionary where keys are colors and values are lists of 
    coordinates representing the object's pixels.
    """
    objects = {color: [] for color in colors_to_keep}
    visited = set()

    def is_valid(row, col):
        return 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]

    def dfs(row, col, color):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return
        visited.add((row, col))
        objects[color].append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, color)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color in colors_to_keep and (row, col) not in visited:
                dfs(row, col, color)
    return objects

def calculate_output_size(input_grid):
    """Calculate output size by dividing input dimensions by 2."""
    in_h, in_w = input_grid.shape
    out_h = int(np.ceil(in_h / 2.0))  # Use ceil to handle odd dimensions
    out_w = int(np.ceil(in_w / 2.0))
    return (out_h, out_w)

def transform(input_grid):
    # Determine relevant colors (from training examples)
    colors_to_keep = [0, 2, 3, 5]

    # Identify Objects (contiguous regions of color)
    objects = get_objects(input_grid, colors_to_keep)

    # Get output grid shape and ratios
    output_size = calculate_output_size(input_grid)

    # initialize output grid
    output_grid = np.zeros(output_size, dtype=int)

    # Downscale and copy objects
    for color, pixels in objects.items():
        for row, col in pixels:
            # Calculate corresponding output coordinates
            out_row = int(row / 2.0)
            out_col = int(col / 2.0)

            # Copy pixel to output grid if within bounds
            if 0 <= out_row < output_grid.shape[0] and 0 <= out_col < output_grid.shape[1]:
                output_grid[out_row, out_col] = color

    return output_grid