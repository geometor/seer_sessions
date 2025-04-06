```python
import copy

def transform(input_grid):
    """
    Transforms the input grid based on a neighbor propagation rule.
    A cell in the output grid becomes 4 if it was already 4 in the input grid,
    or if it was 0 in the input grid and had at least one orthogonal neighbor
    (up, down, left, right) with the value 4 in the input grid. Otherwise,
    the cell retains its original value (which would be 0 if it wasn't 4 initially
    and had no '4' neighbors).
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input_grid
    # This ensures we read from the original state while modifying the new state
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the *input* grid is 0
            if input_grid[r][c] == 0:
                # Define potential orthogonal neighbor coordinates
                neighbors = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]

                # Check each neighbor
                has_active_neighbor = False
                for nr, nc in neighbors:
                    # Check if the neighbor coordinates are within grid bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the *input* grid has value 4
                        if input_grid[nr][nc] == 4:
                            has_active_neighbor = True
                            break  # Found an active neighbor, no need to check further

                # If any valid orthogonal neighbor was 4, update the output grid cell to 4
                if has_active_neighbor:
                    output_grid[r][c] = 4

    # Return the modified grid
    return output_grid
```