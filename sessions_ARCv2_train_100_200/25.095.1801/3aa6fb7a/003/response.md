```python
import copy

"""
Transforms an input grid based on the following rule:
Iterate through each cell of the input grid.
If the input cell's value is 8, keep it as 8 in the output grid.
If the input cell's value is 0, count its 8 neighbors (horizontally, vertically, and diagonally) in the input grid.
If the count of 8-neighbors is exactly 3, set the corresponding output cell's value to 1.
Otherwise (if the input cell is 0 and the neighbor count is not 3), keep the output cell's value as 0.
"""

def count_neighbors(grid: list[list[int]], r: int, c: int, target_value: int) -> int:
    """
    Counts the neighbors of cell (r, c) with the target_value.
    Considers 8 neighbors: horizontal, vertical, and diagonal.
    """
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    # Iterate through the 3x3 neighborhood centered at (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor coordinates are within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # If the neighbor cell has the target value, increment count
                if grid[nr][nc] == target_value:
                    count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    A cell with value 0 becomes 1 if it has exactly three neighbors with value 8 in the input grid.
    Cells with value 8 remain unchanged.
    Other cells with value 0 remain 0.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid.
    # This handles the cases where 8s remain 8s and 0s remain 0s by default.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current cell in the *input* grid
            input_value = input_grid[r][c]

            # Check if the input cell's value is 0
            if input_value == 0:
                # Count neighbors with value 8 in the input grid
                neighbor_count_8 = count_neighbors(input_grid, r, c, 8)
                
                # Apply the rule: if the count is exactly 3, change the cell in the output grid to 1
                if neighbor_count_8 == 3:
                    output_grid[r][c] = 1
            # If input_value is 8, output_grid[r][c] is already 8 from the deepcopy.
            # If input_value is 0 and neighbor_count_8 is not 3, output_grid[r][c] is already 0 from the deepcopy.

    # Return the completed output grid
    return output_grid
```