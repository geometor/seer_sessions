import numpy as np
from typing import Set, List, Tuple

"""
Transformation Rule:
1. Identify the unique color ('target_color') present in the input grid that is neither white (0) nor gray (5).
2. Identify rows that exclusively contain gray (5) pixels and 'target_color' pixels. These are the 'structural rows'.
3. Identify columns that exclusively contain gray (5) pixels and 'target_color' pixels. These are the 'structural columns'.
4. Initialize the output grid with the same dimensions as the input, filled with white (0).
5. Copy all gray (5) pixels from their original positions in the input grid to the output grid.
6. For every intersection point defined by a 'structural row' index `r` and a 'structural column' index `c`, set the pixel at `(r, c)` in the output grid to the 'target_color'. This overwrites any gray pixel previously placed at these intersection coordinates.
"""

def find_target_color(grid: np.ndarray) -> int:
    """Finds the unique color in the grid that is not white (0) or gray (5)."""
    unique_colors = np.unique(grid)
    target_color = -1  # Default value if not found
    for color in unique_colors:
        if color != 0 and color != 5:
            if target_color == -1:
                target_color = color
            else:
                # This case implies more than one non-background/non-structure color,
                # which shouldn't happen based on the examples.
                # Handle as an error or according to specific problem constraints if needed.
                pass # For now, assume only one target color exists per example
    if target_color == -1:
        # Handle case where no target color is found (e.g. input is only white/gray)
        # Based on examples, a target color should always exist.
        # We might return a default or raise an error depending on expected behavior.
        # Let's assume it always exists for valid inputs based on task description.
        # We could pick an arbitrary color, but it's better to rely on finding one.
         raise ValueError("No target color (non-0, non-5) found in the input grid.")
    return target_color

def get_structural_indices(grid: np.ndarray, target_color: int, axis: int) -> List[int]:
    """
    Finds the indices of rows (axis=0) or columns (axis=1)
    that contain only gray (5) and the target_color.
    """
    structural_indices = []
    num_elements = grid.shape[axis]
    num_orthogonal_elements = grid.shape[1 - axis]

    for i in range(num_elements):
        is_structural = True
        contains_gray_or_target = False
        if axis == 0: # Check row i
            line = grid[i, :]
        else: # Check column i
            line = grid[:, i]

        for pixel in line:
            if pixel == 5 or pixel == target_color:
                contains_gray_or_target = True
            else: # Contains other colors (like white 0)
                 is_structural = False
                 break # No need to check further in this line

        # A line is structural if it consists *only* of 5 and target_color
        # and is not empty (which contains_gray_or_target checks implicitly).
        # It must contain *at least one* 5 or target_color pixel.
        if is_structural and contains_gray_or_target:
            structural_indices.append(i)

    return structural_indices


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Identifies a target color, structural gray lines (potentially interrupted by the target color),
    and places the target color at the intersections of these lines in the output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # 1. Identify the target_color
    try:
        target_color = find_target_color(input_array)
    except ValueError as e:
        print(f"Error: {e}. Returning input grid or a default.")
        # Decide on fallback behavior - return input, empty, or specific pattern
        return input_array # Example fallback: return input unchanged

    # 2. & 3. Identify structural rows and columns
    # A row/column is structural if it *only* contains gray (5) and the target_color
    structural_rows = []
    for r in range(height):
        row_colors = np.unique(input_array[r, :])
        is_structural = True
        contains_structure_colors = False
        for color in row_colors:
            if color == 5 or color == target_color:
                contains_structure_colors = True
            else: # Contains a color other than 5 or target_color (e.g., 0)
                is_structural = False
                break
        if is_structural and contains_structure_colors: # Must contain at least one 5 or target_color
             structural_rows.append(r)


    structural_cols = []
    for c in range(width):
        col_colors = np.unique(input_array[:, c])
        is_structural = True
        contains_structure_colors = False
        for color in col_colors:
             if color == 5 or color == target_color:
                 contains_structure_colors = True
             else: # Contains a color other than 5 or target_color (e.g., 0)
                 is_structural = False
                 break
        if is_structural and contains_structure_colors: # Must contain at least one 5 or target_color
             structural_cols.append(c)


    # 4. Initialize the output grid with white (0)
    output_grid = np.zeros_like(input_array) # Fills with 0 (white)

    # 5. Copy gray (5) pixels from input to output
    gray_mask = (input_array == 5)
    output_grid[gray_mask] = 5

    # 6. Place target_color at intersections of structural lines
    for r in structural_rows:
        for c in structural_cols:
             # Check if the point (r,c) is actually within grid bounds, though it should be by definition
            if 0 <= r < height and 0 <= c < width:
                 output_grid[r, c] = target_color

    return output_grid.tolist() # Convert back to list of lists if required by framework
