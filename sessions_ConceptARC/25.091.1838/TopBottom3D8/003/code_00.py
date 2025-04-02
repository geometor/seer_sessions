import numpy as np
from collections import Counter
import copy

"""
Identifies a single dominant vertical line and one or more dominant horizontal lines 
in the input grid based on the most frequent non-background color in each column/row.
For each intersection point between the vertical line's column and a horizontal line's row:
- If the horizontal line's dominant color is yellow (4), the intersection pixel in 
  the output grid takes the yellow color (4).
- Otherwise, the intersection pixel in the output grid takes the dominant color 
  of the vertical line.
Pixels not at an intersection remain unchanged.
"""

def find_dominant_color(line_segment):
    """
    Finds the most frequent non-background color in a 1D array (row or column segment).

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
    # If there's a tie, most_common(1) picks one arbitrarily, which is acceptable here.
    dominant_color, count = counts.most_common(1)[0]
    
    # Simple majority isn't strictly required by the revised logic, just the most frequent.
    # Let's ensure there is at least one non-background color.
    if count > 0:
        return dominant_color, count
    else:
        return None, 0


def find_vertical_line(grid):
    """
    Finds the column index and dominant color of the single vertical line.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (column_index, dominant_color) of the vertical line, 
               or (None, None) if not found.
    """
    height, width = grid.shape
    max_count = 0
    best_col = None
    best_color = None

    for c in range(width):
        col_cells = grid[:, c]
        dominant_color, count = find_dominant_color(col_cells)
        
        # In these examples, the line seems distinct. We assume the column
        # with the highest count of a single non-background color is the target.
        # A more robust check might be needed for more complex cases (e.g., multiple vertical lines).
        if dominant_color is not None and count > max_count:
             # Check if this column has more non-background cells than others, potentially
             non_bg_total = np.count_nonzero(col_cells)
             # Heuristic: The vertical bar usually has more non-background cells than others.
             # This helps differentiate from sparse columns. Let's require at least 2.
             if non_bg_total >= 2:
                 max_count = count
                 best_col = c
                 best_color = dominant_color

    # A final check: ensure the found color exists in most cells of the column
    # This was the issue before. Let's trust the max count for now.
    # If find_dominant_color returns a color, it's the most frequent non-zero one.
    
    # Refined logic: Check if non-zero cells exist primarily in this column.
    # Calculate total non-zero cells per column
    col_non_zeros = np.count_nonzero(grid, axis=0)
    # The vertical bar column should have significantly more non-zero cells than average,
    # or be the max.
    if best_col is not None:
         # Let's just assume the column with the most frequent single color is the one.
         return best_col, best_color
         
    # Fallback if the above didn't work - maybe the simple count wasn't enough
    # Try finding column with maximum number of non-background pixels first
    if best_col is None:
        col_non_zeros = np.count_nonzero(grid, axis=0)
        if np.any(col_non_zeros):
            potential_v_col = np.argmax(col_non_zeros)
            dominant_color, count = find_dominant_color(grid[:, potential_v_col])
            if dominant_color is not None:
                 return potential_v_col, dominant_color

    return None, None


def find_horizontal_lines(grid):
    """
    Finds the row index and dominant color of all horizontal lines.

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
        
        # We need a condition to decide if this row constitutes a "line".
        # Let's assume any row with a dominant non-background color counts.
        # We might need a threshold, e.g., count >= width / 2 or similar if needed.
        # Check if there are at least 2 non-background pixels in the row.
        if dominant_color is not None and np.count_nonzero(row_cells) >= 2:
             # Check if the dominant color count is significant (e.g., > half the non-zero cells?)
             # For now, just having a dominant color and >=2 non-zero seems okay for examples.
             lines.append((r, dominant_color))
             
    return lines


def transform(input_grid):
    """
    Transforms the input grid based on the intersection color rules using dominant colors.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    # Create a deep copy to modify
    output_grid = copy.deepcopy(grid_np)
    
    # --- Identify Lines ---
    # Find the vertical line (column index and its dominant color)
    v_col, v_color = find_vertical_line(grid_np)
    
    # Find all horizontal lines (list of (row index, dominant color))
    h_lines = find_horizontal_lines(grid_np)

    # Check if a vertical line was found
    if v_col is None or v_color is None:
        # If no vertical line, return the original grid copy
        # Or potentially handle cases where only horizontal lines exist if needed
        return output_grid.tolist() 

    # --- Apply Transformation at Intersections ---
    # Iterate through each found horizontal line
    for h_row, h_color in h_lines:
        # Define the intersection point coordinates
        intersection_row = h_row
        intersection_col = v_col

        # Check grid boundaries (shouldn't be necessary if indices are correct)
        # if 0 <= intersection_row < output_grid.shape[0] and 0 <= intersection_col < output_grid.shape[1]:
            
        # Apply the color rule based on the horizontal line's dominant color
        if h_color == 4:  # If horizontal line's dominant color is yellow
            output_grid[intersection_row, intersection_col] = h_color # Set intersection to yellow
        else:
            # Otherwise, set intersection to the vertical line's dominant color
            output_grid[intersection_row, intersection_col] = v_color 

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()