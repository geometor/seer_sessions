
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 3 3 2 3 3 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 3 2 3 3 2 3 3 2 3 3 2 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
2 8 2 8 2 8
2 8 2 8 2 8
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 8 2 8 2 8 2 8 2 8 2 8
2 8 2 8 2 8 2 8 2 8 2 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 2 2 1 2 2 1 2
2 1 2 2 1 2 2 1
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1
2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception of the Elements:**

The task involves transforming a 2D grid of numbers (integers) into a larger 2D grid.
1.  **Input:** A rectangular grid of integers. The grids vary in size (width and height) across examples. Some rows consist entirely of zeros, while others contain patterns of non-zero integers.
2.  **Output:** A rectangular grid of integers. The output grid always has the same height as the corresponding input grid. The width of the output grid is always exactly double the width of the input grid.
3.  **Transformation:** The content of the output grid appears to be formed by taking the entire input grid and placing an identical copy of it immediately to its right. Each row in the output grid is formed by concatenating the corresponding input row with itself.

**Facts:**


```yaml
Objects:
  - Input_Grid:
      Properties:
        - Height: H (integer)
        - Width: W (integer)
        - Content: 2D array of integers
  - Output_Grid:
      Properties:
        - Height: H (integer, same as Input_Grid height)
        - Width: 2 * W (integer, double the Input_Grid width)
        - Content: 2D array of integers

Actions:
  - Horizontal_Concatenation:
      Input: Input_Grid
      Output: Output_Grid
      Description: Appends a copy of the Input_Grid to its own right side.

Relationships:
  - Output_Grid is derived from Input_Grid.
  - Output_Grid.Height equals Input_Grid.Height.
  - Output_Grid.Width equals 2 times Input_Grid.Width.
  - Each row `i` in Output_Grid is formed by concatenating row `i` of Input_Grid with itself.
```


**Natural Language Program:**

1.  Take the input grid.
2.  Create a new grid with the same number of rows as the input grid and double the number of columns.
3.  For each row in the input grid:
    a.  Copy the row's contents.
    b.  Append the copied contents to the end of the original row's contents.
    c.  Place this newly formed, doubled-length row into the corresponding row of the new grid.
4.  The resulting new grid is the output grid.
```python
"""
Takes an input grid and produces an output grid with the same height 
but double the width. Each row in the output grid is formed by 
concatenating the corresponding input row with itself.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Duplicates the input grid horizontally.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the output 2D grid, which is the
        input grid concatenated horizontally with itself.
    """
    # Initialize an empty list to store the rows of the output grid
    output_grid = []

    # Iterate through each row in the input grid
    for row in input_grid:
        # Create the new row by concatenating the current row with itself
        new_row = row + row
        # Append the newly created double-width row to the output grid
        output_grid.append(new_row)

    # Return the completed output grid
    return output_grid

```
