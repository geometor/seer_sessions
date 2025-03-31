```python
import numpy as np
from typing import List, Set, Tuple

"""
Transformation Rule:
1. Identify the unique color ('target_color') present in the input grid that is neither white (0) nor gray (5).
2. Identify 'qualifying rows': rows in the input grid that consist *exclusively* of gray (5) pixels and/or the target_color pixels. No other colors (like white 0) are allowed in these rows.
3. Identify 'qualifying columns': columns in the input grid that consist *exclusively* of gray (5) pixels and/or the target_color pixels. No other colors (like white 0) are allowed in these columns.
4. Initialize an output grid of the same dimensions as the input, filled entirely with white (0).
5. For each identified 'qualifying row' index `r`, set all pixels in the corresponding row `r` of the output grid to gray (5).
6. For each identified 'qualifying column' index `c`, set all pixels in the corresponding column `c` of the output grid to gray (5). Note that pixels at intersections will be overwritten with gray.
7. For every intersection point defined by a 'qualifying row' index `r` and a 'qualifying column' index `c`, set the pixel at `(r, c)` in the output grid to the `target_color`. This specifically colors the intersection points, overwriting the gray pixels placed in steps 5 and 6.
8. Return the constructed output grid.
"""

def find_target_color(grid: np.ndarray) -> int:
    """
    Finds the unique color in the grid that is not white (0) or gray (5).
    Raises ValueError if no such color is found or if multiple such colors exist.
    """
    unique_colors = np.unique(grid)
    target_color = -1
    found = False
    for color in unique_colors:
        if color != 0 and color != 5:
            if found:
                # Found a second non-white, non-gray color - this violates the assumed pattern.
                 raise ValueError("Multiple target colors found, expected only one.")
            target_color = color
            found = True
            
    if not found:
        # No non-white, non-gray color found.
        raise ValueError("No target color (non-0, non-5) found in the input grid.")
    
    return target_color

def find_qualifying_indices(grid: np.ndarray, target_color: int, axis: int) -> List[int]:
    """
    Finds the indices of rows (axis=0) or columns (axis=1)
    that contain *only* gray (5) and/or the target_color.
    """
    qualifying_indices = []
    num_elements = grid.shape[axis]

    for i in range(num_elements):
        is_qualifying = True
        contains_structure_colors = False # Check if the line isn't just empty/white
        if axis == 0: # Check row i
            line = grid[i, :]
        else: # Check column i
            line = grid[:, i]

        # Check each pixel in the line
        for pixel in line:
            if pixel == 5 or pixel == target_color:
                contains_structure_colors = True # Found at least one valid color
            else: # Contains a color other than 5 or target_color (e.g., 0)
                is_qualifying = False
                break # Disqualifies this line

        # A line qualifies if it only contains 5 or target_color AND is not completely empty of these colors
        # Note: A line of only 5s or only target_color is also qualifying.
        if is_qualifying and contains_structure_colors:
            qualifying_indices.append(i)
            
    return qualifying_indices


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on identifying qualifying rows/columns
    containing only gray (5) and a single target color, and coloring their intersections.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # 1. Identify the target_color
    try:
        target_color = find_target_color(input_array)
    except ValueError as e:
        print(f"Error processing grid: {e}. Returning input grid as fallback.")
        # Fallback: return the input grid if pattern assumptions are violated
        return input_grid 

    # 2. Identify qualifying rows
    qualifying_rows = find_qualifying_indices(input_array, target_color, axis=0)

    # 3. Identify qualifying columns
    qualifying_cols = find_qualifying_indices(input_array, target_color, axis=1)

    # 4. Initialize the output grid with white (0)
    output_grid = np.zeros_like(input_array) # Fills with 0 (white)

    # 5. Draw gray lines for qualifying rows
    for r in qualifying_rows:
        output_grid[r, :] = 5

    # 6. Draw gray lines for qualifying columns (overwrites intersections with gray temporarily)
    for c in qualifying_cols:
        output_grid[:, c] = 5

    # 7. Color the intersections with the target_color
    for r in qualifying_rows:
        for c in qualifying_cols:
            # Check bounds just in case, though indices should be valid
            if 0 <= r < height and 0 <= c < width:
                 output_grid[r, c] = target_color

    # 8. Return the result as a list of lists
    return output_grid.tolist()
```