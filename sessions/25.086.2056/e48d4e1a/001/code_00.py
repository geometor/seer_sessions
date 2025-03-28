"""
Transform an input grid by relocating its horizontal and vertical lines based on a count of gray pixels.

1. Identify the dominant color (not white 0 or gray 5) forming a complete horizontal line and a complete vertical line in the input grid.
2. Find the row index (input_h_row) of the horizontal line and the column index (input_v_col) of the vertical line.
3. Count the number of gray (5) pixels (N) in the input grid.
4. Calculate the new row index for the horizontal line: output_h_row = input_h_row + N.
5. Calculate the new column index for the vertical line: output_v_col = input_v_col - N.
6. Create an output grid of the same dimensions as the input, filled with white (0).
7. Draw the horizontal line of the dominant color at output_h_row in the output grid.
8. Draw the vertical line of the dominant color at output_v_col in the output grid.
"""

import numpy as np

def find_dominant_color_and_lines(grid):
    """
    Finds the dominant color and the indices of the horizontal and vertical lines.
    The dominant color is the one forming complete lines, excluding white (0) and gray (5).
    """
    rows, cols = grid.shape
    dominant_color = -1
    input_h_row = -1
    input_v_col = -1

    # Find horizontal line and dominant color
    for r in range(rows):
        row_elements = np.unique(grid[r, :])
        # Check if the row consists of a single non-background, non-gray color
        if len(row_elements) == 1 and row_elements[0] not in [0, 5]:
            dominant_color = row_elements[0]
            input_h_row = r
            break
        # Check if the row consists of the dominant color and potentially white
        elif len(row_elements) == 2 and dominant_color != -1 and dominant_color in row_elements and 0 in row_elements:
             # Check if it's a full line of dominant color
             if np.all(grid[r, :] == dominant_color):
                 input_h_row = r
                 break
        # Check if the row consists of the dominant color and potentially gray (edge case?)
        elif len(row_elements) == 2 and dominant_color != -1 and dominant_color in row_elements and 5 in row_elements:
             # Check if it's a full line of dominant color
             if np.all(grid[r, :] == dominant_color):
                 input_h_row = r
                 break


    # If dominant color wasn't found via horizontal line, try vertical
    if dominant_color == -1:
        for c in range(cols):
            col_elements = np.unique(grid[:, c])
            if len(col_elements) == 1 and col_elements[0] not in [0, 5]:
                dominant_color = col_elements[0]
                # We still need to find the horizontal line index later
                break
            elif len(col_elements) > 1: # Look for columns that aren't just background
                 for color in col_elements:
                     if color not in [0, 5]:
                         # Check if this color forms a full vertical line
                         if np.all(grid[:, c] == color):
                             dominant_color = color
                             break
                 if dominant_color != -1:
                     break # Found dominant color via vertical line


    # Find vertical line column using the determined dominant color
    for c in range(cols):
         # Check if the column is entirely the dominant color
         if np.all(grid[:, c] == dominant_color):
             input_v_col = c
             break
         # Check if the column contains only the dominant color and white/gray
         col_elements = np.unique(grid[:, c])
         if dominant_color in col_elements:
             is_potential_line = True
             for element in col_elements:
                 if element not in [0, 5, dominant_color]:
                     is_potential_line = False
                     break
             if is_potential_line:
                 # Verify it's a full line (might intersect horizontal line)
                 count_dominant = np.sum(grid[:, c] == dominant_color)
                 if count_dominant == rows: # It's a full solid line
                      input_v_col = c
                      break
                 elif count_dominant == rows -1: # It might be the line we are looking for intersecting another
                     # Check if the non-dominant color is at the horizontal line intersection
                     non_dominant_indices = np.where(grid[:, c] != dominant_color)[0]
                     if len(non_dominant_indices) == 1 and non_dominant_indices[0] == input_h_row:
                           # It looks like the correct vertical line, even if intersected
                           input_v_col = c
                           # Need to find the actual horizontal line row if not found yet
                           if input_h_row == -1:
                                for r in range(rows):
                                     if np.all(grid[r, :] == dominant_color):
                                         input_h_row = r
                                         break
                           break


    # Final check/find for horizontal row if needed
    if input_h_row == -1 and dominant_color != -1:
         for r in range(rows):
             if np.all(grid[r, :] == dominant_color):
                 input_h_row = r
                 break
             # Check for intersections
             row_elements = np.unique(grid[r, :])
             if dominant_color in row_elements:
                 is_potential_line = True
                 for element in row_elements:
                     if element not in [0, 5, dominant_color]:
                         is_potential_line = False
                         break
                 if is_potential_line:
                      count_dominant = np.sum(grid[r, :] == dominant_color)
                      if count_dominant == cols:
                          input_h_row = r
                          break
                      elif count_dominant == cols -1:
                           non_dominant_indices = np.where(grid[r, :] != dominant_color)[0]
                           if len(non_dominant_indices) == 1 and non_dominant_indices[0] == input_v_col:
                               input_h_row = r
                               break


    if dominant_color == -1 or input_h_row == -1 or input_v_col == -1:
        # Fallback or error handling if lines/color not found as expected
        # This part might need refinement based on more complex cases.
        # For now, try finding the most frequent non-zero color as dominant.
        colors, counts = np.unique(grid[grid != 0], return_counts=True)
        if len(colors) > 0:
            max_count_idx = np.argmax(counts)
            potential_dominant = colors[max_count_idx]
            if potential_dominant != 5: # Ensure it's not gray
                dominant_color = potential_dominant
                # Attempt to find lines again with this assumption
                if input_h_row == -1:
                    for r in range(rows):
                         if np.sum(grid[r,:] == dominant_color) > cols // 2 : # Heuristic: If more than half the row is the color
                             if np.all(grid[r, grid[r,:] != 0] == dominant_color): # Check non-zero cells are dominant
                                 input_h_row = r
                                 break
                if input_v_col == -1:
                     for c in range(cols):
                         if np.sum(grid[:,c] == dominant_color) > rows // 2: # Heuristic
                             if np.all(grid[grid[:,c] != 0, c] == dominant_color): # Check non-zero cells are dominant
                                 input_v_col = c
                                 break

    if dominant_color == -1 or input_h_row == -1 or input_v_col == -1:
         raise ValueError("Could not reliably determine dominant color or line positions.")


    return dominant_color, input_h_row, input_v_col

def count_gray_pixels(grid):
    """Counts the number of gray (5) pixels in the grid."""
    return np.sum(grid == 5)

def transform(input_grid):
    """
    Transforms the input grid by moving horizontal and vertical lines.
    The movement distance and direction is determined by the count of gray pixels.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Find the dominant color and the original line positions
    dominant_color, input_h_row, input_v_col = find_dominant_color_and_lines(input_array)

    # Count the number of gray pixels
    n_gray = count_gray_pixels(input_array)

    # Calculate the new line positions
    output_h_row = input_h_row + n_gray
    output_v_col = input_v_col - n_gray

    # Ensure new positions are within grid bounds (though examples suggest they are)
    output_h_row = max(0, min(rows - 1, output_h_row))
    output_v_col = max(0, min(cols - 1, output_v_col))

    # Initialize the output grid with the background color (white 0)
    output_grid = np.zeros_like(input_array)

    # Draw the new horizontal line
    output_grid[output_h_row, :] = dominant_color

    # Draw the new vertical line
    # This will overwrite the cell at the intersection, which is the correct behavior
    output_grid[:, output_v_col] = dominant_color

    # Return the transformed grid as a list of lists
    return output_grid.tolist()