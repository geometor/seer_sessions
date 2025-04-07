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
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid.
    # We will modify this grid by setting cells to 0 where needed.
    output_grid = copy.deepcopy(input_grid)

    # Define orthogonal neighbor offsets
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # Iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current cell in the input_grid
            input_value = input_grid[r][c]

            # Skip processing if the cell value is 0 (it's already correct in output)
            if input_value == 0:
                continue

            # Assume initially that the value should not be erased
            should_erase = False

            # Check orthogonal neighbors
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # Check if the neighbor coordinate is within the bounds of the input_grid
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Get the neighbor's value from the *original* input_grid
                    neighbor_value = input_grid[nr][nc]

                    # Check if the neighbor_value is different from 0 AND different from the input_value
                    if neighbor_value != 0 and neighbor_value != input_value:
                        # If such a neighbor exists, mark this cell for erasing
                        should_erase = True
                        # Break the inner loop (no need to check other neighbors)
                        break 
            
            # If the cell was marked for erasing, set its value to 0 in the output_grid
            if should_erase:
                output_grid[r][c] = 0
            # Otherwise, the value remains as it was copied initially.

    # Return the modified output_grid
    return output_grid
```