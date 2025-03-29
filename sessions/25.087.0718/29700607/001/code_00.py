import numpy as np

"""
Transformation Rule:
1. Identify the contiguous sequence of non-white pixels in the top row (row 0). Record the color and column index for each pixel in this sequence.
2. Identify all other non-white pixels below the top row ("isolated pixels"). Record their color, row, and column index.
3. For each color present in the top sequence:
    a. Find the maximum row index among all isolated pixels of the same color. If no such isolated pixel exists, use the grid's last row index.
    b. Draw a vertical line downwards from the top sequence pixel's position (column) using its color, stopping at the determined maximum row index.
4. For each isolated pixel:
    a. Find the column index of the top sequence pixel that shares its color.
    b. Draw a horizontal line in the isolated pixel's row, using its color, connecting the isolated pixel's original column to the column of the corresponding top sequence pixel. Fill all cells between these two columns (inclusive) in that row.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # --- 1. Identify the top sequence ---
    top_sequence = {} # {color: column_index}
    top_row = input_grid_np[0, :]
    in_sequence = False
    start_col = -1
    for c in range(width):
        if top_row[c] != 0:
            if not in_sequence:
                in_sequence = True
                start_col = c # Mark the start of a potential sequence
            top_sequence[top_row[c]] = c # Store color and its column
        elif in_sequence:
            # If we hit a 0 after being in a sequence, the contiguous sequence ends
            break 
        # Continue if top_row[c] is 0 and we weren't in a sequence

    # --- 2. Identify isolated pixels ---
    isolated_pixels = {} # {color: list of (row, col)}
    for r in range(1, height):
        for c in range(width):
            color = input_grid_np[r, c]
            if color != 0:
                if color not in isolated_pixels:
                    isolated_pixels[color] = []
                isolated_pixels[color].append((r, c))

    # --- 3. Draw vertical lines ---
    for color, top_col in top_sequence.items():
        # Find max row for this color among isolated pixels
        max_row = 0 # Default start row is 0 (top row itself)
        if color in isolated_pixels:
            # Find the maximum row index among isolated pixels of this color
            rows_for_color = [r for r, c in isolated_pixels[color]]
            if rows_for_color: # Check if the list is not empty
                 max_row = max(rows_for_color)
            else: # If color exists but has no locations (shouldn't happen with current logic but safe check)
                max_row = height - 1
        else:
            # If no isolated pixels of this color exist, extend to the bottom
            max_row = height - 1

        # Draw the vertical line from row 1 down to max_row
        if max_row > 0: # Only draw if the line extends beyond row 0
             output_grid[1 : max_row + 1, top_col] = color

    # --- 4. Draw horizontal lines ---
    for color, locations in isolated_pixels.items():
        if color in top_sequence: # Only draw if the color exists in the top sequence
            top_col = top_sequence[color]
            for iso_row, iso_col in locations:
                # Determine start and end columns for the horizontal line
                start_col = min(iso_col, top_col)
                end_col = max(iso_col, top_col)
                # Draw the horizontal line
                output_grid[iso_row, start_col : end_col + 1] = color

    return output_grid.tolist() # Convert back to list of lists if required by the environment