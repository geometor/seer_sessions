import numpy as np

"""
Identifies all 4x4 "hollow squares" (1-pixel colored border, 2x2 white center) 
in the input grid. Determines an arrangement direction (horizontal or vertical) 
based on the number and relative positions of these squares. Sorts the squares 
according to the arrangement direction (column-major for horizontal, row-major 
for vertical). Finally, constructs the output grid by concatenating the sorted 
squares side-by-side (horizontal) or stacked (vertical).

Arrangement Rules:
- If exactly two hollow squares are found:
    - Compare their top-left coordinates. Let the square with the smaller row 
      index (or smaller column index if rows are equal) be square1 and the 
      other be square2.
    - If the row index of square2 is greater than the row index of square1 
      plus 3 (i.e., square2 starts on a row completely below square1), the 
      arrangement is 'Vertical'.
    - Otherwise, the arrangement is 'Horizontal'.
- If the number of hollow squares is not two (0, 1, 3, or more), the 
  arrangement is 'Horizontal'.

Sorting Rules:
- Horizontal arrangement: Sort by column coordinate, then row coordinate.
- Vertical arrangement: Sort by row coordinate, then column coordinate.
"""

def is_hollow_square(subgrid):
    """Checks if a 4x4 numpy array is a hollow square."""
    if subgrid.shape != (4, 4):
        return False, -1 # Not 4x4

    border_color = subgrid[0, 0]
    if border_color == 0: # Border cannot be white
        return False, -1

    # Check border pixels
    for r in range(4):
        if subgrid[r, 0] != border_color or subgrid[r, 3] != border_color:
            return False, -1
    for c in range(1, 3): # Skip corners already checked
        if subgrid[0, c] != border_color or subgrid[3, c] != border_color:
            return False, -1

    # Check center pixels
    for r in range(1, 3):
        for c in range(1, 3):
            if subgrid[r, c] != 0: # Center must be white
                return False, -1

    return True, border_color

def find_hollow_squares(grid):
    """Finds all 4x4 hollow squares in the grid."""
    squares = []
    rows, cols = grid.shape
    for r in range(rows - 3):
        for c in range(cols - 3):
            subgrid = grid[r:r+4, c:c+4]
            is_hollow, _ = is_hollow_square(subgrid)
            if is_hollow:
                squares.append({'row': r, 'col': c, 'grid': subgrid})
    return squares

def transform(input_grid):
    """
    Transforms the input grid based on finding, sorting, and arranging 
    4x4 hollow squares.
    """
    input_np = np.array(input_grid)
    
    # 1. Scan the input grid to identify all 4x4 hollow squares
    found_squares = find_hollow_squares(input_np)

    if not found_squares:
        # Handle cases where no squares are found - return empty or based on specific rules
        # Based on examples, there are always squares. If none, maybe return empty 4x0 grid?
        return np.empty((4, 0), dtype=int) 

    # 2. Determine the arrangement direction
    arrangement = 'Horizontal' # Default
    if len(found_squares) == 2:
        # Sort temporarily by row then col to define s1 and s2 consistently
        temp_sorted = sorted(found_squares, key=lambda x: (x['row'], x['col']))
        s1 = temp_sorted[0]
        s2 = temp_sorted[1]
        # Check if s2 starts on a row completely below s1
        if s2['row'] > s1['row'] + 3:
            arrangement = 'Vertical'
        # else: arrangement remains 'Horizontal' (already set)
    # else: arrangement remains 'Horizontal' (already set)

    # 3. Sort the identified hollow squares based on the arrangement direction
    if arrangement == 'Horizontal':
        # Sort primarily by column, secondarily by row
        sorted_squares = sorted(found_squares, key=lambda x: (x['col'], x['row']))
    else: # arrangement == 'Vertical'
        # Sort primarily by row, secondarily by column
        sorted_squares = sorted(found_squares, key=lambda x: (x['row'], x['col']))
        
    # 4. Construct the output grid
    num_squares = len(sorted_squares)
    if arrangement == 'Horizontal':
        # Concatenate horizontally
        output_height = 4
        output_width = 4 * num_squares
        if num_squares == 0: # Should have been caught earlier, but safety check
             return np.empty((output_height, 0), dtype=int)
        # Extract just the grid arrays for concatenation
        square_grids = [sq['grid'] for sq in sorted_squares]
        output_grid = np.concatenate(square_grids, axis=1)
        
    else: # arrangement == 'Vertical'
        # Concatenate vertically
        output_height = 4 * num_squares
        output_width = 4
        if num_squares == 0: # Should have been caught earlier, but safety check
             return np.empty((0, output_width), dtype=int)
        # Extract just the grid arrays for concatenation
        square_grids = [sq['grid'] for sq in sorted_squares]
        output_grid = np.concatenate(square_grids, axis=0)

    # 5. Return the constructed grid 
    # Convert back to list of lists if required by the environment
    return output_grid.tolist()