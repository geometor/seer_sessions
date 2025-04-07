import copy

"""
Transforms an input grid based on the neighboring values of '7' cells.

1.  Copies the input grid to an output grid.
2.  Iterates through each cell of the input grid.
3.  If a cell in the input grid contains the value 7:
    a.  Examines its 8 neighbors (up, down, left, right, diagonals) in the input grid.
    b.  Counts the number of neighbors with value 2 and value 5.
    c.  If there is at least one neighbor with value 5 and no neighbors with value 2, the corresponding cell in the output grid is set to 4.
    d.  If there is at least one neighbor with value 2 (regardless of whether there are neighbors with value 5), the corresponding cell in the output grid is set to 3.
    e.  Otherwise (no neighbors with 2 or 5), the cell remains 7.
4.  Cells in the input grid that are not 7 remain unchanged in the output grid.
"""

def get_neighbors(grid: list[list[int]], r: int, c: int) -> list[int]:
    """
    Gets the values of the 8 neighbors of a cell (r, c) in the grid.
    Handles boundary conditions.
    """
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    # Define the 8 possible relative positions for neighbors
    neighbor_coords = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    for dr, dc in neighbor_coords:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are within the grid bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append(grid[nr][nc])
    return neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid
    # This handles Rule_Object_Preservation and Rule_No_Change (initially)
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is a background cell (value 7)
            if input_grid[r][c] == 7:
                # Get the values of the neighbors from the *input* grid
                neighbors = get_neighbors(input_grid, r, c)

                # Count occurrences of 2 and 5 among neighbors
                count2 = neighbors.count(2)
                count5 = neighbors.count(5)

                # Apply transformation rules based on neighbor counts
                # Rule_2_to_3 and Rule_2_and_5_to_3 (priority given to 2)
                if count2 > 0:
                    output_grid[r][c] = 3
                # Rule_5_to_4 (only if no 2s are present)
                elif count5 > 0: # Implicitly count2 == 0 here because of the 'elif'
                    output_grid[r][c] = 4
                # Rule_No_Change: If count2 == 0 and count5 == 0, the cell
                # remains 7 as initialized in the copy.

    # Return the modified grid
    return output_grid