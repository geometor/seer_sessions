import numpy as np

"""
Transforms an input grid based on a defined pattern and layout.

The input grid is conceptually divided into two parts by a gray separator line:
1. A 6x6 top-left area (rows 0-5, cols 0-5) defining a source pattern. This area consists of 2x2 blocks of color.
2. A layout area below the separator (starting from row 7), conceptually 6x6, containing red markers (color 2) on a background (color 0).

The transformation proceeds as follows:
1. Derive a 3x3 pattern from the 6x6 source area by taking the top-left color of each 2x2 block.
2. Initialize an 18x18 output grid with the background color (0).
3. Read the conceptual 6x6 layout area from the input grid (rows 7 onwards, cols 0-5, padded with 0s if input is smaller).
4. For each red marker (color 2) found at relative coordinates (r, c) in the layout area (0<=r<6, 0<=c<6):
   a. Calculate the target top-left coordinates in the 18x18 output grid as (R, C) = (r * 3, c * 3).
   b. Copy ("stamp") the derived 3x3 pattern onto the output grid starting at (R, C).
5. Return the final 18x18 output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described pattern stamping transformation to the input grid.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the 18x18 output grid.
    """

    # 1. Initialize an empty 18x18 output grid with the background color (white, 0).
    output_grid = np.zeros((18, 18), dtype=int)

    # 2. Identify the 6x6 pattern definition area and derive the 3x3 pattern.
    pattern_definition_area = input_grid[0:6, 0:6]
    pattern_grid = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            # Take the color of the top-left cell of the 2x2 block
            pattern_grid[i, j] = pattern_definition_area[i * 2, j * 2]

    # 3. Identify the conceptual 6x6 layout area.
    input_height, input_width = input_grid.shape
    layout_grid = np.zeros((6, 6), dtype=int)
    layout_start_row = 7 # Row index below the gray separator

    for r in range(6): # Relative row in layout
        for c in range(6): # Relative col in layout (always 0-5)
            input_r = layout_start_row + r
            input_c = c
            # Check if the coordinates are within the input grid bounds
            if input_r < input_height and input_c < input_width:
                 layout_grid[r, c] = input_grid[input_r, input_c]
            # Otherwise, it remains 0 (background) due to initialization

    # 4. Iterate through the layout grid and place the pattern in the output grid.
    for r in range(6): # Layout row index
        for c in range(6): # Layout col index
            # 5. Check if the layout cell contains the red marker (color 2).
            if layout_grid[r, c] == 2:
                # 6a. Calculate the top-left starting coordinates for the output grid.
                output_r = r * 3
                output_c = c * 3

                # 6b. Copy the 3x3 pattern onto the output grid.
                # Ensure slicing doesn't go out of bounds (though should not happen with 18x18 output)
                target_slice_r = slice(output_r, output_r + 3)
                target_slice_c = slice(output_c, output_c + 3)
                output_grid[target_slice_r, target_slice_c] = pattern_grid

    # 7. Return the final 18x18 output grid.
    return output_grid