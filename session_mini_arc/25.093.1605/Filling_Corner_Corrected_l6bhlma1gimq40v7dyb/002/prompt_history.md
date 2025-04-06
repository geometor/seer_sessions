
## train_1

**input:**
```
4 4 0 0 0
4 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
4 4 2 2 2
4 0 0 0 0
2 0 0 0 0
2 0 0 0 0
2 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 4 0 0 0
0 4 4 0 0
0 0 0 0 0
```


**output:**
```
0 2 0 0 0
0 2 0 0 0
0 4 0 0 0
0 4 4 2 2
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 4 4
0 0 0 0 4
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
2 2 2 4 4
0 0 0 0 4
0 0 0 0 2
0 0 0 0 2
```

Okay, analyzing the provided input-output examples.

**Perception:**

The task involves transforming a 2D grid of integers. The input grids contain the numbers 0 and 4. The output grids contain the numbers 0, 2, and 4. The core transformation seems to involve the number 4 influencing its neighboring cells. Specifically, cells containing 0 that are orthogonally adjacent (up, down, left, or right) to a cell containing 4 are changed to 2 in the output grid. The original 4s remain unchanged, as do 0s that are not adjacent to any 4s. The grid dimensions remain constant.

**Facts:**


```yaml
Schema:
  Objects:
    - Grid: A 2D array representing the input and output states.
      Properties:
        - cells: A list of lists containing integer values.
        - dimensions: (height, width) of the grid.
    - Cell: An individual element within the grid.
      Properties:
        - value: An integer (0, 2, or 4).
        - position: (row, column) coordinates within the grid.
        - neighbors: Orthogonally adjacent cells (up, down, left, right).
  Relationships:
    - Adjacency: Cells sharing a horizontal or vertical edge.
    - Source: Cells with value 4 act as sources for transformation.
    - Target: Cells with value 0 are potential targets for transformation.
    - Effect: Cells with value 2 are the result of the transformation.
  Actions:
    - Identify: Locate all cells with value 4 in the input grid.
    - Check Neighbors: For each cell with value 4, examine its orthogonal neighbors.
    - Conditional Update: If a neighbor cell exists within the grid boundaries and has a value of 0 in the input grid, change its value to 2 in the output grid.
    - Preserve: Maintain the original values of cells containing 4 and cells containing 0 that are not adjacent to any 4s.
```


**Natural Language Program:**

1.  Create a new grid (output) with the same dimensions as the input grid, initially copying all values from the input grid.
2.  Iterate through each cell (row `r`, column `c`) of the **input** grid.
3.  If the value of the input cell `input[r][c]` is 4:
    1.  Check the cell directly above (`r-1`, `c`): If this position is within the grid boundaries AND the value at `input[r-1][c]` is 0, set the value of the corresponding cell in the **output** grid (`output[r-1][c]`) to 2.
    2.  Check the cell directly below (`r+1`, `c`): If this position is within the grid boundaries AND the value at `input[r+1][c]` is 0, set the value of the corresponding cell in the **output** grid (`output[r+1][c]`) to 2.
    3.  Check the cell to the left (`r`, `c-1`): If this position is within the grid boundaries AND the value at `input[r][c-1]` is 0, set the value of the corresponding cell in the **output** grid (`output[r][c-1]`) to 2.
    4.  Check the cell to the right (`r`, `c+1`): If this position is within the grid boundaries AND the value at `input[r][c+1]` is 0, set the value of the corresponding cell in the **output** grid (`output[r][c+1]`) to 2.
4.  After checking all cells in the input grid, return the final output grid.
```python
import copy

"""
Transforms a 2D grid by changing the value of cells containing 0 to 2 if they are orthogonally adjacent (up, down, left, or right) to a cell containing 4. Cells containing 4 and 0s not adjacent to any 4 remain unchanged.
"""

def is_within_bounds(r, c, height, width):
  """Checks if the given row and column are within the grid boundaries."""
  return 0 <= r < height and 0 <= c < width

def transform(input_grid):
  """
  Applies the transformation rule to the input grid.

  Args:
    input_grid: A list of lists representing the input 2D grid.

  Returns:
    A list of lists representing the transformed output 2D grid.
  """
  # Get grid dimensions
  height = len(input_grid)
  if height == 0:
    return []
  width = len(input_grid[0])
  if width == 0:
    return [[] for _ in range(height)]

  # Initialize output_grid as a deep copy of the input grid
  # This ensures that original 4s and non-adjacent 0s are preserved,
  # and we check conditions based on the original input state.
  output_grid = copy.deepcopy(input_grid)

  # Iterate through each cell of the input grid
  for r in range(height):
    for c in range(width):
      # Check if the current cell in the *input* grid contains a 4
      if input_grid[r][c] == 4:
        # Define potential orthogonal neighbors (dr, dc offsets)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        # Check each neighbor
        for nr, nc in neighbors:
          # Check if the neighbor is within grid bounds
          if is_within_bounds(nr, nc, height, width):
            # Check if the neighbor cell in the *input* grid is 0
            if input_grid[nr][nc] == 0:
              # If conditions met, update the corresponding cell in the *output* grid to 2
              output_grid[nr][nc] = 2

  # Return the final transformed grid
  return output_grid
```
