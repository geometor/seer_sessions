import numpy as np

"""
Transformation Rule:
1. Identify the border color from the input grid's top-left corner (input_grid[0, 0]). Handle empty or invalid grids.
2. Initialize an output grid with the same dimensions as the input grid.
3. Iterate through each row `r` of the input grid (from index 0 to height-1).
4. For the current input row `r`:
    a. Check if this specific input row contains any Red pixels (color code 2).
    b. Determine the background color for the corresponding output row: use the identified border_color if Red pixels were present in the input row, otherwise use White (color code 0).
    c. Fill the entire output row `r` in the output grid with this determined background color.
    d. Iterate through each column `c` of the input row `r`.
    e. If the input pixel at `input_grid[r, c]` is not White (i.e., its value is not 0), copy the value from `input_grid[r, c]` to the corresponding position `output_grid[r, c]`, overwriting the background color set in step 4c.
5. Return the completed output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by setting the background color of each output row
    based on the presence of Red (2) pixels in the corresponding input row,
    and then overlaying all non-White pixels from the input onto the output.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Handle empty grid case
    if height == 0 or width == 0:
        return []

    # 1. Identify border color (assuming it's reliably at [0, 0])
    border_color = input_grid_np[0, 0]

    # 2. Initialize output grid
    output_grid = np.zeros_like(input_grid_np)

    # 3. Iterate through each row
    for r in range(height):
        # 4a. Check if the input row contains Red (2)
        input_row = input_grid_np[r, :]
        has_red = np.any(input_row == 2)

        # 4b. Determine background color for the output row
        row_bg_color = border_color if has_red else 0 # 0 is White

        # 4c. Fill the output row with the background color
        output_grid[r, :] = row_bg_color

        # 4d/4e. Iterate through columns and overlay non-White input pixels
        for c in range(width):
            if input_grid_np[r, c] != 0: # If not White
                output_grid[r, c] = input_grid_np[r, c] # Copy original pixel

    # 5. Return the output grid as a list of lists
    return output_grid.tolist()