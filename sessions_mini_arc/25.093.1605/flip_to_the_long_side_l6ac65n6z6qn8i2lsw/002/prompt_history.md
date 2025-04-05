
## train_1

**input:**
```
0 0 0 7 0
0 0 0 0 7
0 0 0 7 0
0 0 0 0 7
0 0 0 7 0
```


**output:**
```
0 0 0 0 7
0 0 0 7 0
0 0 0 0 7
0 0 0 7 0
0 0 0 0 7
```


## train_2

**input:**
```
6 0 6 0 0
0 6 0 6 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 6 0 6 0
6 0 6 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0
0 9 0 0 0
8 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 8 0 0 0
9 0 0 0 0
0 8 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
0 3 0 0 0
3 0 0 0 0
0 6 0 0 0
3 0 0 0 0
0 0 0 0 0
```


**output:**
```
3 0 0 0 0
0 3 0 0 0
6 0 0 0 0
0 3 0 0 0
0 0 0 0 0
```

*   **Perception of Elements:** The task operates on 2D grids of integers. The input grid undergoes a transformation to produce the output grid. The transformation appears to be column-based, specifically involving swapping pairs of adjacent columns. The dimensions of the grid remain constant. The values within the cells are moved, but not altered.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: grid
        properties:
          - type: 2D array of integers
          - dimensions: variable (e.g., 5x5 in examples)
          - cells: contain non-negative integers
      - relationship: adjacency
        between: columns
        definition: Columns with indices `j` and `j+1` are adjacent.
      - action: swap_columns
        target: adjacent column pairs
        condition: Applies to pairs starting with an even index (0, 2, 4, ...)
        effect: The entire content of column `j` is exchanged with the entire content of column `j+1`.
    transformation_goal:
      - Rearrange the grid by systematically swapping adjacent pairs of columns.
    ```


*   **Natural Language Program:**
    1.  Iterate through the columns of the input grid using an index `j`, starting from 0 and incrementing by 2 in each step (i.e., process columns 0, 2, 4, ...).
    2.  For each index `j`, check if a subsequent column `j+1` exists within the grid boundaries.
    3.  If column `j+1` exists, swap the entire contents of column `j` with the entire contents of column `j+1`.
    4.  The resulting grid after performing all necessary swaps is the output.
```python
"""
Rearrange the grid by systematically swapping adjacent pairs of columns.
Iterate through the columns starting from index 0, incrementing by 2.
For each index j, if column j+1 exists, swap column j with column j+1.
"""

import numpy as np
import copy

def swap_columns(grid, col1_idx, col2_idx):
    """
    Swaps two columns in a grid represented as a list of lists.
    """
    new_grid = copy.deepcopy(grid) # Work on a copy
    for row_idx in range(len(new_grid)):
        new_grid[row_idx][col1_idx], new_grid[row_idx][col2_idx] = \
            new_grid[row_idx][col2_idx], new_grid[row_idx][col1_idx]
    return new_grid

def transform(input_grid):
    """
    Applies the column swapping transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    num_rows = len(output_grid)
    if num_rows == 0:
        return output_grid # Handle empty grid case
    num_cols = len(output_grid[0])

    # Iterate through the columns with a step of 2
    # We process pairs (0, 1), (2, 3), (4, 5), etc.
    for j in range(0, num_cols - 1, 2):
        # Check if the next column (j+1) exists
        # The range already ensures j < num_cols - 1, so j+1 is always a valid index within the loop
        
        # Swap the entire contents of column j with column j+1
        # Use a helper function for clarity or perform swap directly
        for i in range(num_rows):
            # Swap elements in each row for the current pair of columns
            output_grid[i][j], output_grid[i][j+1] = output_grid[i][j+1], output_grid[i][j]

    # The resulting grid after performing all necessary swaps is the output
    return output_grid

```
