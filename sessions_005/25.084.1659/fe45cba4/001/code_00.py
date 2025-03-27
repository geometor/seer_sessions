import numpy as np

def transform(input_grid):
    """
    Analyzes the input grid to determine if any red (2) pixels exist in the
    left half (columns 0-3).

    If red pixels exist in the left half:
        1. Copies all non-red pixels from the input to the output grid.
        2. Draws a 4x4 solid red (2) square in the bottom-right quadrant
           (rows 4-7, columns 4-7) of the output grid.

    If no red pixels exist in the left half:
        1. Copies all non-maroon (9) pixels from the input to the output grid.
        2. Draws a 3x4 solid maroon (9) rectangle in the top-right quadrant
           (rows 0-2, columns 4-7) of the output grid.

    The background color is assumed to be orange (7).
    """

    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    background_color = 7
    red_color = 2
    maroon_color = 9

    # Initialize output grid with the background color
    output_array = np.full_like(input_array, background_color)

    # Condition check: Check if any red pixel exists in columns 0-3
    red_in_left_half = False
    for r in range(rows):
        for c in range(min(cols, 4)): # Check columns 0, 1, 2, 3
            if input_array[r, c] == red_color:
                red_in_left_half = True
                break
        if red_in_left_half:
            break

    # Apply transformation based on the condition
    if red_in_left_half:
        # --- Condition True: Red found in left half ---

        # 1. Copy all non-red pixels from input to output
        for r in range(rows):
            for c in range(cols):
                if input_array[r, c] != red_color:
                    output_array[r, c] = input_array[r, c]

        # 2. Draw a 4x4 solid red square in the bottom-right quadrant
        # Ensure indices are within bounds, although for 8x8 it's fixed
        start_row, end_row = 4, 8
        start_col, end_col = 4, 8
        if start_row < rows and start_col < cols: # Check if top-left corner is valid
            # Adjust end bounds if they exceed grid size
            actual_end_row = min(end_row, rows)
            actual_end_col = min(end_col, cols)
            output_array[start_row:actual_end_row, start_col:actual_end_col] = red_color

    else:
        # --- Condition False: No red found in left half ---

        # 1. Copy all non-maroon pixels from input to output
        for r in range(rows):
            for c in range(cols):
                if input_array[r, c] != maroon_color:
                    output_array[r, c] = input_array[r, c]

        # 2. Draw a 3x4 solid maroon rectangle in the top-right quadrant
        # Ensure indices are within bounds
        start_row, end_row = 0, 3
        start_col, end_col = 4, 8
        if start_row < rows and start_col < cols: # Check if top-left corner is valid
             # Adjust end bounds if they exceed grid size
            actual_end_row = min(end_row, rows)
            actual_end_col = min(end_col, cols)
            output_array[start_row:actual_end_row, start_col:actual_end_col] = maroon_color

    # Convert back to list of lists for the expected output format
    return output_array.tolist()