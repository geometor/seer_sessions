
## train_1

**input:**
```
0 1 0
1 0 1
0 1 0
1 0 1
0 1 0
1 0 1
```


**output:**
```
0 2 0
2 0 2
0 2 0
2 0 2
0 2 0
2 0 2
0 2 0
2 0 2
0 2 0
```


## train_2

**input:**
```
0 1 0
1 1 0
0 1 0
0 1 1
0 1 0
1 1 0
```


**output:**
```
0 2 0
2 2 0
0 2 0
0 2 2
0 2 0
2 2 0
0 2 0
0 2 2
0 2 0
```


## train_3

**input:**
```
0 1 0
1 1 0
0 1 0
0 1 0
1 1 0
0 1 0
```


**output:**
```
0 2 0
2 2 0
0 2 0
0 2 0
2 2 0
0 2 0
0 2 0
2 2 0
0 2 0
```

*   **Perception of Elements:** The task involves transforming a 2D grid of binary digits (0 and 1) into a larger 2D grid containing digits 0 and 2. The transformation involves both changing cell values and altering the grid's dimensions by appending rows.

*   **Facts:**
    
```yaml
    objects:
      - Input Grid: A 2D array of integers (0 or 1).
        properties:
          - height: H
          - width: W
          - cells: containing values 0 or 1
      - Output Grid: A 2D array of integers (0 or 2).
        properties:
          - height: H + ceil(H/2)
          - width: W
          - cells: containing values 0 or 2
      - Modified Grid: An intermediate 2D array derived from Input Grid.
        properties:
          - height: H
          - width: W
          - cells: containing values 0 or 2 (1s replaced by 2s)
      - Appended Rows: A subset of rows from the Modified Grid.
        properties:
          - count: ceil(H/2)
          - source_indices: from floor(H/3) up to (floor(H/3) + ceil(H/2) - 1) in Modified Grid

    actions:
      - Value Replacement: Change cell value 1 to 2.
      - Row Selection: Identify specific rows from the Modified Grid based on input height H.
      - Vertical Concatenation: Append the selected rows to the bottom of the Modified Grid.

    relationships:
      - The Output Grid is formed by vertically stacking the Modified Grid on top of the Appended Rows.
      - The Modified Grid is derived from the Input Grid by applying the Value Replacement action to all cells.
      - The Appended Rows are selected from the middle section of the Modified Grid. The exact indices depend on the input height H.
    ```


*   **Natural Language Program:**
    1.  Read the input grid and determine its height (H) and width (W).
    2.  Create a new grid, called the "modified grid," with the same dimensions as the input grid.
    3.  Iterate through each cell of the input grid:
        *   If the cell value is 1, set the corresponding cell value in the modified grid to 2.
        *   If the cell value is 0, set the corresponding cell value in the modified grid to 0.
    4.  Calculate the number of rows to append: `num_appended_rows = ceil(H / 2)`.
    5.  Calculate the starting row index for the rows to append from the modified grid: `start_index = floor(H / 3)`.
    6.  Select the sequence of `num_appended_rows` rows from the modified grid, starting from `start_index`. Call this sequence "appended rows".
    7.  Construct the final output grid by vertically concatenating the complete modified grid with the "appended rows" sequence below it. The output grid will have dimensions `(H + num_appended_rows) x W`.
```python
"""
Transforms an input grid of 0s and 1s into an output grid of 0s and 2s.
The transformation involves two main steps:
1. Value Replacement: All 1s in the input grid are replaced with 2s.
2. Row Appending: A specific subset of rows from the modified grid (with 1s replaced by 2s) is appended to the bottom of the grid. The number of rows appended is ceil(H/2) and they are selected starting from row index floor(H/3), where H is the original height of the input grid.
"""

import math
import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """

    # Get input dimensions
    H = len(input_grid)
    if H == 0:
        return [] # Handle empty input grid
    W = len(input_grid[0])

    # 1. Create the modified grid by replacing 1s with 2s
    modified_grid = []
    for r in range(H):
        new_row = []
        for c in range(W):
            if input_grid[r][c] == 1:
                new_row.append(2)
            else:
                new_row.append(0)
        modified_grid.append(new_row)

    # 2. Calculate parameters for row appending
    num_appended_rows = math.ceil(H / 2)
    start_index = math.floor(H / 3)

    # Ensure the end index doesn't exceed the grid bounds
    end_index = min(start_index + num_appended_rows, H)

    # 3. Select the rows to append from the modified grid
    # Ensure start_index is valid
    if start_index >= H:
         appended_rows = [] # No rows to append if start index is out of bounds
    else:
        appended_rows = modified_grid[start_index:end_index]
        # If slicing doesn't provide enough rows due to end_index constraint,
        # handle potential edge cases if logic intended wrapping or different behavior.
        # Based on examples, slicing seems correct. Check if num_appended_rows needs adjustment if end_index < start_index + num_appended_rows
        actual_appended_count = len(appended_rows)
        if actual_appended_count < num_appended_rows:
             # This case implies H is small, e.g., H=1.
             # floor(1/3)=0, ceil(1/2)=1. Append modified_grid[0:1]. Correct.
             # e.g., H=2. floor(2/3)=0, ceil(2/2)=1. Append modified_grid[0:1]. Correct.
             # e.g., H=3. floor(3/3)=1, ceil(3/2)=2. Append modified_grid[1:3]. Correct.
             pass # Slicing handles boundary conditions correctly.


    # 4. Construct the final output grid by concatenating
    # Use deepcopy to ensure the original modified_grid part isn't aliased if appended_rows overlaps significantly
    output_grid = copy.deepcopy(modified_grid)
    output_grid.extend(appended_rows) # Append the selected rows

    return output_grid

```
```python
"""
Transforms an input grid of 0s and 1s into an output grid of 0s and 2s.
The transformation involves two main steps:
1. Value Replacement: All 1s in the input grid are replaced with 2s to create a modified grid.
2. Row Appending: A specific slice of rows from the modified grid is appended to its bottom. The number of rows to append is ceil(H/2), and they are selected as a contiguous block starting from row index floor(H/3) up to min(floor(H/3) + ceil(H/2), H), where H is the original height of the input grid.
"""

import math
import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """

    # Get input dimensions
    H = len(input_grid)

    # Handle empty input grid
    if H == 0:
        return [] 
    W = len(input_grid[0])

    # 1. Create the modified grid by replacing 1s with 2s
    modified_grid = []
    for r in range(H):
        new_row = []
        for c in range(W):
            # Replace 1 with 2, keep 0 as 0
            if input_grid[r][c] == 1:
                new_row.append(2)
            else:
                new_row.append(0)
        modified_grid.append(new_row)

    # 2. Calculate parameters for row appending slice
    num_appended_rows = math.ceil(H / 2)
    start_index = math.floor(H / 3)
    # Calculate the end index, ensuring it doesn't exceed the grid height
    end_index = min(start_index + num_appended_rows, H)

    # 3. Select the rows to append from the modified grid using slicing
    # Slicing handles cases where start_index >= H or end_index <= start_index correctly (returns empty list)
    appended_rows = modified_grid[start_index:end_index]

    # 4. Construct the final output grid by concatenating
    # Use deepcopy to ensure the original modified_grid part isn't aliased, especially relevant
    # if appended_rows were modified later (though they aren't here). Good practice.
    output_grid = copy.deepcopy(modified_grid)
    # Append the selected rows to the bottom
    output_grid.extend(appended_rows) 

    return output_grid

```
