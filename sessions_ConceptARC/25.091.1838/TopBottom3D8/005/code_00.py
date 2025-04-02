import numpy as np
from collections import Counter
import copy

"""
Identifies a single vertical bar and one or more horizontal bars in the input grid. 
At each intersection point between the vertical bar and a horizontal bar, the pixel color 
is modified based on the following rules:
1. If the horizontal bar's color is yellow (4), the intersection pixel becomes yellow (4).
2. If the horizontal bar's color is not yellow:
   a. If the original color of the intersection pixel (in the input grid) matches the vertical bar's color, the intersection pixel takes the horizontal bar's color.
   b. If the original color of the intersection pixel does not match the vertical bar's color (implying it matches the horizontal bar's color in the examples), the intersection pixel takes the vertical bar's color.
Pixels not at an intersection remain unchanged.
"""


def find_dominant_color(line_segment):
    """
    Finds the most frequent non-background color in a 1D array (row or column segment).
    Helper function for identifying line colors.

    Args:
        line_segment (np.ndarray): A 1D numpy array representing a row or column.

    Returns:
        tuple: (dominant_color, count) or (None, 0) if no dominant non-background color.
               Returns the color with the highest count among non-zero colors.
    """
    non_background_colors = line_segment[line_segment != 0]
    if len(non_background_colors) == 0:
        return None, 0

    counts = Counter(non_background_colors)
    # Find the color with the maximum count
    dominant_color, count = counts.most_common(1)[0]
    
    if count > 0:
        return dominant_color, count
    else:
        return None, 0


def find_vertical_line(grid):
    """
    Finds the column index and dominant color of the single vertical line.
    Uses the most frequent non-background color per column as a heuristic.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (column_index, dominant_color) of the vertical line, 
               or (None, None) if not reliably found.
    """
    height, width = grid.shape
    max_freq_count = 0 # Max count of the dominant color in a column
    best_col = None
    best_color = None
    max_non_bg = 0 # Max total non-background cells in a column

    col_non_zeros = np.count_nonzero(grid, axis=0)

    for c in range(width):
        col_cells = grid[:, c]
        dominant_color, freq_count = find_dominant_color(col_cells)
        non_bg_total = col_non_zeros[c]

        # Prioritize columns with more non-background cells, then highest frequency of dominant color
        # This helps distinguish the main bar from sparse columns. Requires at least 2 non-bg cells.
        if dominant_color is not None and non_bg_total >= 2:
             # Simple approach: Pick the column with the most non-background pixels
             # Then find its dominant color. This seems robust for the examples.
             if non_bg_total > max_non_bg:
                 max_non_bg = non_bg_total
                 best_col = c
                 best_color = dominant_color
             # If non_bg counts are tied, could use frequency count as tie-breaker, but maybe not needed.


    # Refined selection: find the column with the maximum number of non-background pixels
    if np.any(col_non_zeros):
      potential_v_col = np.argmax(col_non_zeros)
      # Ensure it has at least 2 non-background pixels
      if col_non_zeros[potential_v_col] >= 2:
        dominant_color, count = find_dominant_color(grid[:, potential_v_col])
        if dominant_color is not None:
              return potential_v_col, dominant_color

    # Fallback if argmax method fails (e.g., all zeros)
    if best_col is not None:
        return best_col, best_color
        
    return None, None


def find_horizontal_lines(grid):
    """
    Finds the row index and dominant color of all horizontal lines.
    Identifies rows with at least 2 non-background pixels and finds their dominant color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (row_index, dominant_color) 
              of a horizontal line.
    """
    height, width = grid.shape
    lines = []
    for r in range(height):
        row_cells = grid[r, :]
        dominant_color, count = find_dominant_color(row_cells)
        
        # Consider it a line if it has a dominant non-background color
        # and at least 2 non-background pixels total in the row.
        if dominant_color is not None and np.count_nonzero(row_cells) >= 2:
             lines.append((r, dominant_color))
             
    return lines


def transform(input_grid):
    """
    Transforms the input grid based on the specified intersection color rules.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a deep copy of the input
    output_grid = copy.deepcopy(grid_np)
    
    # --- Identify Vertical Line ---
    # Find the column index (v_col) and dominant color (v_color) of the vertical line
    v_col, v_color = find_vertical_line(grid_np)
    
    # If no distinct vertical line is found, return the original grid copy
    if v_col is None or v_color is None:
        return output_grid.tolist() 

    # --- Identify Horizontal Lines ---
    # Find all horizontal lines, getting their row index (h_row) and dominant color (h_color)
    h_lines = find_horizontal_lines(grid_np)

    # --- Apply Transformation at Intersections ---
    # Iterate through each identified horizontal line
    for h_row, h_color in h_lines:
        # Define the intersection point coordinates
        intersection_row = h_row
        intersection_col = v_col

        # Get the original color of the pixel at the intersection from the input grid
        input_color_at_intersection = grid_np[intersection_row, intersection_col]

        # Apply the transformation rule based on horizontal color and input color
        if h_color == 4:  # Rule 1: If horizontal line's dominant color is yellow (4)
            output_grid[intersection_row, intersection_col] = h_color # Set intersection to yellow (4)
        else: # Rule 2: If horizontal line's dominant color is NOT yellow
            if input_color_at_intersection == v_color: # Rule 2a: If input color matches vertical color
                output_grid[intersection_row, intersection_col] = h_color # Set intersection to horizontal color
            else: # Rule 2b: If input color does NOT match vertical color
                output_grid[intersection_row, intersection_col] = v_color # Set intersection to vertical color

    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()