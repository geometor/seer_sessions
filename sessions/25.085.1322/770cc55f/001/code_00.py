import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule:
1. Identify the single horizontal red line (color 2).
2. Identify the two objects that are neither red (2) nor white (0). These two objects will have the same color and one will be above the red line, the other below.
3. Determine the set of column indices occupied by the object above the red line.
4. Determine the set of column indices occupied by the object below the red line.
5. Find the intersection of these two sets of column indices (common columns).
6. The output grid is a copy of the input grid, with an added yellow (color 4) rectangle.
7. This yellow rectangle spans vertically from the row immediately below the red line down to the second-to-last row of the grid.
8. Horizontally, the yellow rectangle spans the common columns identified in step 5.
"""

def find_colored_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_object_columns(pixels: List[Tuple[int, int]]) -> Set[int]:
    """Gets the set of unique column indices from a list of pixel coordinates."""
    if not pixels:
        return set()
    return set(col for row, col in pixels)

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
        if np.any(input_np[r, :] == 2):
            red_line_row = r
            break
    
    # Check if red line was found (should always be present based on examples)
    if red_line_row == -1:
        print("Warning: Red line (color 2) not found.")
        return input_grid # Or handle error appropriately

    # 2. Find the paired objects' color and pixels
    paired_object_color = -1
    all_paired_pixels = []
    unique_colors = np.unique(input_np)
    for color in unique_colors:
        if color != 0 and color != 2: # Exclude white and red
            paired_object_color = color
            all_paired_pixels = find_colored_pixels(input_np, paired_object_color)
            break
            
    if paired_object_color == -1:
         print("Warning: Paired objects (non-white, non-red) not found.")
         # If no paired objects, maybe just return the input? Or perhaps there's an edge case?
         # Based on examples, this shouldn't happen. For now, return unmodified copy.
         return output_np.tolist()


    # Separate pixels into above and below the red line
    pixels_above = [p for p in all_paired_pixels if p[0] < red_line_row]
    pixels_below = [p for p in all_paired_pixels if p[0] > red_line_row]

    # 3. Get column indices for the object above
    cols_above = get_object_columns(pixels_above)

    # 4. Get column indices for the object below
    cols_below = get_object_columns(pixels_below)

    # 5. Find the intersection of column indices
    common_cols = cols_above.intersection(cols_below)

    # 6. Define the row range for the yellow rectangle
    # Starts row below red line, ends at the second-to-last row (height - 1 exclusive)
    start_row = red_line_row + 1
    end_row = height # The loop will go up to end_row - 1

    # 7. & 8. Fill the yellow rectangle in the output grid
    for r in range(start_row, end_row):
        for c in common_cols:
            # Ensure column index is within grid bounds (safety check)
            if 0 <= c < width:
                 # Check if the target cell is white (0) before overwriting. 
                 # The examples suggest overwriting only white space.
                 if output_np[r, c] == 0:
                     output_np[r, c] = 4 # Yellow

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid