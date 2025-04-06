
## train_1

**input:**
```
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 8 8 8 2 2 8
8 8 8 8 8 8 8
8 8 8 8 8 8 8
8 8 8 5 5 8 8
5 8 5 5 5 5 5
5 5 5 5 5 5 5
```


**output:**
```
2
8
5
```


## train_2

**input:**
```
4 4 4 4 4 4 4 2 2 2 2 2 2 2 8 8
4 4 4 4 4 4 4 4 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 4 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 2 2 2 2 2 2 2 8 8 8
4 4 4 4 4 4 2 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 2 2 2 2 2 2 8 8 8
4 4 4 4 4 2 2 2 2 2 2 2 2 2 8 8
4 4 4 4 4 2 2 2 2 2 2 2 2 2 8 8
4 4 4 4 2 2 2 2 2 2 2 2 2 8 8 8
4 4 4 4 2 2 2 2 2 2 2 2 8 8 8 8
4 4 4 4 4 2 2 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 2 2 2 2 2 2 2 8 8 8
```


**output:**
```
4 2 8
```


## train_3

**input:**
```
6 6 6 6 6 6 6 6 6
6 6 4 4 6 6 6 6 6
6 4 4 4 6 4 6 4 4
4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4
4 2 2 4 4 4 2 2 4
2 2 2 2 2 2 2 2 2
2 3 2 2 2 2 2 3 3
3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3
```


**output:**
```
6
4
2
3
```

*   **Perception:** The task involves processing grids of single-digit integers. The transformation rule appears to depend on the grid's aspect ratio (number of rows vs. columns). Based on this ratio, the grid is scanned either row-by-row (horizontally) or column-by-column (vertically). Within each row or column, the most frequent number (the dominant number) is identified. Consecutive rows or columns sharing the same dominant number form a "band". The final output is the sequence of dominant numbers corresponding to these bands, ordered as they appear (top-to-bottom for horizontal bands, left-to-right for vertical bands). The output format (newline vs. space separated) also seems correlated with the scan direction.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    input_type: grid_of_integers
    output_type: sequence_of_integers
    objects:
      - name: input_grid
        properties:
          - rows: integer
          - columns: integer
          - cells: containing single digits
      - name: scan_direction
        properties:
          - orientation: horizontal | vertical
            determination: based on grid aspect ratio (rows >= columns -> horizontal, columns > rows -> vertical)
      - name: line_scan # Represents a single row or column depending on scan_direction
        properties:
          - elements: list of integers
          - dominant_number: integer (most frequent number in the line_scan)
      - name: dominant_sequence # Sequence of dominant numbers for all lines
        properties:
          - elements: list of integers
      - name: bands # Groups of consecutive identical dominant numbers
        properties:
          - dominant_number: integer
          - extent: range of rows or columns
      - name: output_sequence
        properties:
          - elements: list of unique dominant numbers from consecutive bands
          - order: preserved from band sequence (top-to-bottom or left-to-right)
          - format: newline-separated (horizontal scan) | space-separated (vertical scan)
    actions:
      - name: determine_scan_direction
        inputs: input_grid dimensions
        outputs: scan_direction (horizontal or vertical)
      - name: calculate_dominant_number
        inputs: line_scan (row or column)
        outputs: dominant_number
      - name: generate_dominant_sequence
        inputs: input_grid, scan_direction
        outputs: dominant_sequence
      - name: identify_bands
        inputs: dominant_sequence
        outputs: list of bands (each represented by its dominant number)
      - name: format_output
        inputs: list of band dominant numbers, scan_direction
        outputs: formatted output_sequence
    relationships:
      - scan_direction depends on input_grid aspect ratio.
      - dominant_number is derived from the frequency of elements in a line_scan.
      - dominant_sequence is ordered list of dominant_numbers for each line_scan.
      - bands are identified by grouping consecutive identical numbers in dominant_sequence.
      - output_sequence is derived from the unique dominant numbers of the identified bands, in order.
      - output_format depends on scan_direction.
    ```


*   **Natural Language Program:**
    1.  Read the input grid and determine its dimensions: `R` rows and `C` columns.
    2.  Compare `R` and `C` to determine the scan direction:
        *   If `R` >= `C`, set scan direction to `horizontal`.
        *   If `C` > `R`, set scan direction to `vertical`.
    3.  Initialize an empty list called `dominant_numbers`.
    4.  If the scan direction is `horizontal`:
        *   Iterate through each row of the grid from top to bottom.
        *   For each row, find the integer that appears most frequently (the dominant number).
        *   Append this dominant number to the `dominant_numbers` list.
    5.  If the scan direction is `vertical`:
        *   Iterate through each column of the grid from left to right.
        *   For each column, find the integer that appears most frequently (the dominant number).
        *   Append this dominant number to the `dominant_numbers` list.
    6.  Initialize an empty list called `output_sequence`.
    7.  If `dominant_numbers` is not empty:
        *   Add the first number from `dominant_numbers` to `output_sequence`.
        *   Iterate through `dominant_numbers` starting from the second element.
        *   If the current number is different from the last number added to `output_sequence`, add the current number to `output_sequence`.
    8.  Format the `output_sequence` based on the scan direction:
        *   If scan direction was `horizontal`, join the numbers in `output_sequence` with newline characters.
        *   If scan direction was `vertical`, join the numbers in `output_sequence` with space characters.
    9.  Return the formatted string.
```python
"""
Processes a grid of single-digit integers.
Determines the scan direction (horizontal or vertical) based on the grid's aspect ratio (rows vs. columns).
If rows >= columns, scan horizontally (row-by-row).
If columns > rows, scan vertically (column-by-column).
For each line (row or column) in the scan direction, find the most frequent number (dominant number).
Collect the sequence of these dominant numbers.
Identify consecutive "bands" where the dominant number is the same.
Construct the output sequence by taking the dominant number from each band, preserving the order.
Format the output sequence: newline-separated if scanned horizontally, space-separated if scanned vertically.
"""

