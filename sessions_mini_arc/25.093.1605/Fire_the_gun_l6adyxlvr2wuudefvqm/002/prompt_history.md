
## train_1

**input:**
```
0 0 0 5 5
0 0 0 0 5
5 5 5 0 0
0 0 0 5 0
0 0 5 5 5
```


**output:**
```
2 2 2 5 5
0 0 0 0 5
5 5 5 0 0
0 0 0 5 0
0 0 5 5 5
```


## train_2

**input:**
```
0 0 0 0 0
0 5 5 0 0
0 5 0 0 5
0 0 0 0 5
5 5 5 0 5
```


**output:**
```
0 0 0 0 0
0 5 5 2 2
0 5 0 0 5
0 0 0 0 5
5 5 5 0 5
```


## train_3

**input:**
```
0 5 5 0 0
0 5 0 0 0
0 0 0 0 0
0 0 5 5 0
0 0 0 5 0
```


**output:**
```
0 5 5 2 2
0 5 0 0 0
0 0 0 0 0
2 2 5 5 0
0 0 0 5 0
```

Okay, let's analyze the provided examples.

## Perception

1.  **Data Structure:** The input and output are both 2D grids (matrices) of integers. All examples use 5x5 grids.
2.  **Values:** The input grids contain only the integers 0 and 5. The output grids contain integers 0, 2, and 5.
3.  **Transformation:** The core transformation appears to be changing certain 0s in the input grid to 2s in the output grid. The 5s remain unchanged, and some 0s also remain unchanged.
4.  **Pattern:** The change from 0 to 2 seems dependent on the horizontal proximity to the number 5. Specifically, if a sequence of one or more 0s is immediately adjacent horizontally (either to the left or right) to a sequence of one or more 5s within the same row, those 0s are changed to 2s.
5.  **Row Independence:** The transformation seems to operate independently on each row. Changes in one row do not appear to be influenced by other rows.
6.  **Example Walkthrough (train_3):**
    *   Input Row 0: `0 5 5 0 0`. The sequence `5 5` is adjacent to the sequence `0 0` on its right. Thus, `0 0` becomes `2 2`. Output Row 0: `0 5 5 2 2`.
    *   Input Row 1: `0 5 0 0 0`. No sequence of 0s is directly adjacent to the `5`. Output Row 1: `0 5 0 0 0`.
    *   Input Row 2: `0 0 0 0 0`. No 5s present. Output Row 2: `0 0 0 0 0`.
    *   Input Row 3: `0 0 5 5 0`. The sequence `0 0` is adjacent to the sequence `5 5` on its left. Thus, `0 0` becomes `2 2`. Output Row 3: `2 2 5 5 0`.
    *   Input Row 4: `0 0 0 5 0`. No sequence of 0s is directly adjacent to the `5`. Output Row 4: `0 0 0 5 0`.

## Facts


