import numpy as np

"""
Transforms an input grid based on the proximity of orange (7) pixels to red (2) and gray (5) pixels.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell (row, column) of the input grid.
3. If the color of the cell in the input grid is orange (7):
    a. Check all 8 neighboring cells (including diagonals).
    b. Determine if any neighbor has the color red (2). Let this be `is_near_red`.
    c. Determine if any neighbor has the color gray (5). Let this be `is_near_gray`.
    d. If `is_near_red` is true, change the color of the cell in the output grid to green (3).
    e. Else if `is_near_gray` is true (and `is_near_red` is false), change the color of the cell in the output grid to yellow (4).
    f. Otherwise (orange cell not near red or gray), it remains orange (7).
4. Cells that were originally red (2) or gray (5) remain unchanged.
5. Return the final output grid.
"""

def _check_neighbors(grid, r, c):
    """
    Checks the 8 neighbors of a cell (r, c) for red (2) and gray (5) pixels.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.

    Returns:
        tuple: (is_near_red, is_near_gray) - booleans indicating presence of neighbors.
    """
    height, width = grid.shape
    is_near_red = False
    is_near_gray = False
    # Define 8 neighboring offsets (row, col)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    for dr, dc in neighbors:
        nr, nc = r + dr, c + dc
        # Check if neighbor is within grid bounds
        if 0 <= nr < height and 0 <= nc < width:
            neighbor_color = grid[nr, nc]
            if neighbor_color == 2: # red
                is_near_red = True
            elif neighbor_color == 5: # gray
                is_near_gray = True
            # Optimization is tricky due to priority, so check all neighbors
            # If we find red, we know the final color will be green anyway (if the cell is orange)
            # but we still need is_near_gray for the yellow case.
    return is_near_red, is_near_gray


def transform(input_grid):
    """
    Applies the color transformation based on neighbor proximity.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is orange (7)
            if input_np[r, c] == 7:
                # Check the neighbors of the current cell
                is_near_red, is_near_gray = _check_neighbors(input_np, r, c)

                # Apply transformation rules based on neighbors
                if is_near_red:
                    # If near red, change to green (3)
                    output_grid[r, c] = 3
                elif is_near_gray:
                    # If near gray BUT NOT near red, change to yellow (4)
                    output_grid[r, c] = 4
                # Otherwise (orange cell not near red or gray), it remains orange (7) - no change needed

    # Return the final output grid
    return output_grid.tolist() # Convert back to list of lists if required by ARC standard