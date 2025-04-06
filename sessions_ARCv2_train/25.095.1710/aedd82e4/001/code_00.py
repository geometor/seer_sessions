import copy

"""
Iterates through each cell of the input grid. If a cell contains the value 2, 
it checks all its orthogonal neighbors (up, down, left, right) that are within 
the grid boundaries. If all existing orthogonal neighbors have the value 0, 
the cell's value in the output grid is changed to 1. Otherwise, the cell's 
value remains unchanged (copied from the input to the output). Cells that 
do not initially have the value 2 are also copied unchanged.
"""

def check_neighbors_all_zero(grid: list[list[int]], r: int, c: int) -> bool:
    """
    Checks if all valid orthogonal neighbors of cell (r, c) in the grid are 0.

    Args:
        grid: The input grid.
        r: The row index of the cell.
        c: The column index of the cell.

    Returns:
        True if all existing orthogonal neighbors are 0, False otherwise.
        Returns True if the cell has no neighbors (e.g., 1x1 grid).
    """
    rows = len(grid)
    cols = len(grid[0])
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    
    has_neighbors = False
    all_zero = True

    for dr, dc in neighbor_offsets:
        nr, nc = r + dr, c + dc
        # Check if the neighbor is within grid bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            has_neighbors = True
            # If any neighbor is not 0, the condition fails
            if grid[nr][nc] != 0:
                all_zero = False
                break 
                
    # If there are no neighbors, the condition is vacuously true.
    # If there are neighbors, return whether all were zero.
    return all_zero

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the neighbor rule for cells with value 2.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy to preserve original values unless changed
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle empty columns

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell's value is 2
            if input_grid[r][c] == 2:
                # Check if all existing orthogonal neighbors are 0
                if check_neighbors_all_zero(input_grid, r, c):
                    # If condition met, change the value to 1 in the output grid
                    output_grid[r][c] = 1
            # No explicit 'else' needed because output_grid started as a copy.
            # Cells not equal to 2, or cells equal to 2 but failing the neighbor check,
            # retain their original value from the input_grid copy.

    return output_grid