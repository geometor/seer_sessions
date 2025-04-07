import numpy as np
from typing import List, Tuple, Optional

"""
Transforms the grid by filling horizontal strips based on the color found
in the leftmost quadrant of each strip, preserving separator lines.

1. Identifies a unique 'separator_color' that forms complete horizontal and 
   vertical lines.
2. Finds the row and column indices of these separator lines.
3. Defines horizontal strips as the regions between consecutive horizontal 
   separator lines (or grid edges).
4. For each horizontal strip:
   a. Identifies the 'leftmost quadrant' (from column 0 to the first vertical 
      separator line or grid edge).
   b. Finds the first 'source_color' (non-background, non-separator) within 
      this leftmost quadrant.
   c. Fills all cells within the entire horizontal strip (full width) in the 
      output grid with this 'source_color', *unless* the corresponding cell 
      in the input grid contains the 'separator_color'.
"""

def find_separator_color(grid: np.ndarray) -> Optional[int]:
    """
    Finds the unique non-zero color that forms complete horizontal rows 
    AND complete vertical columns. Returns None if no such unique color exists.
    """
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return None
        
    color_in_full_row = {} # color -> set of row indices
    color_in_full_col = {} # color -> set of col indices

    # Check horizontal lines
    for r in range(rows):
       # Check if all elements in the row are the same and not zero
       first_val = grid[r, 0]
       if first_val != 0 and np.all(grid[r, :] == first_val):
           color = first_val
           if color not in color_in_full_row: color_in_full_row[color] = set()
           color_in_full_row[color].add(r)

    # Check vertical lines
    for c in range(cols):
        # Check if all elements in the col are the same and not zero
        first_val = grid[0, c]
        if first_val != 0 and np.all(grid[:, c] == first_val):
           color = first_val
           if color not in color_in_full_col: color_in_full_col[color] = set()
           color_in_full_col[color].add(c)

    # Find colors present in both full rows and full columns
    common_colors = set(color_in_full_row.keys()).intersection(set(color_in_full_col.keys()))

    if len(common_colors) == 1:
        return common_colors.pop()
    elif len(common_colors) > 1:
         # Heuristic for ambiguity: return the one with most lines? Or smallest value?
         # Based on ARC tasks, usually there's a single clear separator if this pattern holds.
         # Let's return the smallest color value as a tie-breaker for now.
         print(f"Warning: Multiple potential separator colors found: {common_colors}. Choosing smallest.")
         return min(common_colors)
         
    return None # No single color forms both full rows and columns

def find_separator_lines(grid: np.ndarray, separator_color: int) -> Tuple[List[int], List[int]]:
    """Finds the indices of rows and columns completely filled with the separator color."""
    rows, cols = grid.shape
    h_lines = [r for r in range(rows) if np.all(grid[r, :] == separator_color)]
    v_lines = [c for c in range(cols) if np.all(grid[:, c] == separator_color)]
    return h_lines, v_lines

def find_source_color(grid_slice: np.ndarray, separator_color: int, background_color: int = 0) -> Optional[int]:
    """
    Finds the first non-background, non-separator color in the given grid slice.
    Searches row by row, then column by column.
    Returns the color if found, otherwise None.
    """
    if grid_slice.size == 0: # Handle empty slice case
        return None
        
    rows, cols = grid_slice.shape
    for r in range(rows):
        for c in range(cols):
            color = grid_slice[r, c]
            if color != background_color and color != separator_color:
                return color
    return None # No source color found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    if rows == 0 or cols == 0:
        return input_grid # Return empty or invalid grid as is

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    background_color = 0

    # 1. Identify the separator_color
    separator_color = find_separator_color(grid)
    if separator_color is None:
        # If no separator color is found based on the strict definition,
        # return the original grid. (Or apply alternative logic if needed)
        print("Warning: No unique separator color found. Returning original grid.")
        return input_grid

    # 2. Identify Separator Locations
    h_lines, v_lines = find_separator_lines(grid, separator_color)

    # 3. Define Horizontal Boundaries
    h_boundaries = sorted(list(set([0] + h_lines + [rows])))

    # 4. Iterate through Horizontal Strips
    for i in range(len(h_boundaries) - 1):
        strip_start_row = h_boundaries[i]
        strip_end_row = h_boundaries[i+1]

        # 4a. Determine the actual content rows for the strip
        # If the strip starts *on* a separator line, content begins on the next row
        content_start_row = strip_start_row + 1 if strip_start_row in h_lines else strip_start_row
        
        # 4b. Check for valid content strip (must have height > 0)
        if content_start_row >= strip_end_row:
            continue # This is just a separator line row or an empty gap

        # 4c. Define the Leftmost Quadrant column range
        col_start = 0
        col_end = cols # Default to full width
        for v_line_idx in sorted(v_lines):
            if v_line_idx > 0: # Find the first vertical separator after column 0
                col_end = v_line_idx
                break
        
        # Ensure quadrant dimensions are valid before slicing
        if content_start_row >= strip_end_row or col_start >= col_end:
             print(f"Warning: Skipping strip {i+1} due to invalid leftmost quadrant dimensions.")
             continue

        # 4d. Find the source_color in the leftmost quadrant
        leftmost_quadrant_slice = grid[content_start_row:strip_end_row, col_start:col_end]
        source_color = find_source_color(leftmost_quadrant_slice, separator_color, background_color)

        # If no source color is found in the leftmost quadrant, skip filling this strip
        # (Based on examples, a source color seems expected if the strip has content)
        if source_color is None:
            print(f"Warning: No source color found for strip {i+1} (Rows {content_start_row}-{strip_end_row-1}). Skipping fill.")
            continue

        # 4e. Fill the Strip in Output Grid
        # Iterate through all cells within the content rows of the current strip
        for r in range(content_start_row, strip_end_row):
            for c in range(cols):
                # Check the corresponding cell in the *input* grid
                # Only update the output cell if the input cell is NOT the separator color
                if grid[r, c] != separator_color:
                    output_grid[r, c] = source_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()