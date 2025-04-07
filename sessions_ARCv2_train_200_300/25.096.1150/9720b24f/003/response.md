```python
import copy

"""
Creates an output grid where non-zero cells from the input are set to 0 
if they have any orthogonal neighbor (up, down, left, right) with a 
different non-zero value. Cells with value 0 remain 0. Non-zero cells 
that are only adjacent to cells with the same non-zero value or 0 remain 
unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on neighbor values.

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

    # 1. Create a new grid (output_grid) with the same dimensions as the input_grid.
    # We initialize it as a deep copy, then modify it.
    output_grid = copy.deepcopy(input_grid)

    # Define orthogonal neighbor offsets
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # 2. Iterate through each cell of the input_grid using its row index r and column index c.
    for r in range(rows):
        for c in range(cols):
            # 3. Get the value of the current cell in the input_grid.
            input_value = input_grid[r][c]

            # 4. If input_value is 0, the corresponding cell in output_grid is already 0 (from copy), so skip.
            if input_value == 0:
                continue

            # 5. If input_value is not 0, assume initially that the value should be kept.
            should_erase = False

            # 6. Define the coordinates of the orthogonal neighbors (done via offsets).
            # 7. For each neighbor coordinate (nr, nc):
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # 7a. Check if the neighbor coordinate is within the bounds of the input_grid.
                if 0 <= nr < rows and 0 <= nc < cols:
                    # 7b. If it is within bounds, get the neighbor's value from the original input grid.
                    neighbor_value = input_grid[nr][nc]

                    # 7c. Check if the neighbor_value is different from 0 AND different from the input_value.
                    if neighbor_value != 0 and neighbor_value != input_value:
                        # 7d. If both conditions are true, set should_erase = True and break.
                        should_erase = True
                        break # No need to check other neighbors for this cell

            # 8. After checking all neighbors (or breaking early), if should_erase is True, set output cell to 0.
            if should_erase:
                output_grid[r][c] = 0
            # 9. If should_erase is False, the output cell retains the input_value (already set by deepcopy).

    # 10. After iterating through all cells, return the output_grid.
    return output_grid
```