
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

**Perception**

The task involves transforming a grid of single-digit integers into a smaller grid. The input grids vary in size (4x4, 3x3, 5x5 in the examples), while the output grid is consistently 2x2. By comparing the input and output grids across the examples, a clear pattern emerges: the output grid is always identical to the top-left 2x2 portion of the input grid. The remaining elements of the input grid are discarded.

**Facts**


```yaml
objects:
  - name: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (NxM, where N>=2, M>=2)
      - cell_values: single digits (0-9)
  - name: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: fixed (2x2)
      - cell_values: single digits (0-9)

actions:
  - name: extract_subgrid
    actor: system
    input: input_grid
    output: output_grid
    details: Selects a specific portion of the input_grid.

relationships:
  - type: selection
    source: input_grid
    target: output_grid
    details: The output_grid is formed by selecting the elements from the first two rows (row index 0 and 1) and the first two columns (column index 0 and 1) of the input_grid.
    mapping:
      - input_cell: input_grid[0][0]
        output_cell: output_grid[0][0]
      - input_cell: input_grid[0][1]
        output_cell: output_grid[0][1]
      - input_cell: input_grid[1][0]
        output_cell: output_grid[1][0]
      - input_cell: input_grid[1][1]
        output_cell: output_grid[1][1]

```


**Natural Language Program**

1.  Identify the input grid of numbers.
2.  Select the element at row index 0, column index 0. This becomes the element at row index 0, column index 0 of the output grid.
3.  Select the element at row index 0, column index 1. This becomes the element at row index 0, column index 1 of the output grid.
4.  Select the element at row index 1, column index 0. This becomes the element at row index 1, column index 0 of the output grid.
5.  Select the element at row index 1, column index 1. This becomes the element at row index 1, column index 1 of the output grid.
6.  Arrange these selected elements to form the 2x2 output grid.
```python
"""
Extracts the top-left 2x2 subgrid from the input grid.
The input grid is assumed to have at least 2 rows and 2 columns.
The output grid will always be a 2x2 grid containing the elements
from the first two rows and first two columns of the input grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects the top-left 2x2 portion of the input grid.

    Args:
        input_grid: A list of lists representing the input grid of integers.
                    It's assumed to have at least 2 rows and 2 columns.

    Returns:
        A 2x2 list of lists representing the top-left corner of the input grid.
    """
    # Initialize an empty list to store the output grid
    output_grid = []

    # Select the first row (index 0) from the input grid
    # and take the first two elements (index 0 and 1)
    row0 = input_grid[0][:2]
    output_grid.append(row0)

    # Select the second row (index 1) from the input grid
    # and take the first two elements (index 0 and 1)
    row1 = input_grid[1][:2]
    output_grid.append(row1)

    # Return the constructed 2x2 output grid
    return output_grid

```
