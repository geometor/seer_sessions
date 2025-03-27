import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule:
1. Identify the single horizontal red line (color 2) and its row index (`red_line_row`).
2. Identify the single color (`paired_color`) present that is neither white (0) nor red (2). Locate all pixels of this color, forming two objects: one above and one below the red line.
3. Determine the set of column indices occupied by the object above the red line (`cols_above`).
4. Determine the set of column indices occupied by the object below the red line (`cols_below`).
5. Find the intersection of these two sets of column indices (`common_cols`).
6. Determine the vertical placement of the yellow rectangle:
    a. If `cols_above` is a proper subset of `cols_below`, place the rectangle below the red line.
    b. Otherwise (if `cols_below` is a proper subset of `cols_above`, or if neither is a proper subset of the other), place the rectangle above the red line.
7. Define the rectangle boundaries:
    a. Horizontal: Spans the columns in `common_cols`.
    b. Vertical: 
        i. If placed below: Starts at row `red_line_row + 1`, ends at the last row (`height - 1`).
        ii. If placed above: Starts at row 0, ends at row `red_line_row - 1`.
8. Create the output grid by copying the input grid.
9. Fill the determined rectangle area in the output grid with yellow (color 4), but only overwrite existing white (color 0) pixels.
"""

def find_colored_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_object_columns(pixels: List[Tuple[int, int]]) -> Set[int]:
    """Gets the set of unique column indices from a list of pixel coordinates."""
    if not pixels:
        return set()
    return set(col for _, col in pixels)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Find the red line row
    red_line_row = -1
    for r in range(height):
        # Check if any red pixel exists in the row as an indicator
        if np.any(input_np[r, :] == 2):
             # Verify all red pixels are ONLY on this row
             red_rows, _ = np.where(input_np == 2)
             if np.all(red_rows == r):
                 red_line_row = r
                 break
             else:
                 # Handle potential complex red structures if necessary,
                 # but for now, assume the first row with red is the line if all red is on it.
                 # If red exists on multiple rows, this logic might fail for unseen patterns.
                 print(f"Warning: Red pixels found on multiple rows. Using row {r} as the reference line.")
                 red_line_row = r
                 break # Take the first occurrence as the line

    # Check if red line indicator was found
    if red_line_row == -1:
        print("Error: Red line indicator (color 2) not found.")
        return input_grid # Return original if rule prerequisite is missing

    # 2. Find the paired objects' color and pixels
    paired_object_color = -1
    all_paired_pixels = []
    unique_colors = np.unique(input_np)
    for color in unique_colors:
        if color not in [0, 2]: # Exclude white and red
            paired_object_color = color
            all_paired_pixels = find_colored_pixels(input_np, paired_object_color)
            break # Assume only one such color pair exists

    if paired_object_color == -1:
         print("Warning: Paired objects (non-white, non-red) not found.")
         return output_np.tolist() # Return unmodified copy if no objects to compare

    # Separate pixels into above and below the red line
    pixels_above = [p for p in all_paired_pixels if p[0] < red_line_row]
    pixels_below = [p for p in all_paired_pixels if p[0] > red_line_row]

    # 3. Get column indices for the object above
    cols_above = get_object_columns(pixels_above)

    # 4. Get column indices for the object below
    cols_below = get_object_columns(pixels_below)

    # 5. Find the intersection of column indices
    common_cols = cols_above.intersection(cols_below)

    # 6. Determine vertical placement based on subset relationship
    place_above = True # Default placement
    is_above_proper_subset_of_below = cols_above.issubset(cols_below) and cols_above != cols_below
    
    if is_above_proper_subset_of_below:
        place_above = False # Place below only if 'above' shape fits strictly inside 'below' projection

    # 7. Define the row range for the yellow rectangle
    if place_above:
        start_row = 0
        end_row = red_line_row # Exclusive end (up to red_line_row - 1)
    else: # place_below
        start_row = red_line_row + 1
        end_row = height # Exclusive end (up to height - 1)

    # 8. & 9. Fill the yellow rectangle in the output grid (only on white pixels)
    for r in range(start_row, end_row):
        for c in common_cols:
            # Ensure column index is within grid bounds (safety check)
            if 0 <= c < width:
                 # Only overwrite white pixels
                 if output_np[r, c] == 0:
                     output_np[r, c] = 4 # Yellow

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid