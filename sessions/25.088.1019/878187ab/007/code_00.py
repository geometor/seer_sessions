import numpy as np

"""
Transforms an input grid into an output grid with a fixed size (16x16).
The output grid is initially filled with the background color (orange/7).
If the input grid contains any pixels other than the background color, a specific predefined pattern is placed onto the output grid starting at row 11, column 0.
The pattern selected depends on the maximum color value found among the non-background pixels in the input grid.
Known patterns exist for max color 8 (a 5x10 pattern using red/2 and yellow/4) and max color 5 (a 5x7 pattern using red/2 and yellow/4).
If the input grid contains only the background color, the output grid remains entirely filled with the background color.
"""

# --- Constants ---
BACKGROUND_COLOR = 7  # Orange
OUTPUT_HEIGHT = 16    # Fixed height for the output grid
OUTPUT_WIDTH = 16     # Fixed width for the output grid
PATTERN_START_ROW = 11 # Row index where patterns are placed
PATTERN_START_COL = 0  # Column index where patterns are placed

# --- Predefined Patterns ---
# Store patterns associated with the maximum non-background color found in the input.
# Keys are the max_color, values are the numpy arrays representing the patterns.
KNOWN_PATTERNS = {
    8: np.array([ # Pattern for max_color = 8 (Azure)
        [2, 2, 2, 2, 4, 4, 2, 2, 2, 2],
        [2, 2, 2, 4, 2, 2, 4, 2, 2, 2],
        [2, 2, 4, 2, 2, 2, 2, 4, 2, 2],
        [2, 4, 2, 2, 2, 2, 2, 2, 4, 2],
        [4, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    ], dtype=int),
    5: np.array([ # Pattern for max_color = 5 (Gray)
        [2, 2, 4, 2, 4, 2, 2],
        [2, 2, 2, 4, 2, 2, 2],
        [2, 2, 4, 2, 4, 2, 2],
        [2, 4, 2, 2, 2, 4, 2],
        [4, 2, 2, 2, 2, 2, 4]
    ], dtype=int)
    # Add other patterns here if more examples reveal them
}

def transform(input_grid):
    """
    Applies the transformation rule based on non-background pixels and their max color.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # Step 1 & 2: Create an output grid with fixed size (16x16) and fill with background color
    output_grid = np.full((OUTPUT_HEIGHT, OUTPUT_WIDTH), BACKGROUND_COLOR, dtype=int)

    # Step 3: Examine the input grid for non-background pixels
    non_background_mask = input_np != BACKGROUND_COLOR

    # Step 4: Check if any non-background pixels exist
    if np.any(non_background_mask):
        # Step 4a & 4b: Identify non-background pixels and find the maximum color
        non_background_colors = input_np[non_background_mask]
        max_color = np.max(non_background_colors)

        # Step 4c: Check if a predefined pattern exists for this max_color
        if max_color in KNOWN_PATTERNS:
            # Select the appropriate pattern
            selected_pattern = KNOWN_PATTERNS[max_color]
            pattern_height, pattern_width = selected_pattern.shape

            # Step 4d: Calculate the end row and column indices for placing the pattern
            # Ensure placement is within the defined starting position
            end_row = PATTERN_START_ROW + pattern_height
            end_col = PATTERN_START_COL + pattern_width

            # Ensure the pattern placement fits within the output grid bounds
            # The output grid is 16x16. Patterns start at row 11.
            # Max pattern height is 5, so end_row is 11+5=16.
            # Max pattern width is 10, starting at col 0, so end_col is 10.
            # Both fit within the 16x16 grid.
            if end_row <= OUTPUT_HEIGHT and end_col <= OUTPUT_WIDTH:
                 # Overwrite the corresponding area in the output grid with the selected pattern
                output_grid[PATTERN_START_ROW:end_row, PATTERN_START_COL:end_col] = selected_pattern
            # else: # Optional handling if pattern exceeds bounds, not needed for current examples
            #    pass

        # else: # Optional handling if max_color doesn't have a known pattern
        #    pass # Output grid remains background-filled in the pattern area

    # Step 5: If no non-background pixels were found, the grid remains filled with BACKGROUND_COLOR (no action needed)

    # Step 6: Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
