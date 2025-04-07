import numpy as np
from typing import List, Tuple, Optional

"""
The transformation rule identifies a bottom section in the input grid, separated from any top section by one or more horizontal rows containing only zeros (background value 0). 
Within this bottom section, it finds all non-zero elements and determines their overall vertical extent (min_row, max_row). 
It then identifies the right-most distinct pattern of non-zero elements within this vertical extent. A distinct pattern is separated from others horizontally by columns containing only the background value within the determined row range (min_row to max_row).
Finally, it extracts the smallest rectangular subgrid (bounding box) from the original input grid that completely encloses this right-most pattern.
"""

def find_separator_end_row(grid: np.ndarray) -> int:
    """
    Finds the row index of the last row in the separator block 
    (contiguous all-zero rows) that lies above the bottom-most object/section.
    Returns -1 if no separator is found above the bottom object or if the grid is empty/all zeros.
    """
    rows, _ = grid.shape
    if rows == 0:
        return -1

    # Find the last row containing any non-zero value
    last_non_zero_row = -1
    for r in range(rows - 1, -1, -1):
        if np.any(grid[r, :] != 0):
            last_non_zero_row = r
            break
            
    # If the grid is all zeros or empty
    if last_non_zero_row == -1:
        return -1 
        
    # Scan upwards from the last non-zero row to find the first all-zero row
    # This all-zero row marks the end of the separator block just above the bottom section
    for r in range(last_non_zero_row, -1, -1):
         if np.all(grid[r, :] == 0):
             return r # Found the last row of the separator
             
    # If no all-zero row is found above the last non-zero content,
    # it implies the bottom section starts at or near row 0 without a preceding separator.
    # In this case, the "separator" effectively ends before the grid starts.
    return -1


def find_bottom_section_content_bounds(grid: np.ndarray, bottom_section_start_row: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the overall bounding box (min_row, max_row, min_col, max_col) for *all* non-zero elements 
    located at or below the specified start row.
    Returns None if no non-zero elements are found in the bottom section.
    """
    rows, cols = grid.shape
    
    # Ensure start row is valid
    if bottom_section_start_row >= rows:
        return None

    # Consider only the part of the grid at or below the start row
    bottom_grid_view = grid[bottom_section_start_row:, :]
    
    # Get relative indices (row, col) of non-zero elements in the bottom view
    relative_non_zero_indices = np.argwhere(bottom_grid_view != 0)

    # If no non-zero elements exist in the bottom section
    if relative_non_zero_indices.size == 0:
        return None 

    # Calculate the min/max relative row and the min/max column from the relative indices
    min_rel_row = np.min(relative_non_zero_indices[:, 0])
    max_rel_row = np.max(relative_non_zero_indices[:, 0])
    min_col = np.min(relative_non_zero_indices[:, 1])
    max_col = np.max(relative_non_zero_indices[:, 1])
    
    # Convert relative row indices back to absolute grid indices
    min_abs_row = min_rel_row + bottom_section_start_row
    max_abs_row = max_rel_row + bottom_section_start_row

    return min_abs_row, max_abs_row, min_col, max_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Extracts the bounding box of the right-most pattern within the bottom section of the grid.
    """
    
    # Convert input to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Handle empty input grid
    if grid_np.size == 0:
        return []
        
    # --- Workflow ---
    
    # 1. Identify the end row of the horizontal zero-separator block above the bottom section.
    separator_end_row = find_separator_end_row(grid_np)
    
    # 2. Determine the starting row of the bottom section (the row after the separator).
    bottom_section_start_row = separator_end_row + 1
    
    # 3. Find the overall bounding box (min/max row/col) of *all* non-zero content within the bottom section.
    overall_bounds = find_bottom_section_content_bounds(grid_np, bottom_section_start_row)

    # If no non-zero content found in the bottom section, return empty grid
    if overall_bounds is None:
        return []
        
    min_row, max_row, overall_min_col, overall_max_col = overall_bounds

    # 4. Find the horizontal bounds (target_min_col, target_max_col) of the right-most pattern.
    target_max_col = overall_max_col # The right edge is fixed by the overall content.
    target_min_col = overall_min_col # Default left edge if no vertical separator is found.

    # Scan columns from right-to-left within the bottom section's row bounds 
    # to find the last vertical separator (a column of all zeros).
    for c in range(overall_max_col - 1, overall_min_col - 1 , -1):
        # Check if the column 'c' within the vertical bounds (min_row to max_row) is all zeros.
        column_slice = grid_np[min_row : max_row + 1, c]
        if np.all(column_slice == 0):
            # Found the last vertical separator column.
            # The right-most pattern starts at the column immediately to the right.
            target_min_col = c + 1 
            break # Stop searching once the last separator is found

    # 5. Extract the subgrid based on the final bounding box of the right-most pattern.
    # The row bounds are from the overall bottom section content.
    # The column bounds are specific to the right-most pattern.
    output_grid_np = grid_np[min_row : max_row + 1, target_min_col : target_max_col + 1]
    
    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid