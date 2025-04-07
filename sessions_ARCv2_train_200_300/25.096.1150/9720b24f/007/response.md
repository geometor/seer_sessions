```python
import copy
import numpy as np # numpy is commonly available, useful for grid ops if needed, but copy is sufficient here

"""
Creates an output grid based on the input grid. Iterates through each cell 
in the input grid. If a cell has a non-zero value, it checks its orthogonal 
neighbors (up, down, left, right). If any neighbor has a non-zero value that 
is *different* from the current cell's value, then the current cell's value is 
set to 0 in the output grid. Otherwise (if all neighbors are zero or have the 
same non-zero value as the current cell), the current cell's value is kept 
in the output grid. Cells with value 0 in the input grid remain 0 in the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by erasing non-zero cells that have 
    orthogonally adjacent neighbors with different non-zero values.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        # Handle empty rows case
        return [[] for _ in range(rows)]

    # 1. Create a new grid (output_grid) as a copy of the input_grid.
    # We initialize it as a deep copy, then modify it based on the rules.
    output_grid = copy.deepcopy(input_grid)

    # 6a. Define the relative coordinates for neighbors.
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # 3. Iterate through each cell of the input_grid.
    for r in range(rows):
        for c in range(cols):
            # 4. Get the value of the current cell from the *original* input_grid.
            input_value = input_grid[r][c]

            # 5. If input_value is 0, skip (output already has 0).
            if input_value == 0:
                continue

            # 6. If input_value is not 0, check its orthogonal neighbors.
            # 6b. Initialize a flag to track if the cell needs erasure.
            should_erase = False

            # 6c. For each relative neighbor coordinate:
            for dr, dc in neighbor_offsets:
                # 6ci. Calculate the neighbor's absolute coordinates.
                nr, nc = r + dr, c + dc

                # 6cii. Check if the neighbor coordinate is within the valid bounds.
                if 0 <= nr < rows and 0 <= nc < cols:
                    # 6ciii. Get the neighbor's value from the *original* input_grid.
                    neighbor_value = input_grid[nr][nc]

                    # 6civ. Check if the neighbor represents a conflict.
                    if neighbor_value != 0 and neighbor_value != input_value:
                        # 6cv. If a conflict exists, mark for erasure and stop checking neighbors.
                        should_erase = True
                        break # Exit the neighbor checking loop for this cell

            # 7. After checking neighbors, if marked for erasure, update the output grid.
            if should_erase:
                output_grid[r][c] = 0
            # (Otherwise, output_grid[r][c] retains its copied value).

    # 8. Return the modified output_grid.
    return output_grid
```