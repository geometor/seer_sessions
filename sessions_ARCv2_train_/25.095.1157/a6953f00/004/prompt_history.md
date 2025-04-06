
## train_1

**input:**
```
7 5 8 2
8 0 4 7
1 6 4 7
8 9 6 9
```


**output:**
```
8 2
4 7
```


## train_2

**input:**
```
0 7 9
5 6 5
3 7 9
```


**output:**
```
0 7
5 6
```


## train_3

**input:**
```
5 8 8 9 2
8 0 5 6 5
7 7 2 2 9
5 5 1 7 4
3 3 8 7 7
```


**output:**
```
5 8
8 0
```

*   **Perception:** The input is a grid of integers. The output is always a 2x2 grid of integers. The specific 2x2 subgrid selected from the input depends on the dimensions of the input grid, specifically the number of columns. The output always consists of elements from the first two rows of the input grid. The starting column index for the 2x2 subgrid depends on whether the total number of columns in the input grid is even or odd.

*   **Facts:**
    
```yaml
    task_description: Extract a 2x2 subgrid from the top-left or top-right corner of an input grid based on the parity of the input grid's width.
    elements:
      - object: input_grid
        properties:
          - type: 2D array of integers
          - rows: variable number (R)
          - columns: variable number (N)
      - object: output_grid
        properties:
          - type: 2D array of integers
          - rows: 2
          - columns: 2
          - source: subgrid extracted from input_grid
    actions:
      - action: determine_grid_dimensions
        input: input_grid
        output: number of rows (R), number of columns (N)
      - action: determine_start_column
        input: number of columns (N)
        logic: >
          If N is even, start_column = N - 2.
          If N is odd, start_column = 0.
        output: start_column_index
      - action: extract_subgrid
        input:
          - input_grid
          - start_column_index
        logic: >
          Select elements from input_grid at rows 0 and 1,
          and columns start_column_index and start_column_index + 1.
        output: 2x2 output_grid
      - action: format_output
        input: output_grid
        logic: Format the 2x2 grid with space-separated integers per row and newline characters between rows.
        output: formatted string representation
    relationships:
      - relationship: dependency
        subject: output_grid
        verb: is derived from
        object: input_grid
      - relationship: conditional_logic
        subject: start_column_index
        verb: depends on
        object: parity of the number of columns (N) in input_grid
      - relationship: positional_extraction
        subject: output_grid
        description: Always uses the first two rows (index 0 and 1) of the input_grid.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a 2D grid of integers.
    2.  Determine the number of columns (`N`) in the input grid.
    3.  Calculate the starting column index (`start_col`) for the output subgrid:
        *   If `N` is even, set `start_col = N - 2`.
        *   If `N` is odd, set `start_col = 0`.
    4.  Extract the 2x2 subgrid from the input grid by taking the elements at:
        *   Row 0, Column `start_col`
        *   Row 0, Column `start_col + 1`
        *   Row 1, Column `start_col`
        *   Row 1, Column `start_col + 1`
    5.  Format this 2x2 subgrid into the output string, with space-separated integers on each row and rows separated by newlines.
```python
"""
Extracts a 2x2 subgrid from the input grid. The extraction starts from the first two rows.
The starting column depends on the width (number of columns) of the input grid:
- If the width is even, the subgrid is taken from the last two columns (columns N-2 and N-1).
- If the width is odd, the subgrid is taken from the first two columns (columns 0 and 1).
"""

from typing import List

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Extracts a 2x2 subgrid based on the input grid's width parity.

    Args:
        input_grid: A list of lists representing the 2D integer grid.

    Returns:
        A 2x2 list of lists representing the extracted subgrid.
    """
    # Ensure the grid has at least 2 rows and is not empty
    if not input_grid or len(input_grid) < 2 or not input_grid[0]:
        # Or handle error appropriately based on expected constraints
        return []

    # Determine the number of columns (width)
    num_cols = len(input_grid[0])

    # Calculate the starting column index based on parity
    if num_cols % 2 == 0:
        # Even width: use the last two columns
        # Ensure there are at least 2 columns
        if num_cols < 2:
             return [] # Cannot extract 2x2 if width < 2
        start_col = num_cols - 2
    else:
        # Odd width: use the first two columns
        # Ensure there are at least 2 columns
        if num_cols < 2:
             return [] # Cannot extract 2x2 if width < 2
        start_col = 0

    # Extract the 2x2 subgrid from the first two rows and calculated columns
    # Initialize the output grid
    output_grid = [
        [input_grid[0][start_col], input_grid[0][start_col + 1]],
        [input_grid[1][start_col], input_grid[1][start_col + 1]]
    ]

    # Return the extracted 2x2 subgrid
    return output_grid

```
```python
"""
Extracts a 2x2 subgrid from the input grid and returns it as a formatted string.
The extraction always uses the first two rows.
The starting column depends on the width (number of columns) of the input grid:
- If the width is even, the subgrid is taken from the last two columns (columns N-2 and N-1).
- If the width is odd, the subgrid is taken from the first two columns (columns 0 and 1).
The output is a string with two lines, each containing two space-separated integers.
"""

import numpy as np
from typing import List, Union

def transform(input_grid: Union[List[List[int]], np.ndarray]) -> str:
    """
    Extracts a 2x2 subgrid based on the input grid's width parity and returns a formatted string.

    Args:
        input_grid: A list of lists or NumPy array representing the 2D integer grid.

    Returns:
        A string representing the 2x2 extracted subgrid, formatted with spaces and newlines.
        Returns an empty string or raises an error if extraction is not possible (e.g., < 2 rows/cols).
    """
    # Convert to numpy array for easier handling, if it's not already
    if not isinstance(input_grid, np.ndarray):
        grid = np.array(input_grid)
    else:
        grid = input_grid

    # Check if grid has at least 2 rows and 2 columns
    if grid.shape[0] < 2 or grid.shape[1] < 2:
        # Handle error case: Cannot extract a 2x2 grid
        # Depending on requirements, could return empty string, raise error, etc.
        # Let's return an empty string for now, matching potential implicit ARC behavior.
        return ""
        # raise ValueError("Input grid must have at least 2 rows and 2 columns.")

    # Determine the number of columns (width)
    num_cols = grid.shape[1]

    # Calculate the starting column index based on parity
    if num_cols % 2 == 0:
        # Even width: use the last two columns
        start_col = num_cols - 2
    else:
        # Odd width: use the first two columns
        start_col = 0

    # Extract the four integer values from the first two rows
    val_00 = grid[0, start_col]
    val_01 = grid[0, start_col + 1]
    val_10 = grid[1, start_col]
    val_11 = grid[1, start_col + 1]

    # Format the output string
    # Line 1: value_row0_col0 space value_row0_col1
    # Line 2: value_row1_col0 space value_row1_col1
    output_string = f"{val_00} {val_01}\n{val_10} {val_11}"

    # Return the formatted string
    return output_string

```
