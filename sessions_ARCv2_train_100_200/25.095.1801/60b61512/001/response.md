```python
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the following rule:
    If a cell in the input grid has a value of 0 and is adjacent (including diagonals) 
    to at least one cell with a value of 4, its value is changed to 7 in the output grid. 
    All other cells retain their original values.
    """
    # Get the dimensions of the grid
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize the output grid as a deep copy of the input grid
    # This handles the invariant cases (cells with 4 or 0s not adjacent to 4s)
    output_grid = copy.deepcopy(input_grid)

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the input grid is 0
            if input_grid[r][c] == 0:
                found_4_neighbor = False
                # Examine the 8 neighboring cells
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the input grid has the value 4
                        if input_grid[nr][nc] == 4:
                            found_4_neighbor = True
                            break  # Found a 4, no need to check other neighbors

                # If at least one neighbor has the value 4, update the output grid cell to 7
                if found_4_neighbor:
                    output_grid[r][c] = 7
            # If the input cell is not 0 (i.e., it's 4), it remains unchanged 
            # in the output grid because we initialized output_grid as a copy.

    # Return the final transformed grid
    return output_grid
```