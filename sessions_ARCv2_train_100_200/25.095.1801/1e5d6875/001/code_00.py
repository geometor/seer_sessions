import copy

"""
Transforms a grid of numbers based on the values of neighboring cells.

Specifically:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell of the input grid.
3. If the input cell value is 7:
   a. Examine the values of its 8 neighbors (N, NE, E, SE, S, SW, W, NW) in the input grid.
   b. If any neighbor has the value 2, set the corresponding cell in the output grid to 3.
   c. Else if any neighbor has the value 5, set the corresponding cell in the output grid to 4.
   d. Otherwise, the output cell value remains 7.
4. If the input cell value is not 7 (e.g., 2 or 5), the corresponding cell in the output grid retains its original value.
5. Return the transformed output grid.
"""

def get_neighbor_values(grid: list[list[int]], r: int, c: int) -> list[int]:
    """
    Retrieves the values of the 8 neighbors for a cell at (r, c).
    Handles boundary conditions by ignoring neighbors outside the grid.
    """
    neighbors = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Define the 8 relative neighbor offsets
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are within the grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append(grid[nr][nc])
            
    return neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is not empty
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This preserves non-7 values and provides the default for 7s that don't change.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the *input* grid is 7
            if input_grid[r][c] == 7:
                # Get the values of the neighbors from the *input* grid
                neighbor_vals = get_neighbor_values(input_grid, r, c)
                
                # Apply transformation rules based on neighbor values
                if 2 in neighbor_vals:
                    # If any neighbor is 2, change the output cell to 3
                    output_grid[r][c] = 3
                elif 5 in neighbor_vals:
                    # Else if any neighbor is 5, change the output cell to 4
                    output_grid[r][c] = 4
                # Otherwise, the output cell remains 7 (already set by the deepcopy)

    # Return the fully transformed grid
    return output_grid