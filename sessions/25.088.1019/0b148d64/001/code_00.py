import numpy as np
from typing import List, Tuple, Optional

"""
Identifies the bottom-most contiguous block of non-background (non-zero) pixels 
in the input grid, where blocks are separated by horizontal rows consisting 
entirely of the background color (0). The transformation extracts the bounding 
box of this bottom-most block.

1. Scan the input grid from bottom to top to find the index of the last row 
   containing any non-background pixel. This is the bottom edge of the target region.
2. Scan from this bottom edge row upwards to find the index of the first row 
   encountered that consists entirely of the background color (0). The row below 
   this separator row is the top edge of the target region. If no separator row 
   is found above the bottom edge, the top edge is the first row (index 0) of 
   the grid.
3. Within the identified rows (from top edge to bottom edge, inclusive), find the 
   minimum and maximum column indices that contain a non-background pixel across 
   any of these rows. These are the left and right edges of the target region.
4. Extract the subgrid defined by these row and column boundaries.
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

def find_last_all_background_row_before(grid: np.ndarray, end_row_index: int, background_color: int = 0) -> Optional[int]:
    """
    Finds the index of the last row consisting entirely of background_color,
    searching upwards from (but not including) end_row_index down to row 0.
    Returns None if no such row is found.
    """
    for r in range(end_row_index - 1, -1, -1):
        if np.all(grid[r] == background_color):
            return r
    return None

def find_column_bounds(grid: np.ndarray, start_row: int, end_row: int, background_color: int = 0) -> Optional[Tuple[int, int]]:
    """
    Finds the minimum and maximum column indices containing non-background pixels
    within the specified row range (inclusive).
    Returns None if no non-background pixels are found in the range.
    """
    min_col = grid.shape[1]
    max_col = -1
    found_non_bg = False

    for r in range(start_row, end_row + 1):
        non_bg_indices = np.where(grid[r] != background_color)[0]
        if non_bg_indices.size > 0:
            found_non_bg = True
            current_min = np.min(non_bg_indices)
            current_max = np.max(non_bg_indices)
            min_col = min(min_col, current_min)
            max_col = max(max_col, current_max)

    if not found_non_bg:
        return None
    return min_col, max_col


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Extracts the bottom-most non-background region from the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the extracted subgrid (the bottom region).
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    background_color = 0
    height, width = grid.shape

    if height == 0 or width == 0:
        return [] # Handle empty input

    # 1. Find the bottom row index of the target region
    last_row = find_last_non_background_row(grid, background_color)
    
    # If no non-background pixels exist anywhere, return empty grid
    if last_row is None:
        return [] 

    # 2. Find the top row index of the target region
    # Scan upwards from the last_row to find the first all-background separator row
    separator_row = find_last_all_background_row_before(grid, last_row, background_color)

    # The target region starts the row *after* the separator, or row 0 if no separator found
    first_row = 0 if separator_row is None else separator_row + 1
        
    # 3. Find the column bounds (left and right edges) within the target rows
    col_bounds = find_column_bounds(grid, first_row, last_row, background_color)
    
    # This check might be redundant if last_row was found, but good practice
    if col_bounds is None:
        # This case should ideally not be reached if last_row is not None,
        # but handles potential edge cases or empty regions between separators.
        # Let's return an empty grid or the single row/column if that makes sense.
        # Based on examples, an empty result is unlikely if a non-bg row was found.
        # If last_row exists, there must be columns.
         return [] # Or potentially handle differently if needed.
        
    first_col, last_col = col_bounds

    # 4. Extract the subgrid using numpy slicing
    output_grid_np = grid[first_row : last_row + 1, first_col : last_col + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid