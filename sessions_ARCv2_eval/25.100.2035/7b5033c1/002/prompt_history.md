
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 4 4 4 4 8 8 8 8 8 8
8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 6 6 6 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
1
1
1
1
1
3
3
3
3
2
2
2
2
2
4
4
4
4
4
6
6
6
```


## train_2

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 2 2 2 2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 3 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 3 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 3 3 3 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 3 3 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
8
8
8
8
8
8
8
2
2
2
2
2
2
2
2
3
3
3
3
3
3
3
3
3
```

## Perception of Task Elements

The input is a square grid (16x16) composed of single digits (0-9). The grid primarily consists of one dominant digit, which acts as a "background" color or value. Embedded within this background are various "blobs" or contiguous regions formed by other digits ("foreground" digits).

The output is a one-dimensional list of digits. This list appears to be constructed by collecting all the foreground digits from the input grid. The order of digits in the output list corresponds to a standard reading order (top-to-bottom, left-to-right) scan of the input grid. The background digit itself is excluded from the output list.

## YAML Fact Documentation

```yaml
task_elements:
  - name: input_grid
    type: Grid
    description: A 2D array of single digits.
    properties:
      - rows: Integer (e.g., 16)
      - columns: Integer (e.g., 16)
      - cell_values: Digits (0-9)
      - contains_background_digit: Boolean
      - contains_foreground_digits: Boolean

  - name: background_digit
    type: Digit
    description: The most frequent digit in the input grid, acting as the background.
    determination_method: Find the digit with the highest count in the input grid.
    example_values:
      - train_1: 8
      - train_2: 1

  - name: foreground_digit
    type: Digit
    description: Any digit in the input grid that is not the background digit.
    properties:
      - value: Digit (0-9, excluding the background_digit)
      - position: Tuple (row_index, column_index)

  - name: output_list
    type: List
    description: A 1D list containing the foreground digits from the input grid.
    properties:
      - elements: Digits (corresponding to foreground_digits)
      - order: Determined by scan order of the input grid.

relationships:
  - type: Extraction
    description: Foreground digits are extracted from the input grid to form the output list.
    source: input_grid
    target: output_list
    condition: The digit must not be the background_digit.

  - type: Ordering
    description: The order of digits in the output list is determined by a row-major scan of the input grid.
    applies_to: output_list
    based_on: Scan order (top-to-bottom, left-to-right) of foreground_digit positions in input_grid.

actions:
  - name: identify_background
    input: input_grid
    output: background_digit
    steps:
      - Count the frequency of each digit in the grid.
      - Identify the digit with the maximum frequency.

  - name: scan_and_extract
    input:
      - input_grid
      - background_digit
    output: output_list
    steps:
      - Initialize an empty list.
      - Iterate through grid rows (0 to N-1).
      - Iterate through grid columns (0 to M-1) within each row.
      - If the digit at the current cell (row, col) is not the background_digit, append it to the list.
      - Return the final list.
```

## Natural Language Program

1.  **Identify the background digit:** Determine which digit appears most frequently in the input grid. This is the background digit.
2.  **Initialize an empty list:** Create a new, empty list to store the results.
3.  **Scan the grid:** Iterate through each cell of the input grid, processing rows from top to bottom, and within each row, processing cells from left to right.
4.  **Check the cell value:** For each cell, compare its digit value to the identified background digit.
5.  **Extract foreground digits:** If the cell's digit is *not* the background digit, append this digit to the result list.
6.  **Finalize:** After scanning all cells, the populated list is the final output.
```python
"""
Identify the most frequent digit (background) in the input grid.
Scan the grid row by row, from top to bottom, and left to right within each row.
Collect all digits that are *not* the background digit into a new list, preserving the scan order.
Return the resulting list of foreground digits.
"""

from collections import Counter
import itertools

def find_background_digit(grid: list[list[int]]) -> int:
  """Finds the most frequent digit in the grid."""
  # Flatten the grid into a single list of digits
  all_digits = list(itertools.chain.from_iterable(grid))
  # Count the occurrences of each digit
  counts = Counter(all_digits)
  # Find the digit with the maximum count
  # If there's a tie, most_common(1) returns one of the most frequent
  background_digit = counts.most_common(1)[0][0]
  return background_digit

def transform(input_grid: list[list[int]]) -> list[int]:
  """
    Extracts foreground digits from a grid based on frequency analysis.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 1D list containing the foreground digits in scan order.
    """

  # 1. Identify the background digit
  background_digit = find_background_digit(input_grid)

  # 2. Initialize an empty list for the output
  output_list = []

  # 3. Scan the grid (top-to-bottom, left-to-right)
  for row in input_grid:
    for cell_value in row:
      # 4. Check if the cell value is a foreground digit
      if cell_value != background_digit:
        # 5. Extract (append) the foreground digit
        output_list.append(cell_value)

  # 6. Return the list of extracted foreground digits
  return output_list
```
