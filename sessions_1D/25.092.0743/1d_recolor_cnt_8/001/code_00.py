import numpy as np

"""
This program transforms a 1D input grid containing white (0) and gray (5) pixels.
It identifies contiguous blocks of gray pixels.
Based on the length of each gray block, it replaces the block with a new color:
- Length 1: Replaced with maroon (9)
- Length 2: Replaced with green (3)
- Length 3: Replaced with blue (1)
White pixels remain unchanged.
"""

# Define the mapping from the length of a gray block to its replacement color
LENGTH_COLOR_MAP = {
    1: 9,  # Maroon
    2: 3,  # Green
    3: 1   # Blue
}

# Define the colors involved
GRAY = 5
WHITE = 0

def transform(input_grid):
    """
    Transforms the input grid by replacing contiguous blocks of gray pixels
    based on their length.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.
                                     Expected to have only one row based on examples.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert input to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Initialize the output grid as a copy of the input grid.
    # White pixels (0) are already correct in the copy.
    output_grid = grid.copy()

    # Get the dimensions (assuming 1 row based on examples)
    rows, cols = grid.shape
    if rows != 1:
        # This solution assumes a single row grid as per the examples.
        # Handle multi-row grids differently if needed, maybe raise an error.
        print("Warning: Expected a 1-row grid, received {} rows.".format(rows))
        # For now, proceed focusing on the first row if multiple exist, or fail if 0 rows.
        if rows == 0:
            return [] # Return empty for empty input

    # Iterate through the columns of the single row
    col = 0
    while col < cols:
        # Check if the current pixel is gray
        if grid[0, col] == GRAY:
            # Found the start of a potential gray block
            start_col = col
            block_length = 0
            # Measure the length of the contiguous gray block
            while col < cols and grid[0, col] == GRAY:
                block_length += 1
                col += 1
            # The block ends at the current 'col' index (exclusive)

            # Determine the replacement color using the map.
            # Use .get() with a default value (e.g., original GRAY color)
            # in case a block length not in the map is encountered.
            replacement_color = LENGTH_COLOR_MAP.get(block_length, GRAY)

            # Fill the corresponding segment in the output grid with the replacement color
            output_grid[0, start_col:col] = replacement_color

            # 'col' is already advanced past the processed block by the inner while loop
        else:
            # If the pixel is not gray (it must be white based on examples),
            # simply move to the next column.
            col += 1

    # Convert the NumPy array back to a list of lists for the final output
    return output_grid.tolist()