```python
import copy

"""
Creates an output grid based on the input grid. Iterates through each cell 
in the input grid. If a cell has a non-zero value, it checks its orthogonal 
neighbors (up, down, left, right). If any neighbor has a non-zero value that 
is *smaller* than the current cell's value, then the current cell's value is 
set to 0 in the output grid. Otherwise (if all non-zero neighbors have values 
equal to or greater than the current cell, or if all neighbors are zero), 
the current cell's value is kept in the output grid. Cells with value 0 in 
the input grid remain 0 in the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on comparing cell values with their 
    smaller non-zero neighbors.

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

    # Initialize output_grid as a deep copy of the input grid.
    # We will modify this grid by setting cells to 0 where needed based on the rule.
    output_grid = copy.deepcopy(input_grid)

    # Define orthogonal neighbor offsets
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # Iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current cell from the original input grid
            input_value = input_grid[r][c]

            # Skip processing if the cell value is 0 (it remains 0 in the output)
            if input_value == 0:
                continue

            # Flag to determine if the current cell should be erased
            should_erase = False

            # Check orthogonal neighbors
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # Check if the neighbor coordinate is within the bounds of the input_grid
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Get the neighbor's value from the *original* input_grid
                    neighbor_value = input_grid[nr][nc]

                    # Check the core condition: erase if a neighbor has a smaller non-zero value
                    if 0 < neighbor_value < input_value:
                        # If such a neighbor exists, mark this cell for erasing
                        should_erase = True
                        # Break the inner loop (no need to check other neighbors)
                        break 
            
            # If the cell was marked for erasing, set its value to 0 in the output_grid
            if should_erase:
                output_grid[r][c] = 0
            # Otherwise, the value remains as it was copied initially from input_grid.

    # Return the modified output_grid
    return output_grid
```