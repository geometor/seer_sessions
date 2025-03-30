```python
import numpy as np
from typing import List, Tuple, Optional, Set

"""
Extracts a subgrid representing the bounding box of specific color(s) found only 
in the bottom-most horizontal region of the input grid, where regions are 
separated by rows of the background color (white, 0). The specific color(s) 
to extract are those present in the bottom region but not in the region 
immediately above it.

The process involves:
1. Identifying the last row containing non-background pixels (`last_row`).
2. Identifying the last separator row (all background) before `last_row`.
3. Defining the row ranges for the 'bottom block' (below separator) and 'top block' (above or including separator).
4. Finding the unique non-background colors in each block.
5. Determining the 'target colors' (those unique to the bottom block).
6. Finding the minimal column bounds containing any target color pixels within the bottom block's rows.
7. Extracting the subgrid defined by the bottom block's row range and the target color's column bounds.
"""

def find_last_non_background_row(grid: np.ndarray, background_color: int = 0) -> Optional[int]:
    """
    Finds the index of the last row containing any non-background pixels.
    Scans from bottom to top. Returns None if the grid is empty or all background.
    """
    height = grid.shape[0]
    for r in range(height - 1, -1, -1):
        if np.any(grid[r] != background_color):
            return r
    return None

def find_last_all_background_row_before(grid: np.ndarray, end_row_index: int, background_color: int = 0) -> int:
    """
    Finds the index of the last row consisting entirely of background_color,
    searching upwards from (but not including) end_row_index down to row 0.
    Returns -1 if no such row is found.
    """
    for r in range(end_row_index - 1, -1, -1):
        if np.all(grid[r] == background_color):
            return r
    return -1 # Indicates no separator row found above the content

def get_unique_colors_in_rows(grid: np.ndarray, start_row: int, end_row: int, background_color: int = 0) -> Set[int]:
    """
    Finds the set of unique non-background colors within a specified row range (inclusive).
    Returns an empty set if the range is invalid or contains only background.
    """
    if start_row < 0 or end_row < start_row or start_row >= grid.shape[0]:
        return set()
    # Ensure end_row is within grid bounds for slicing
    actual_end_row = min(end_row, grid.shape[0] - 1)
    subgrid = grid[start_row : actual_end_row + 1]
    if subgrid.size == 0:
        return set()
    unique_colors = np.unique(subgrid)
    non_background_colors = unique_colors[unique_colors != background_color]
    return set(non_background_colors)

def find_target_column_bounds(grid: np.ndarray, start_row: int, end_row: int, target_colors: Set[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the minimum and maximum column indices containing any of the target_colors
    within the specified row range (inclusive).
    Returns None if no target colors are found in the range.
    """
    min_col = grid.shape[1]
    max_col = -1
    found_target = False

    # Ensure row bounds are valid
    start_row = max(0, start_row)
    end_row = min(grid.shape[0] - 1, end_row)
    
    if start_row > end_row: # Handle cases where block might be empty after clipping
         return None

    for r in range(start_row, end_row + 1):
        for c in range(grid.shape[1]):
            if grid[r, c] in target_colors:
                found_target = True
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    if not found_target:
        return None
    return min_col, max_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the described rule.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    background_color = 0
    height, width = grid.shape

    if height == 0 or width == 0:
        return [] # Handle empty input

    # 1. Find the bottom row index of any non-background content
    last_row = find_last_non_background_row(grid, background_color)

    # If no non-background pixels exist anywhere, return empty grid
    if last_row is None:
        return []

    # 2. Find the highest separator row (all background) below last_row
    separator_row = find_last_all_background_row_before(grid, last_row, background_color)
    # separator_row is -1 if no separator exists

    # 3. Define row ranges for blocks
    bottom_block_start_row = separator_row + 1
    bottom_block_end_row = last_row
    top_block_start_row = 0
    top_block_end_row = separator_row # Use separator_row directly. Slicing handles end<start.

    # 4. Identify unique non-background colors in each block
    top_colors = get_unique_colors_in_rows(grid, top_block_start_row, top_block_end_row, background_color)
    bottom_colors = get_unique_colors_in_rows(grid, bottom_block_start_row, bottom_block_end_row, background_color)

    # 5. Determine the target colors (present in bottom block, absent in top block)
    target_colors = bottom_colors - top_colors

    # If no unique colors in bottom block, result is empty (shouldn't happen if last_row exists)
    if not target_colors:
         # This might occur if the only non-bg color in bottom is also in top
         # Let's find the bounding box of *all* non-bg colors in the bottom block in this case?
         # Or maybe the rule implies there *must* be a unique color.
         # Based on examples, there's always a unique color. If not, returning empty seems plausible.
         # Let's stick to the derived rule: only extract unique colors.
        # Re-evaluate if a test case fails this assumption.
        # We need *some* bounds to extract *something*. Let's calculate bounds for any non-bg color in the bottom block.
        all_non_bg_bottom_colors = get_unique_colors_in_rows(grid, bottom_block_start_row, bottom_block_end_row, background_color)
        if not all_non_bg_bottom_colors: return [] # Truly empty bottom block
        col_bounds = find_target_column_bounds(grid, bottom_block_start_row, bottom_block_end_row, all_non_bg_bottom_colors)

        # The previous code simply returned [], let's try that first.
        # The examples always have a target color.
        # A more robust approach might be needed if edge cases without unique colors exist.
        # For now, assume target_colors will be non-empty if bottom_colors is non-empty.
        # If bottom_colors IS empty, last_row wouldn't have been found, so we shouldn't reach here.
        # Let's check if target_colors is empty but bottom_colors is not.
        if not target_colors and bottom_colors:
             # This means all colors in bottom also exist in top.
             # The examples don't cover this. What should happen?
             # Possibility 1: Extract bounding box of *all* colors in bottom block.
             # Possibility 2: Return empty.
             # Let's choose Possibility 2 for now as it aligns with strict interpretation.
             return []


    # 6. Find the column bounds (left and right edges) for target colors within the bottom block rows
    col_bounds = find_target_column_bounds(grid, bottom_block_start_row, bottom_block_end_row, target_colors)

    # If no target colors were found within the bottom block (e.g., if target_colors was somehow empty)
    if col_bounds is None:
        return []

    first_col, last_col = col_bounds

    # 7. Extract the subgrid using numpy slicing
    # Rows: from bottom_block_start_row up to and including bottom_block_end_row
    # Cols: from first_col up to and including last_col
    output_grid_np = grid[bottom_block_start_row : bottom_block_end_row + 1, first_col : last_col + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```