```yaml
objects:
  - grid:
      description: A 2D array of integers representing the input and output state.
      properties:
        - rows: Integer number of rows.
        - columns: Integer number of columns.
        - cells: Collection of individual cells within the grid.
  - cell:
      description: An individual element within the grid.
      properties:
        - row_index: Integer row position (0-based).
        - column_index: Integer column position (0-based).
        - value: Integer value (0, 2, or 5).
  - sequence:
      description: A contiguous horizontal run of cells with the same value within a single row.
      properties:
        - value: The integer value repeated in the sequence (e.g., 0 or 5).
        - start_col: The starting column index of the sequence.
        - end_col: The ending column index of the sequence.
        - length: The number of cells in the sequence.
        - row_index: The row index where the sequence occurs.

actions:
  - find_sequences:
      description: Identify all horizontal sequences of a specific value (0 or 5) within a given row.
      inputs: [row_data, target_value]
      outputs: [list_of_sequences]
  - check_adjacency:
      description: Determine if a sequence of 0s is immediately adjacent horizontally to a sequence of 5s in the same row.
      inputs: [sequence_0, sequence_5]
      outputs: [boolean_is_adjacent]
      condition: sequence_0.row_index == sequence_5.row_index AND (sequence_0.end_col + 1 == sequence_5.start_col OR sequence_5.end_col + 1 == sequence_0.start_col)
  - change_value:
      description: Modify the value of cells within a sequence from 0 to 2.
      inputs: [grid, sequence_to_change]
      outputs: [modified_grid]

relationships:
  - adjacency:
      description: The relationship between two sequences in the same row where one ends immediately before the other begins horizontally.
      involved_objects: [sequence, sequence]
  - precedence:
      description: A sequence of 0s appears immediately to the left of a sequence of 5s.
      involved_objects: [sequence_of_0s, sequence_of_5s]
  - succession:
      description: A sequence of 0s appears immediately to the right of a sequence of 5s.
      involved_objects: [sequence_of_5s, sequence_of_0s]

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid independently.
3.  For the current row, identify all contiguous horizontal sequences of the value 5. Record their start and end column indices.
4.  For the same current row, identify all contiguous horizontal sequences of the value 0. Record their start and end column indices.
5.  For each identified sequence of 0s:
    *   Check if its end column index plus one equals the start column index of any identified sequence of 5s in the same row (i.e., the 0 sequence immediately precedes a 5 sequence).
    *   Check if its start column index minus one equals the end column index of any identified sequence of 5s in the same row (i.e., the 0 sequence immediately follows a 5 sequence).
    *   If either of these adjacency conditions is true, change the value of all cells within that 0 sequence in the *output* grid from 0 to 2.
6.  After processing all rows, return the modified output grid.
```python
import numpy as np
import copy

"""
Transforms a 2D grid by changing sequences of 0s to 2s if they are immediately 
adjacent horizontally (left or right) to a sequence of 5s within the same row.
"""

def find_sequences(row, target_value):
    """
    Finds all contiguous horizontal sequences of a target value in a row.

    Args:
        row (list or np.array): A single row from the grid.
        target_value (int): The value to find sequences of.

    Returns:
        list: A list of tuples, where each tuple is (start_col, end_col) 
              representing the inclusive start and end indices of a sequence.
    """
    sequences = []
    in_sequence = False
    start_col = -1
    for col_idx, value in enumerate(row):
        if value == target_value and not in_sequence:
            # Start of a new sequence
            in_sequence = True
            start_col = col_idx
        elif value != target_value and in_sequence:
            # End of the current sequence
            sequences.append((start_col, col_idx - 1))
            in_sequence = False
            start_col = -1
        # Handle sequence ending at the last element
        if in_sequence and col_idx == len(row) - 1:
             sequences.append((start_col, col_idx))
    return sequences

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.array): The input 2D grid.

    Returns:
        np.array: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Iterate through each row independently
    for r in range(rows):
        current_row = input_np[r, :]
        
        # Find all horizontal sequences of 0s in the current row
        zero_sequences = find_sequences(current_row, 0)
        
        # Find all horizontal sequences of 5s in the current row
        five_sequences = find_sequences(current_row, 5)
        
        # If there are no 5s in the row, no changes are needed for this row
        if not five_sequences:
            continue
            
        # Check each sequence of 0s for adjacency to any sequence of 5s
        for zero_start, zero_end in zero_sequences:
            is_adjacent_to_five = False
            for five_start, five_end in five_sequences:
                # Check if zero sequence is immediately to the left of a five sequence
                if zero_end + 1 == five_start:
                    is_adjacent_to_five = True
                    break 
                # Check if zero sequence is immediately to the right of a five sequence
                if five_end + 1 == zero_start:
                    is_adjacent_to_five = True
                    break
            
            # If an adjacent 5 sequence was found, change the 0s to 2s in the output grid
            if is_adjacent_to_five:
                for c in range(zero_start, zero_end + 1):
                    output_grid[r, c] = 2

    return output_grid.tolist() # Return as list of lists if preferred, or output_grid for numpy array
```
