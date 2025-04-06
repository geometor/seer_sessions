
## train_1

**input:**
```
8 8 0 0 2 2 0
0 8 8 0 2 2 8
0 0 0 8 0 8 0
8 0 0 0 0 0 0
0 2 2 0 8 0 8
0 2 2 8 8 0 8
```


**output:**
```
0
```


## train_2

**input:**
```
8 0 0 0 0 8 0
0 0 2 2 0 8 0
8 0 2 2 0 0 0
0 0 8 0 0 8 0
0 0 8 2 2 0 8
8 0 0 2 2 8 0
```


**output:**
```
8
```


## train_3

**input:**
```
8 0 0 2 2 8
8 0 8 2 2 0
0 0 0 0 8 0
2 2 8 0 8 0
2 2 0 0 0 8
0 8 8 0 8 0
```


**output:**
```
0
```


## train_4

**input:**
```
0 8 0 0 0 0 0
2 2 0 8 8 8 0
2 2 8 8 0 2 2
0 0 8 0 0 2 2
0 8 0 0 8 0 0
```


**output:**
```
8
```


## train_5

**input:**
```
8 2 2 8 8 0 0
0 2 2 0 0 0 8
0 8 8 0 0 8 0
0 0 8 0 0 0 8
8 0 8 8 8 2 2
8 0 0 0 0 2 2
```


**output:**
```
8
```


## train_6

**input:**
```
0 0 8 0 8
2 2 8 0 0
2 2 0 0 8
0 0 0 2 2
8 8 0 2 2
```


**output:**
```
0
```

*   **Perception of Task Elements:**
    *   The input is a grid represented as a multi-line string of space-separated digits.
    *   The digits observed in the input grids are 0, 2, and 8.
    *   The size (rows and columns) of the input grid varies across examples.
    *   The output is always a single digit: either 0 or 8.
    *   The digit '2' often appears in adjacent horizontal pairs (`2 2`).
    *   In some inputs, these horizontal pairs are stacked vertically to form 2x2 squares of `2`s (`[[2, 2], [2, 2]]`).
    *   The transformation logic appears to depend on two factors: the shape of the grid (square vs. non-square) and the presence of these 2x2 squares of `2`s.

*   **Facts:**
    
```yaml
    objects:
      - name: input_grid
        properties:
          - type: 2D array of integers
          - digits: [0, 2, 8]
          - rows: integer (number of rows)
          - columns: integer (number of columns)
          - shape: derived property (square if rows == columns, non-square otherwise)
      - name: two_by_two_square_pattern
        properties:
          - structure: [[2, 2], [2, 2]]
          - exists_in_grid: boolean (whether at least one instance is found in input_grid)
      - name: output_value
        properties:
          - type: integer
          - possible_values: [0, 8]

    actions:
      - name: parse_input
        description: Convert the input string into the input_grid object.
      - name: calculate_dimensions
        description: Determine the rows and columns properties of the input_grid.
      - name: check_grid_shape
        description: Determine the shape property (square or non-square) of the input_grid.
      - name: search_for_pattern
        description: Iterate through all 2x2 subgrids of input_grid to determine if the two_by_two_square_pattern exists. Update the exists_in_grid property.
      - name: determine_output
        description: Calculate the output_value based on the grid shape and pattern existence.

    relationships:
      - The output_value depends on the input_grid's shape.
      - If the input_grid's shape is non-square, the output_value depends on whether the two_by_two_square_pattern exists_in_grid.
    ```


*   **Natural Language Program:**
    1.  Read the input string and parse it into a 2D grid of integers.
    2.  Determine the number of rows and columns in the grid.
    3.  Check if the number of rows is equal to the number of columns (i.e., if the grid is square).
    4.  If the grid is square, the output is 0.
    5.  If the grid is not square:
        a.  Search the grid for any 2x2 subgrid that consists entirely of the digit 2 (i.e., `[[2, 2], [2, 2]]`).
        b.  If at least one such 2x2 subgrid of `2`s is found, the output is 8.
        c.  If no such 2x2 subgrid of `2`s is found, the output is 0.
```python
import math
import numpy as np
from collections import Counter

"""
This function takes a 2D grid of integers as input.
It first checks if the grid is square (number of rows equals number of columns).
If the grid is square, the output is 0.
If the grid is not square, it searches for a 2x2 subgrid consisting entirely of the digit 2.
If such a 2x2 subgrid of 2s is found, the output is 8.
If the grid is not square and no 2x2 subgrid of 2s is found, the output is 0.
"""

def find_2x2_of_twos(grid: list[list[int]]) -> bool:
    """
    Searches the grid for any 2x2 subgrid containing only the digit 2.
    Returns True if found, False otherwise.
    """
    rows = len(grid)
    if rows < 2:
        return False
    cols = len(grid[0])
    if cols < 2:
        return False

    # Iterate through all possible top-left corners of a 2x2 subgrid
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if the 2x2 subgrid starting at (r, c) consists only of 2s
            if (grid[r][c] == 2 and
                grid[r+1][c] == 2 and
                grid[r][c+1] == 2 and
                grid[r+1][c+1] == 2):
                return True # Found the pattern
    return False # Pattern not found


def transform(input_grid: list[list[int]]) -> int:
    """
    Determines the output based on grid shape and presence of 2x2 blocks of '2'.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        An integer (0 or 8) based on the transformation rules.
    """
    # Get grid dimensions
    rows = len(input_grid)
    # Handle empty grid case gracefully although examples don't show it
    if rows == 0:
        return 0 
    cols = len(input_grid[0])
    if cols == 0:
        return 0

    # Check if the grid is square
    is_square = (rows == cols)

    # Apply transformation logic
    if is_square:
        # If the grid is square, the output is 0
        output_value = 0
    else:
        # If the grid is not square, check for the 2x2 pattern of 2s
        pattern_found = find_2x2_of_twos(input_grid)
        if pattern_found:
            # If the pattern is found, the output is 8
            output_value = 8
        else:
            # If the pattern is not found, the output is 0
            output_value = 0

    return output_value

# Helper function to parse the input string format if needed
# (assuming the main caller handles parsing based on the problem description)
def parse_input_string(input_str: str) -> list[list[int]]:
    """ Parses the multi-line string input into a list of lists of integers. """
    grid = []
    lines = input_str.strip().split('\n')
    for line in lines:
        grid.append([int(digit) for digit in line.split()])
    return grid

```
```python
import math
import numpy as np
from collections import Counter

"""
Transforms an input grid based on its shape and the number of 2x2 blocks of '2's.

1.  Determine the grid dimensions (rows and columns).
2.  Check if the grid is square (rows == columns).
3.  If the grid is square, the output is 0.
4.  If the grid is not square:
    a.  Count the number of non-overlapping 2x2 subgrids consisting entirely of the digit 2.
    b.  If the count of such 2x2 subgrids is exactly 1, the output is 8.
    c.  Otherwise (count is 0 or greater than 1), the output is 0.
"""

def count_2x2_of_twos(grid: list[list[int]]) -> int:
    """
    Counts the number of non-overlapping 2x2 subgrids containing only the digit 2.

    Args:
        grid: A list of lists representing the 2D grid of integers.

    Returns:
        The integer count of 2x2 subgrids made entirely of '2's.
    """
    rows = len(grid)
    # Handle edge cases: grid too small or potentially malformed
    if rows < 2:
        return 0
    if not grid[0]: # Check if the first row is empty
        return 0
    cols = len(grid[0])
    if cols < 2:
        return 0
    # Ensure all rows have the same length for valid grid processing
    if not all(len(r) == cols for r in grid):
        # Or raise an error, depending on expected input guarantees
        return 0 # Treat malformed grid as having 0 patterns

    count = 0
    # Iterate through all possible top-left corners of a 2x2 subgrid
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if the 2x2 subgrid starting at (r, c) consists only of 2s
            if (grid[r][c] == 2 and
                grid[r+1][c] == 2 and
                grid[r][c+1] == 2 and
                grid[r+1][c+1] == 2):
                count += 1 # Found a pattern
    return count


def transform(input_grid: list[list[int]]) -> int:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        An integer (0 or 8) based on the transformation rules.
    """
    # Get grid dimensions
    rows = len(input_grid)
    # Handle empty grid case
    if rows == 0:
        return 0
    cols = len(input_grid[0])
    if cols == 0:
        return 0

    # Check if the grid is square
    is_square = (rows == cols)

    # Apply transformation logic based on shape
    if is_square:
        # If the grid is square, the output is 0
        output_value = 0
    else:
        # If the grid is not square, count the 2x2 pattern of 2s
        pattern_count = count_2x2_of_twos(input_grid)

        # Determine output based on the count
        if pattern_count == 1:
            # If exactly one pattern is found, the output is 8
            output_value = 8
        else:
            # If zero or more than one pattern is found, the output is 0
            output_value = 0

    # The output is a single integer, not a grid
    return output_value

```
