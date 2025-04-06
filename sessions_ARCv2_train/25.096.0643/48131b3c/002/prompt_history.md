
## train_1

**input:**
```
7 0
0 7
```


**output:**
```
0 7 0 7
7 0 7 0
0 7 0 7
7 0 7 0
```


## train_2

**input:**
```
0 8 0
8 0 8
0 0 0
```


**output:**
```
8 0 8 8 0 8
0 8 0 0 8 0
8 8 8 8 8 8
8 0 8 8 0 8
0 8 0 0 8 0
8 8 8 8 8 8
```


## train_3

**input:**
```
4 0 0 0
0 4 4 4
0 0 4 0
0 4 0 0
```


**output:**
```
0 4 4 4 0 4 4 4
4 0 0 0 4 0 0 0
4 4 0 4 4 4 0 4
4 0 4 4 4 0 4 4
0 4 4 4 0 4 4 4
4 0 0 0 4 0 0 0
4 4 0 4 4 4 0 4
4 0 4 4 4 0 4 4
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Input/Output Data:** Both inputs and outputs are grids (matrices) containing single-digit integers.
2.  **Grid Structure:** The grids are represented with space-separated values within rows and newline characters separating rows.
3.  **Dimensionality Change:** The output grid consistently has twice the number of rows and twice the number of columns compared to the input grid. For an input of N rows and M columns, the output is 2N rows and 2M columns.
4.  **Pattern Repetition:** The output grid appears to be constructed by repeating a smaller pattern four times, arranged in a 2x2 configuration.
5.  **Core Transformation:** The repeated pattern in the output is not identical to the input grid but seems closely related. Comparing the input rows to the rows within one quadrant of the output suggests a rearrangement of the input rows. Specifically, the first two rows of the input grid appear to be swapped in the repeating pattern, while any subsequent rows retain their original relative order.

**YAML Facts:**

```
yaml
task: Grid Transformation

input_elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - dimensions: N rows, M columns (variable)

output_elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - dimensions: 2*N rows, 2*M columns (derived from input)

transformation:
  - action: row_rearrangement
    input: input grid
    output: intermediate grid (T)
    details:
      - The first row of T is the second row of the input grid.
      - The second row of T is the first row of the input grid.
      - Subsequent rows (row 3 to N) of T are identical to the corresponding rows (row 3 to N) of the input grid.
  - action: tiling
    input: intermediate grid (T)
    output: final output grid
    details:
      - The intermediate grid T is tiled 2 times horizontally and 2 times vertically.
      - The output grid is composed of four copies of T arranged as:
          T T
          T T

relationships:
  - output grid dimensions are double the input grid dimensions in both rows and columns.
  - The output grid is a 2x2 tiling of a modified version of the input grid.
  - The modification involves swapping the first two rows of the input grid.

```python
import copy

"""
Transforms an input grid of integers (N rows, M columns) into an output grid (2N rows, 2M columns).
The transformation involves two steps:
1. Row Rearrangement: An intermediate grid is created by swapping the first two rows of the input grid. 
   If the input grid has fewer than two rows, the intermediate grid is identical to the input.
2. Tiling: The final output grid is constructed by tiling the intermediate grid in a 2x2 pattern. 
   This means the intermediate grid is repeated twice horizontally and twice vertically.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the row swap and 2x2 tiling transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed output grid.
    """

    # --- Step 0: Handle edge cases and get dimensions ---
    num_rows = len(input_grid)
    if num_rows == 0:
        return []  # Return empty list for empty input grid

    num_cols = len(input_grid[0]) if num_rows > 0 else 0
    if num_cols == 0:
         # Return a grid with doubled rows but still zero columns
        return [[] for _ in range(num_rows * 2)]

    # --- Step 1: Row Rearrangement (Create Intermediate Grid) ---
    # Create a deep copy to avoid modifying the original input grid
    intermediate_grid = copy.deepcopy(input_grid)

    # Swap the first two rows if the grid has at least two rows
    if num_rows >= 2:
        intermediate_grid[0], intermediate_grid[1] = intermediate_grid[1], intermediate_grid[0]
        
    # --- Step 2: Tiling (Create Output Grid) ---
    # Calculate output dimensions
    output_num_rows = num_rows * 2
    output_num_cols = num_cols * 2

    # Initialize the output grid (e.g., with zeros, will be overwritten)
    output_grid = [[0] * output_num_cols for _ in range(output_num_rows)]

    # Fill the output grid by tiling the intermediate grid
    for r in range(output_num_rows):
        for c in range(output_num_cols):
            # Determine the corresponding row and column in the intermediate grid
            # Use the modulo operator to wrap around the dimensions of the intermediate grid
            source_row = r % num_rows
            source_col = c % num_cols

            # Assign the value from the intermediate grid to the output grid cell
            output_grid[r][c] = intermediate_grid[source_row][source_col]

    return output_grid
```
