import copy

"""
Transforms an input grid based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through the cells within the inner region defined by the outer frame (rows 3-9, columns 4-10).
3. If a cell in the input grid within this region is 0:
    a. Check its four orthogonal neighbors (up, down, left, right) in the input grid.
    b. If any neighbor has the value 3, set the corresponding cell in the output grid to 4.
    c. Otherwise (if none of the neighbors have the value 3), set the corresponding cell in the output grid to 2.
4. Cells outside this inner region, frame cells (value 3), and internal obstacle cells (value 3) remain unchanged.
5. Return the modified output grid.
"""

def check_neighbors_for_value(grid: list[list[int]], r: int, c: int, value: int) -> bool:
    """
    Checks if any orthogonal neighbor of grid[r][c] has the specified value.

    Args:
        grid: The input grid.
        r: Row index of the cell.
        c: Column index of the cell.
        value: The value to check for in neighbors.

    Returns:
        True if any neighbor has the value, False otherwise.
    """
    rows = len(grid)
    cols = len(grid[0])
    neighbors = []
    # Check up
    if r > 0:
        neighbors.append(grid[r-1][c])
    # Check down
    if r < rows - 1:
        neighbors.append(grid[r+1][c])
    # Check left
    if c > 0:
        neighbors.append(grid[r][c-1])
    # Check right
    if c < cols - 1:
        neighbors.append(grid[r][c+1])

    return value in neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Fills internal '0' cells with '2' or '4' based on adjacency to '3' cells.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Determine the bounds of the inner region to check
    # Based on examples, the outer frame uses rows 2-10 and cols 3-11.
    # The inner region where 0s can be replaced is rows 3-9 and cols 4-10.
    min_row, max_row = 3, 9  # Inclusive range for rows to potentially change
    min_col, max_col = 4, 10 # Inclusive range for columns to potentially change

    # Iterate through each cell potentially inside the frame
    for r in range(min_row, max_row + 1):
        # Check row bounds just in case grid size varies, although examples are fixed
        if r >= rows: continue 
        for c in range(min_col, max_col + 1):
             # Check col bounds
            if c >= cols: continue

            # Check if the cell in the *input* grid is an internal empty cell (value 0)
            if input_grid[r][c] == 0:
                # Check its orthogonal neighbors in the *input* grid for the value 3
                if check_neighbors_for_value(input_grid, r, c, 3):
                    # If any neighbor is 3, set the output cell to 4
                    output_grid[r][c] = 4
                else:
                    # If no neighbor is 3, set the output cell to 2
                    output_grid[r][c] = 2
            # If input_grid[r][c] is not 0 (e.g., it's a 3 - part of frame or obstacle), 
            # it remains unchanged because output_grid was initialized as a copy.

    # Cells outside the iterated range (r, c) also remain unchanged.
    return output_grid