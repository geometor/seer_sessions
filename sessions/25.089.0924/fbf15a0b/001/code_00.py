import numpy as np

"""
Identify the locations of the two gray (5) marker pixels in the input grid.
Determine if the markers are aligned vertically (same column) or horizontally (same row).

If vertically aligned in column 'c':
  - Calculate the output height as half the input height (integer division).
  - If 'c' is the first column (index 0), remove the top 2 rows.
  - If 'c' is the last column, remove the top 1 row.
  - The output is the subgrid starting after the removed rows, with the calculated height, spanning all columns.

If horizontally aligned in row 'r':
  - Calculate the output width as half the input width (integer division).
  - If 'r' is the first row (index 0), remove the leftmost 2 columns. (Based on available examples)
  - The output is the subgrid starting after the removed columns, with the calculated width, spanning all rows.

Return the resulting cropped subgrid.
"""

def find_markers(grid_np, marker_color=5):
    """Finds the coordinates of the two marker pixels."""
    coords = np.argwhere(grid_np == marker_color)
    if len(coords) != 2:
        # This case shouldn't happen based on the problem description,
        # but good to handle defensively.
        raise ValueError(f"Expected exactly 2 marker pixels (color {marker_color}), found {len(coords)}")
    return tuple(coords[0]), tuple(coords[1])

def transform(input_grid):
    """
    Crops the input grid based on the location and alignment of two gray marker pixels.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    h, w = input_np.shape

    # 1. Identify the locations of the two gray (5) pixels
    (r1, c1), (r2, c2) = find_markers(input_np, 5)

    output_np = None

    # 2. Check alignment and apply cropping logic
    if c1 == c2:  # Vertical alignment
        # a. Calculate target output height
        output_height = h // 2
        shared_col = c1
        start_row = 0

        # b. Determine rows to remove from top
        if shared_col == 0: # Markers in the first column
            start_row = 2
        elif shared_col == w - 1: # Markers in the last column
             start_row = 1
        else:
            # Undefined behavior based on examples, assume default or raise error
            # Let's assume start_row 1 for any other vertical case for now,
            # but this might need refinement if new examples appear.
             start_row = 1 # Placeholder assumption

        # c. Crop the grid
        output_np = input_np[start_row : start_row + output_height, :]

    elif r1 == r2:  # Horizontal alignment
        # a. Calculate target output width
        output_width = w // 2
        shared_row = r1
        start_col = 0

        # b. Determine columns to remove from left
        if shared_row == 0: # Markers in the first row
            start_col = 2
        # Based on only one horizontal example, we only have the r=0 case.
        # Need more examples to generalize behavior for markers in other rows.
        # Let's assume start_col 1 for other horizontal cases for now.
        # elif shared_row == h - 1: # Hypothetical last row case
        #     start_col = 1 # Placeholder assumption
        else:
             start_col = 1 # Placeholder assumption

        # c. Crop the grid
        output_np = input_np[:, start_col : start_col + output_width]

    else:
        # Markers are not aligned vertically or horizontally.
        # This case is not covered by the examples.
        # Returning the input unchanged or raising an error might be options.
        # Let's raise an error for clarity.
        raise ValueError("Marker pixels are not aligned vertically or horizontally.")

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid