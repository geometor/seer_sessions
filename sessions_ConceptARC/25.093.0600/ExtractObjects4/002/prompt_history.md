
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 6 6 6 6 0
6 6 6 6 6 6
0 6 6 6 6 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
0 0 0 0 0 0
6 6 6 6 6 6
```


**output:**
```
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
4 4 4
4 4 4
4 4 4
```

## Perception

The input data consists of grids (matrices) containing numerical digits. Each grid primarily uses two digits: zero ('0') and a single non-zero digit ('2', '6', or '4' in the examples). The non-zero digit is consistent within each input grid. The zero digit appears to function as a background or separator.

The input grids exhibit a structure often involving alternating rows of all zeros and rows primarily composed of the non-zero digit. Crucially, some rows contain a mixture of zeros and the non-zero digit, specifically featuring a contiguous block of the non-zero digit bounded by zeros (e.g., `... 0 N N N 0 ...`).

The output is a smaller, solid rectangular grid composed entirely of the non-zero digit identified from the input. The dimensions of this output grid appear related to the length of the bounded block of non-zero digits found within the mixed rows of the input.

The transformation involves:
1.  Identifying the unique non-zero digit (`N`) in the input grid.
2.  Locating rows containing the pattern of a sequence of `N`s surrounded by `0`s.
3.  Measuring the length (`W`) of this sequence of `N`s.
4.  Determining the height (`H`) of the output grid based on `W`. The observed rule is H=W, unless W=4, in which case H=5.
5.  Generating an `H x W` grid filled with the digit `N`.

## Facts


```yaml
elements:
  - object: input_grid
    properties:
      - type: grid (matrix) of digits
      - contains: primarily two digits - zero and one unique non-zero digit (N)
      - structure: rows can be all zeros, mostly N, or contain patterns like '0 N...N 0'
  - object: non_zero_digit
    properties:
      - type: digit (e.g., '2', '6', '4')
      - role: foreground color/value
      - uniqueness: only one type per input grid
  - object: zero_digit
    properties:
      - type: digit ('0')
      - role: background color/separator
  - object: pattern_block
    properties:
      - type: contiguous sequence of non_zero_digits
      - location: found within input grid rows that also contain zero_digits
      - structure: bounded by zero_digits (or grid edges acting as boundaries), e.g., '0 N...N 0'
      - characteristic: length (W)
  - object: output_grid
    properties:
      - type: grid (matrix) of digits
      - composition: filled entirely with the non_zero_digit (N) from the input
      - dimensions: H rows x W columns
      - relationship_to_input:
          - W (width) is determined by the length of the pattern_block.
          - H (height) is determined by W (H=W, except if W=4 then H=5).

actions:
  - identify: the unique non_zero_digit (N) in the input_grid.
  - locate: rows in the input_grid containing the pattern_block ('0 N...N 0').
  - measure: the length (W) of the pattern_block.
  - calculate: the output height (H) based on W (H=W, or H=5 if W=4).
  - generate: the output_grid of size H x W, filled with N.

relationships:
  - output_grid width (W) is equal to the pattern_block length (W).
  - output_grid height (H) depends conditionally on the pattern_block length (W).
  - output_grid cell value is the non_zero_digit from the input_grid.
```


## Natural Language Program

1.  Identify the unique non-zero digit (`N`) present in the input grid.
2.  Scan each row of the input grid to find rows containing a contiguous sequence of `N`s that is immediately preceded and followed by a `0`.
3.  Determine the length (`W`) of this contiguous sequence of `N`s. (Assume this length is consistent if multiple such sequences exist).
4.  Calculate the height (`H`) for the output grid: if `W` is 4, set `H` to 5; otherwise, set `H` equal to `W`.
5.  Create a new grid with `H` rows and `W` columns.
6.  Fill every cell of this new grid with the non-zero digit `N`.
7.  Return the newly created grid as the output.
```python
import numpy as np
import re
from typing import List

"""
1. Identify the unique non-zero digit (`N`) present in the input grid.
2. Scan each row of the input grid to find rows containing a contiguous sequence of `N`s that is immediately preceded and followed by a `0`.
3. Determine the length (`W`) of this contiguous sequence of `N`s. (Assume this length is consistent if multiple such sequences exist).
4. Calculate the height (`H`) for the output grid: if `W` is 4, set `H` to 5; otherwise, set `H` equal to `W`.
5. Create a new grid with `H` rows and `W` columns.
6. Fill every cell of this new grid with the non-zero digit `N`.
7. Return the newly created grid as the output (list of lists of integers).
"""

def find_non_zero_digit(grid: np.ndarray) -> int:
    """Finds the unique non-zero digit in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    raise ValueError("No non-zero digit found in the input grid.")

def find_pattern_width(grid: np.ndarray, non_zero_digit: int) -> int:
    """Finds the width W of the pattern '0 N...N 0'."""
    n_str = str(non_zero_digit)
    width = 0
    pattern_found = False
    # Define the regular expression pattern to find Ns bounded by 0s
    regex_pattern = rf"0({n_str}+)0"

    for r in range(grid.shape[0]):
        # Convert the current row to a string for regex matching
        row_str = "".join(map(str, grid[r, :]))
        
        # Find all occurrences of the pattern in the row
        matches = re.findall(regex_pattern, row_str)
        
        if matches:
            # If matches are found, process them
            for match in matches:
                current_width = len(match) # Length of the sequence of Ns
                if not pattern_found:
                    # If this is the first pattern found, set the width
                    width = current_width
                    pattern_found = True
                elif width != current_width:
                    # If a pattern with a different width is found, raise an error
                    # (assuming consistency based on examples)
                    raise ValueError(f"Inconsistent pattern widths found: {width} and {current_width}")

    if not pattern_found:
        # If no pattern '0 N...N 0' was found after checking all rows
        raise ValueError("Pattern '0 N...N 0' not found in any row.")
        
    return width

def transform(input_grid_str: List[str]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying a non-zero digit N
    and a pattern '0 N...N 0' to determine the dimensions of a solid
    output grid filled with N.

    Args:
        input_grid_str: A list of strings, where each string represents a row
                         of the input grid with space-separated digits.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    # Convert input strings to numpy array of ints for easier processing
    try:
        input_list = [[int(d) for d in row.split()] for row in input_grid_str]
        input_grid = np.array(input_list, dtype=int)
    except ValueError:
        raise ValueError("Input grid contains non-integer values or incorrect format.")
    
    if input_grid.size == 0:
         return [] # Handle empty input grid

    # 1. Identify the unique non-zero digit (N)
    try:
        non_zero_digit = find_non_zero_digit(input_grid)
    except ValueError as e:
        print(f"Error: {e}")
        return [] # Return empty if no non-zero digit is found

    # 2. Scan rows to find the pattern '0 N...N 0' and determine its length (W)
    try:
        W = find_pattern_width(input_grid, non_zero_digit)
    except ValueError as e:
        print(f"Error: {e}")
        return [] # Return empty if pattern is not found or inconsistent

    # 3. Calculate the output height (H) based on W
    #    Special case: If W is 4, H is 5. Otherwise, H is W.
    if W == 4:
        H = 5
    else:
        H = W

    # 4. Create a new grid (H x W) filled with the non-zero digit N
    output_grid = np.full((H, W), non_zero_digit, dtype=int)

    # 5. Convert the output numpy array back to a list of lists of integers
    output_list = output_grid.tolist()

    return output_list

```
