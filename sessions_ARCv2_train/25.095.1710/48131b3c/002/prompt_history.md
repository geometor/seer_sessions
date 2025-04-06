
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

Okay, let's break down the transformation.

**Perception of Elements:**

1.  **Input/Output Data Structure:** Both inputs and outputs are 2D grids (matrices) containing integer values.
2.  **Grid Dimensions:** The output grid's dimensions (height and width) are consistently double the input grid's dimensions. If the input is N x N, the output is 2N x 2N.
3.  **Row Transformation:** Examining the relationship between input rows and output rows reveals a specific pattern:
    *   The first row of the output is formed by taking the *second* row of the input and repeating it horizontally twice.
    *   The second row of the output is formed by taking the *first* row of the input and repeating it horizontally twice.
    *   Subsequent rows (from index 2 up to N-1) in the *first half* of the output grid (rows 0 to N-1) are formed by taking the corresponding input row (index 2 to N-1) and repeating it horizontally twice.
4.  **Grid Duplication:** The entire top half of the output grid (rows 0 to N-1) is identical to the bottom half of the output grid (rows N to 2N-1). The pattern generated in the first N rows is simply duplicated vertically.
5.  **Core Operation:** The fundamental operations are:
    *   Swapping the first two rows of the input grid.
    *   Horizontally duplicating each row of the modified input grid.
    *   Vertically duplicating the resulting grid block.

**Facts (YAML):**


```yaml
task_description: Transform an input grid into an output grid of doubled dimensions based on row swapping and duplication.
input_object:
  type: grid
  properties:
    data_type: integer
    shape: NxN (square)
output_object:
  type: grid
  properties:
    data_type: integer
    shape: 2Nx2N (square)
transformation_steps:
  - step: 1
    action: modify_input
    details: Create a temporary grid by swapping the first row (index 0) and the second row (index 1) of the input grid. All other rows remain in their original positions relative to each other. Let N be the dimension of the input grid. If N < 2, this step has no effect.
  - step: 2
    action: build_intermediate_grid
    details: Create an intermediate grid with dimensions N x 2N. For each row `i` (from 0 to N-1) in the modified input grid, the corresponding row `i` in the intermediate grid is formed by concatenating the modified input grid's row `i` with itself horizontally.
  - step: 3
    action: build_output_grid
    details: Create the final output grid with dimensions 2N x 2N. The top half (rows 0 to N-1) of the output grid is identical to the intermediate grid. The bottom half (rows N to 2N-1) of the output grid is also identical to the intermediate grid (i.e., the intermediate grid is vertically stacked upon itself).
relationships:
  - output_dimensions: are double the input_dimensions (height and width).
  - output_content: derived from input_content via row swapping and duplication.
  - output_structure: exhibits a 2x2 tiling pattern based on a modified version of the input.
```


**Natural Language Program:**

1.  Given an input square grid of size N x N.
2.  Create a modified version of the input grid: if N is 2 or greater, swap the first row (at index 0) with the second row (at index 1). Otherwise, use the input grid as is.
3.  Construct an intermediate grid of size N x 2N: For each row in the modified grid, create a new row by appending the row to itself (horizontal duplication). Assemble these new, wider rows to form the intermediate grid, maintaining the row order from the modified grid.
4.  Construct the final output grid of size 2N x 2N: Take the intermediate grid (N x 2N) and vertically stack it on top of itself. The resulting 2N x 2N grid is the output.
```python
import copy # Used for deep copying the input grid to avoid modifying it

"""
Transforms an input square grid (N x N) into an output grid (2N x 2N) based on the following steps:
1. Create a modified version of the input grid: if the grid height (N) is 2 or greater, swap the first row (index 0) with the second row (index 1).
2. Construct an intermediate grid (N x 2N): Each row from the modified grid is duplicated horizontally (concatenated with itself).
3. Construct the final output grid (2N x 2N): The intermediate grid is duplicated vertically (stacked on top of itself).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A square list of lists representing the N x N input grid.

    Returns:
        A list of lists representing the 2N x 2N output grid.
    """

    # Determine the size of the input grid
    n = len(input_grid)
    if n == 0:
        return [] # Handle empty input

    # --- Step 1: Modify the input grid (swap first two rows if N >= 2) ---
    modified_grid = copy.deepcopy(input_grid) # Create a copy to avoid changing the original input
    if n >= 2:
        # Swap the first and second rows
        modified_grid[0], modified_grid[1] = modified_grid[1], modified_grid[0]

    # --- Step 2: Build the intermediate grid (N x 2N) by horizontal duplication ---
    intermediate_grid = []
    for i in range(n):
        # Get the current row from the modified grid
        row = modified_grid[i]
        # Create the new row by concatenating the row with itself
        doubled_row = row + row
        # Add the doubled row to the intermediate grid
        intermediate_grid.append(doubled_row)

    # --- Step 3: Build the output grid (2N x 2N) by vertical duplication ---
    # The output grid is simply the intermediate grid stacked on top of itself
    output_grid = intermediate_grid + intermediate_grid

    return output_grid

```