import collections
import numpy as np

def find_dominant_number(line: list[int]) -> int:
    """Finds the most frequent number in a list. Handles ties by picking one."""
    if not line:
        # Handle empty lines if necessary, though examples don't show this.
        # Returning a default or raising an error might be options.
        # Based on constraints, let's assume lines are non-empty.
        # If they can be empty, the logic needs refinement.
        # For now, assume non-empty as per examples.
        # A simple approach if empty lines are possible: return a placeholder like -1 or None
        # Or, if an empty line shouldn't contribute, handle it in the caller.
        # Let's stick to the assumption based on examples and return the most common.
        pass # Or handle appropriately if empty lines are expected

    # Count occurrences of each number
    counts = collections.Counter(line)
    # Find the number with the maximum count
    # most_common(1) returns a list of [ (element, count) ]
    dominant_num, _ = counts.most_common(1)[0]
    return dominant_num

def transform(input_grid: list[list[int]]) -> str:
    """
    Transforms the input grid based on dominant numbers in rows or columns.

    Args:
        input_grid: A list of lists representing the grid of integers.

    Returns:
        A formatted string representing the sequence of dominant numbers from bands.
    """

    # 1. Determine grid dimensions
    if not input_grid or not input_grid[0]:
        return "" # Handle empty grid case
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # 2. Determine scan direction
    scan_direction = 'horizontal' if num_rows >= num_cols else 'vertical'

    # 3. Initialize dominant numbers list
    dominant_numbers = []

    # 4./5. Calculate dominant numbers for each row or column
    if scan_direction == 'horizontal':
        # Iterate through each row
        for row in input_grid:
            dominant_num = find_dominant_number(row)
            dominant_numbers.append(dominant_num)
        separator = '\n'
    else: # scan_direction == 'vertical'
        # Use numpy for easy transposition to iterate through columns
        np_grid = np.array(input_grid)
        # Iterate through each column (rows of the transposed grid)
        for col_idx in range(num_cols):
            column = np_grid[:, col_idx].tolist()
            dominant_num = find_dominant_number(column)
            dominant_numbers.append(dominant_num)
        separator = ' '

    # 6. Initialize output sequence
    output_sequence = []

    # 7. Identify unique consecutive dominant numbers (bands)
    if dominant_numbers:
        # Add the first dominant number
        output_sequence.append(dominant_numbers[0])
        # Iterate through the rest, adding only when the number changes
        for i in range(1, len(dominant_numbers)):
            if dominant_numbers[i] != dominant_numbers[i-1]:
                output_sequence.append(dominant_numbers[i])

    # 8. Format the output sequence based on scan direction
    # Convert numbers to strings before joining
    output_str = separator.join(map(str, output_sequence))

    # 9. Return the formatted string
    return output_str
```
