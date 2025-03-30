import numpy as np

"""
Transformation Rule Natural Language Description:

1. Identify all pixels with the azure color (8) in the input grid.
2. Determine the bounding box of these azure pixels: find the minimum and maximum row indices (min_r, max_r) and minimum and maximum column indices (min_c, max_c).
3. Determine the vertical band (range of columns) to be filled: this band starts at min_c and extends up to and including the column index max_c + 1.
4. Find the fill color: search within the azure bounding box (rows min_r to max_r, columns min_c to max_c) for the first pixel whose color is not white (0) and not azure (8). This color will be used for filling.
5. Create the output grid by copying the input grid.
6. Iterate through each row of the grid. For each row, iterate through the columns within the determined fill band (from min_c to max_c + 1).
7. If the pixel at the current (row, column) in the *input* grid is white (0), change the color of the corresponding pixel in the *output* grid to the determined fill_color. Otherwise, keep the original color.
8. Return the modified output grid.
"""

def find_azure_coords(grid):
    """Finds the coordinates of all azure (8) pixels."""
    rows, cols = np.where(grid == 8)
    if len(rows) == 0:
        return None, None, None, None
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    return min_r, max_r, min_c, max_c

def find_fill_color_in_box(grid, min_r, max_r, min_c, max_c):
    """Finds the non-white, non-azure color within the specified bounding box."""
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            color = grid[r, c]
            if color != 0 and color != 8:
                return color
    # Fallback if no suitable color found within the box (shouldn't happen based on examples)
    return 0 # Or raise an error

def transform(input_grid):
    """
    Applies the transformation rule: fills a vertical band defined by azure pixels
    with a color found within the azure bounding box.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. & 2. Find azure pixels and their bounding box
    min_r, max_r, min_c, max_c = find_azure_coords(input_np)

    # Handle case where no azure pixels are found (return original grid)
    if min_r is None:
        return input_grid

    # 3. Determine fill columns
    # The band starts at min_c and goes up to and includes max_c + 1
    # The range function's end is exclusive, so we use max_c + 2
    # We must cap the end column index at the grid width
    start_col = min_c
    end_col = min(max_c + 2, width) # max_c + 1 is the last column index to potentially fill

    # 4. Find the fill color within the azure bounding box
    fill_color = find_fill_color_in_box(input_np, min_r, max_r, min_c, max_c)

    # 5. Output grid is already initialized as a copy

    # 6. & 7. Apply the fill
    for r in range(height):
        for c in range(start_col, end_col):
            # Check the original grid's color
            if input_np[r, c] == 0:
                # Modify the output grid
                output_np[r, c] = fill_color

    # 8. Return the result as a list of lists
    return output_np.tolist()