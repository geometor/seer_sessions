import copy

"""
1. Identify the single contiguous block of non-white pixels in the input grid. Determine its color (C) and bounding box (min_row, max_row, min_col, max_col).
2. Determine the height (H) and width (W) of the input grid.
3. Calculate the middle row index of the object: `mid_row = (min_row + max_row) // 2`.
4. Calculate the middle column index of the object: `mid_col = (min_col + max_col) // 2`.
5. Create a copy of the input grid to serve as the output grid.
6. Compare the grid width (W) and height (H):
    *   If W > H (grid is wider than tall):
        *   Iterate through each column index `c` from `max_col + 1` up to `W - 1`.
        *   Set the pixel value at `(mid_row, c)` in the output grid to color C.
    *   Else (if H >= W, grid is taller than or same height as width):
        *   Iterate through each row index `r` from `max_row + 1` up to `H - 1`.
        *   Set the pixel value at `(r, mid_col)` in the output grid to color C.
7. Return the modified output grid.
"""

def find_object_properties(grid: list[list[int]]) -> tuple[int, int, int, int, int] | None:
    """
    Finds the first non-background object and returns its color and bounding box.
    Assumes a single contiguous non-background object.
    """
    height = len(grid)
    width = len(grid[0])
    object_color = -1
    object_pixels = []

    # Find the first non-background pixel and its color
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                object_color = grid[r][c]
                break
        if object_color != -1:
            break
    
    if object_color == -1:
        return None # No object found

    # Find all pixels of the object color to determine the bounding box
    min_row, max_row = height, -1
    min_col, max_col = width, -1
    for r in range(height):
        for c in range(width):
            if grid[r][c] == object_color:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    if min_row > max_row or min_col > max_col: # Should not happen if object_color was found
         return None
         
    return object_color, min_row, max_row, min_col, max_col


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extending a line from the middle
    of the single object to the edge of the grid. The direction
    of the line depends on the grid's aspect ratio.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(output_grid)
    if height == 0:
        return output_grid # Handle empty grid
    width = len(output_grid[0])
    if width == 0:
        return output_grid # Handle empty row

    # 1. Identify the object and its properties
    object_props = find_object_properties(output_grid)
    if object_props is None:
        return output_grid # No object found, return copy of input

    object_color, min_row, max_row, min_col, max_col = object_props

    # 3. Calculate middle row index of the object
    mid_row = (min_row + max_row) // 2
    
    # 4. Calculate middle column index of the object
    mid_col = (min_col + max_col) // 2

    # 6. Compare grid width and height and draw the line
    if width > height:
        # Grid is wider than tall: draw horizontal line
        # Iterate from the column after the object to the right edge
        for c in range(max_col + 1, width):
            # Check bounds just in case, though mid_row should be valid
            if 0 <= mid_row < height:
                 output_grid[mid_row][c] = object_color
    else:
        # Grid is taller than or same height as width: draw vertical line
        # Iterate from the row below the object to the bottom edge
        for r in range(max_row + 1, height):
             # Check bounds just in case, though mid_col should be valid
            if 0 <= mid_col < width:
                output_grid[r][mid_col] = object_color

    # 7. Return the modified output grid
    return output_grid