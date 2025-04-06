"""
Transforms an input grid based on the following rules:
1.  Identifies horizontal rows and vertical columns consisting entirely of the number 4 (Separators).
2.  Uses these Separators and grid boundaries to define distinct rectangular Cells, assigning logical coordinates (row_index, column_index) to each.
3.  Iterates through each Cell (TargetCell). If a TargetCell contains the number 1:
    a.  It attempts to find a PaintColor.
    b.  First, it checks the Cell logically above it (same column_index, row_index - 1). If this cell exists and contains exactly one unique number other than 0, 1, or 4, that number is chosen as the PaintColor.
    c.  If no PaintColor is found above, it checks the Cell logically to the left (same row_index, column_index - 1). If this cell exists and contains exactly one unique number other than 0, 1, or 4, that number is chosen as the PaintColor.
    d.  If a PaintColor is determined, all instances of the number 1 within the TargetCell in the output grid are replaced by the PaintColor.
    e.  If no PaintColor is found, the 1s in the TargetCell remain unchanged.
4.  Numbers 0 and 4, and Cells not containing 1, remain unchanged in the output grid.
"""

import numpy as np
from typing import List, Tuple, Optional, Set, Dict

# --- Helper Functions ---

def _find_separators(grid: np.ndarray) -> Tuple[List[int], List[int]]:
    """Finds the indices of rows and columns that consist entirely of the separator value (4)."""
    rows, cols = grid.shape
    separator_rows = [r for r in range(rows) if np.all(grid[r, :] == 4)]
    separator_cols = [c for c in range(cols) if np.all(grid[:, c] == 4)]
    return separator_rows, separator_cols

def _get_cell_map(grid_shape: Tuple[int, int], sep_rows: List[int], sep_cols: List[int]) -> Dict[Tuple[int, int], Tuple[int, int, int, int]]:
    """
    Determines the boundaries (start_row, end_row, start_col, end_col)
    and logical coordinates (ri, ci) of each cell, returning a map:
    {(ri, ci): (r_start, r_end, c_start, c_end)}
    """
    rows, cols = grid_shape
    cell_map = {} # Stores {(ri, ci): (r_start, r_end, c_start, c_end)}

    # Define the start and end points for row sections based on separators
    row_starts = [0] + [r + 1 for r in sep_rows]
    row_ends = [r for r in sep_rows] + [rows]

    # Define the start and end points for column sections based on separators
    col_starts = [0] + [c + 1 for c in sep_cols]
    col_ends = [c for c in sep_cols] + [cols]

    # Assign logical coordinates and map them to boundaries
    ri = 0
    for r_start, r_end in zip(row_starts, row_ends):
        if r_start >= r_end: continue # Skip empty sections
        ci = 0
        for c_start, c_end in zip(col_starts, col_ends):
            if c_start >= c_end: continue # Skip empty sections
            cell_map[(ri, ci)] = (r_start, r_end, c_start, c_end)
            ci += 1
        ri += 1

    return cell_map

def _get_cell_subgrid(grid: np.ndarray, boundaries: Tuple[int, int, int, int]) -> np.ndarray:
    """Extracts the subgrid corresponding to the given cell boundaries."""
    r_start, r_end, c_start, c_end = boundaries
    return grid[r_start:r_end, c_start:c_end]

def _find_unique_source_color(cell_subgrid: np.ndarray) -> Optional[int]:
    """
    Finds if a cell contains exactly one unique number other than 0, 1, or 4.
    Returns that number if found, otherwise None.
    """
    # Get unique values present in the cell
    unique_values = np.unique(cell_subgrid)
    # Filter out background (0), target (1), and separator (4) to find potential source colors
    source_colors: Set[int] = {val for val in unique_values if val not in {0, 1, 4}}
    # Return the color if exactly one unique source color exists
    if len(source_colors) == 1:
        return source_colors.pop()
    return None # Return None if zero or more than one source color found

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Identify separator rows and columns (filled with 4s)
    sep_rows, sep_cols = _find_separators(grid)

    # Determine the boundaries and logical coordinates of all cells
    cell_map = _get_cell_map((rows, cols), sep_rows, sep_cols)

    # Iterate through each cell using its logical coordinates (ri, ci)
    for (ri, ci), target_boundaries in cell_map.items():
        # Extract the subgrid for the current target cell from the *original* input grid
        target_cell_subgrid = _get_cell_subgrid(grid, target_boundaries)

        # Only process cells that contain the target number '1'
        if 1 not in target_cell_subgrid:
            continue

        # Attempt to find the paint color, prioritizing vertical then horizontal adjacency
        paint_color: Optional[int] = None

        # 1. Check Cell Above (Vertical Priority)
        coords_above = (ri - 1, ci)
        if coords_above in cell_map: # Check if a cell exists at these logical coordinates
            source_boundaries = cell_map[coords_above]
            source_subgrid = _get_cell_subgrid(grid, source_boundaries)
            paint_color = _find_unique_source_color(source_subgrid)

        # 2. Check Cell Left (Horizontal Priority - only if color not found above)
        if paint_color is None:
            coords_left = (ri, ci - 1)
            if coords_left in cell_map: # Check if a cell exists at these logical coordinates
                source_boundaries = cell_map[coords_left]
                source_subgrid = _get_cell_subgrid(grid, source_boundaries)
                paint_color = _find_unique_source_color(source_subgrid)

        # 3. Apply Paint Color if found
        if paint_color is not None:
            # Get the boundaries of the target cell
            tr_start, tr_end, tc_start, tc_end = target_boundaries
            # Create a boolean mask identifying '1's within the target cell in the *original* subgrid
            target_mask = (target_cell_subgrid == 1)
            # Update the corresponding locations in the *output* grid using the determined paint color
            output_grid[tr_start:tr_end, tc_start:tc_end][target_mask] = paint_color
            # Note: Cells without a determined paint color remain unchanged as per the initial copy.

    # Convert the final numpy array back to a list of lists for the return value
    return output_grid.tolist()