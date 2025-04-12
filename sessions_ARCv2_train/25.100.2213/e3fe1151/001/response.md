```python
import copy
import math

"""
Transforms a 5x5 grid of digits based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Identify the central cross (row index 2 or column index 2). Cells in this cross remain unchanged.
3. Iterate through each cell (r, c) *not* in the central cross.
4. If the input cell value input_grid[r][c] is 7:
   a. Find its direct (up, down, left, right) neighbors within the grid boundaries.
   b. Get the values of these neighbors from the *input* grid.
   c. Filter out any neighbor values that are 7.
   d. If there are any non-7 neighbor values remaining, find the minimum value among them.
   e. Update the corresponding cell output_grid[r][c] with this minimum non-7 neighbor value.
   f. If all neighbors have the value 7, the output cell output_grid[r][c] remains 7.
5. If the input cell value input_grid[r][c] is *not* 7 and the cell is outside the central cross, it remains unchanged in the output grid.
6. Return the modified output grid.
"""

def get_neighbors(r: int, c: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """Gets the coordinates of valid neighbors (up, down, left, right) for a cell."""
    neighbors = []
    # Check Up
    if r > 0:
        neighbors.append((r - 1, c))
    # Check Down
    if r < rows - 1:
        neighbors.append((r + 1, c))
    # Check Left
    if c > 0:
        neighbors.append((r, c - 1))
    # Check Right
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the transformation rule to the input grid."""

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assuming a rectangular grid

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Skip cells in the central cross (row 2 or column 2)
            if r == 2 or c == 2:
                continue

            # Check if the cell value is 7
            if input_grid[r][c] == 7:
                # Find neighbors of the current cell (r, c)
                neighbor_coords = get_neighbors(r, c, rows, cols)

                # Get the values of the neighbors from the *input* grid
                neighbor_values = [input_grid[nr][nc] for nr, nc in neighbor_coords]

                # Filter out neighbor values that are 7
                non_seven_neighbors = [val for val in neighbor_values if val != 7]

                # If there are any non-7 neighbors, find the minimum
                if non_seven_neighbors:
                    min_val = min(non_seven_neighbors)
                    # Update the output grid with the minimum value
                    output_grid[r][c] = min_val
                # If all neighbors were 7, the value remains 7 (already copied)

            # If the cell value is not 7 and outside the cross, it remains unchanged (already copied)

    # Return the transformed grid
    return output_grid
```