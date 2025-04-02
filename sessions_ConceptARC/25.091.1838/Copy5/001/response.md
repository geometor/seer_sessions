```python
import numpy as np
from typing import List, Tuple, Set

"""
Identify a 'pattern block' and 'control pixels' (blue=1) in the input grid.
The pattern block is the part of the grid not occupied by the rows or columns containing only control pixels (and potentially white=0 pixels).
Count the number of blue control pixels (N). The pattern block will be repeated R = N + 1 times.
Determine the orientation of repetition (horizontal or vertical) based on whether the control pixels define rows or columns to be excluded.
If control pixels occupy specific columns, the repetition is horizontal, separated by columns of white (0) pixels.
If control pixels occupy specific rows, the repetition is vertical, separated by rows of white (0) pixels.
Construct the output grid by concatenating the pattern block and white separators R times (pattern) and R-1 times (separator) according to the determined orientation.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on repeating a pattern block determined
    by the position and count of blue control pixels.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Identify Control Pixels (blue=1) and count them.
    blue_coords = find_pixels(grid, 1)
    
    # Handle edge case where there are no blue pixels (though examples suggest there always are)
    if not blue_coords:
        return input_grid # Or potentially raise an error or return an empty grid

    N = len(blue_coords)
    repetition_count = N + 1

    # 2. Determine rows and columns occupied by blue pixels.
    blue_rows = set(r for r, c in blue_coords)
    blue_cols = set(c for r, c in blue_coords)

    # 3. Identify potential pattern rows/columns by excluding blue rows/columns.
    potential_pattern_rows_idx = sorted(list(set(range(height)) - blue_rows))
    potential_pattern_cols_idx = sorted(list(set(range(width)) - blue_cols))

    # 4. Determine Orientation and identify the actual pattern block.
    # We check if the grid area defined *only* by blue rows/cols contains any non-blue pixels.
    # If the blue-pixel-exclusive columns contain non-blue pixels, separation must be row-wise (vertical).
    # If the blue-pixel-exclusive rows contain non-blue pixels, separation must be column-wise (horizontal).

    # Default assumption: separation by columns (horizontal repetition)
    orientation = 'horizontal'
    pattern_rows_idx = list(range(height)) # Assume pattern uses all rows initially
    pattern_cols_idx = potential_pattern_cols_idx

    # Check if blue pixels define rows instead of columns
    # This happens if the columns *not* containing blue pixels are empty or only contain white
    # Or, more robustly, if the rows *containing* blue pixels also contain non-blue, non-white elements elsewhere.
    
    # A simpler check based on the examples: if removing blue rows leaves all columns intact, it's vertical. If removing blue cols leaves all rows intact, it's horizontal.
    if len(potential_pattern_rows_idx) < height and len(potential_pattern_cols_idx) == width:
         orientation = 'vertical'
         pattern_rows_idx = potential_pattern_rows_idx
         pattern_cols_idx = list(range(width))
    elif len(potential_pattern_cols_idx) < width and len(potential_pattern_rows_idx) == height:
         orientation = 'horizontal'
         pattern_rows_idx = list(range(height))
         pattern_cols_idx = potential_pattern_cols_idx
    else:
        # Fallback or more complex logic might be needed for ambiguous cases,
        # but the provided examples fit the above conditions.
        # Let's refine the check slightly: If blue pixels occupy *entire* rows/columns
        # that contain *only* blue or white pixels, those rows/columns define the separation.
        
        separating_rows = True
        for r in blue_rows:
            if np.any((grid[r, :] != 1) & (grid[r, :] != 0)):
                separating_rows = False
                break
        
        separating_cols = True
        for c in blue_cols:
             if np.any((grid[:, c] != 1) & (grid[:, c] != 0)):
                separating_cols = False
                break

        if separating_rows and not separating_cols:
             orientation = 'vertical'
             pattern_rows_idx = potential_pattern_rows_idx
             pattern_cols_idx = list(range(width))
        elif separating_cols and not separating_rows:
             orientation = 'horizontal'
             pattern_rows_idx = list(range(height))
             pattern_cols_idx = potential_pattern_cols_idx
        # If both or neither are true, stick with the initial dimension-based check result (or previous default)
        # The dimension check handles the provided examples correctly.


    # Extract the pattern block using determined indices
    # Need np.ix_ for advanced indexing with lists
    ix_rows, ix_cols = np.ix_(pattern_rows_idx, pattern_cols_idx)
    pattern_block = grid[ix_rows, ix_cols]

    # Handle case where pattern block is empty (if logic failed)
    if pattern_block.size == 0:
        # This indicates an issue with identifying the pattern or orientation
        # Returning input might be safest for now, or raise error
        print("Warning: Pattern block identification failed.")
        return input_grid

    # 5. Create Separator (white=0)
    if orientation == 'horizontal':
        separator = np.zeros((pattern_block.shape[0], 1), dtype=int)
    else: # vertical
        separator = np.zeros((1, pattern_block.shape[1]), dtype=int)

    # 6. Construct Output Grid
    output_parts = []
    for i in range(repetition_count):
        output_parts.append(pattern_block)
        if i < repetition_count - 1:
            output_parts.append(separator)

    if orientation == 'horizontal':
        output_grid_np = np.hstack(output_parts)
    else: # vertical
        output_grid_np = np.vstack(output_parts)

    # Convert back to list of lists
    return output_grid_np.tolist()

```