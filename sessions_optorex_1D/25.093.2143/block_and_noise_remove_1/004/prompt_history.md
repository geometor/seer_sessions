
## train_1

**input:**
```
0 7 7 7 7 0 0 7 0 0 0 7
```


**output:**
```
0 7 7 7 7 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 2 0 0 2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 0 2 2 2 2 2 2
```


## train_3

**input:**
```
0 8 8 8 8 8 8 0 8 0 0 8
```


**output:**
```
0 8 8 8 8 8 8 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 1 0 0 0 0 1 1 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 1 0
```


## train_5

**input:**
```
7 0 0 0 7 0 0 7 7 0 7 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 0 0 0
```


## train_6

**input:**
```
6 0 0 6 0 6 6 6 6 0 0 6
```


**output:**
```
0 0 0 0 0 6 6 6 6 0 0 0
```


## train_7

**input:**
```
0 0 0 8 0 0 0 0 8 8 8 8
```


**output:**
```
0 0 0 0 0 0 0 0 8 8 8 8
```

*   **Perception:** The input and output are sequences of integers of the same length (12). The sequences contain zeros and other non-zero digits. The transformation appears to filter the input sequence, keeping only a specific contiguous subsequence of non-zero numbers while replacing all other elements with zero. The key feature determining which subsequence is kept seems to be its length; specifically, the *longest* contiguous subsequence of non-zero numbers from the input is preserved in its original position in the output. All other positions in the output sequence are filled with zeros.

*   **Facts:**
    
```yaml
    task_description: Identify the longest contiguous sequence of non-zero integers in the input and preserve it in the output, setting all other elements to zero.
    input_data:
      type: list
      element_type: integer
      length: 12
      properties: Contains zeros and non-zero integers.
    output_data:
      type: list
      element_type: integer
      length: 12
      properties: Contains mostly zeros and one contiguous sequence of non-zero integers copied from the input.
    transformation:
      steps:
        - Find all contiguous subsequences of non-zero integers in the input list.
        - Identify the subsequence with the maximum length. (Assumption: there is a unique longest subsequence based on examples).
        - Create a new list of the same length as the input, initialized with zeros.
        - Copy the elements of the identified longest subsequence into the new list at their original indices.
      relationships:
        - The output sequence length is identical to the input sequence length.
        - Non-zero elements in the output correspond exactly to the elements of the longest contiguous non-zero subsequence in the input, maintaining their original values and relative positions.
        - All elements in the output that do not belong to this longest subsequence are zero.
    ```


*   **Natural Language Program:**
    1.  Scan the input sequence to identify all contiguous blocks of non-zero numbers. For each block, record its starting index, length, and the sequence of numbers it contains.
    2.  Compare the lengths of all identified blocks and determine the block with the greatest length.
    3.  Initialize an output sequence of the same length as the input sequence, filling it entirely with zeros.
    4.  Place the numbers from the longest block (identified in step 2) into the output sequence, starting at the same index where the block began in the input sequence.
    5.  Return the modified output sequence.
```python
import math
import collections

def find_longest_nonzero_block(data):
    """
    Finds the start index and length of the longest contiguous block of non-zero numbers.

    Args:
        data: A list of numbers.

    Returns:
        A tuple (start_index, length) of the longest block. 
        Returns (-1, 0) if no non-zero numbers are found.
    """
    max_len = 0
    best_start = -1
    
    current_start = -1
    current_len = 0
    
    for i, x in enumerate(data):
        if x != 0:
            # If starting a new block
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            # If a block just ended
            if current_len > 0:
                # Check if this block is the new longest
                if current_len > max_len:
                    max_len = current_len
                    best_start = current_start
                # Reset current block tracking
                current_len = 0
                current_start = -1

    # Check the last block if the list ends with non-zero numbers
    if current_len > 0:
        if current_len > max_len:
            max_len = current_len
            best_start = current_start
            
    return best_start, max_len

def transform(input_grid):
    """
    Identifies the longest contiguous sequence of non-zero integers in the input list 
    and preserves it in the output list, setting all other elements to zero.
    
    Workflow:
    1. Initialize an output list of the same size as the input, filled with zeros.
    2. Find all contiguous blocks of non-zero numbers in the input list.
    3. Determine the block with the maximum length.
    4. If a longest block exists, copy its elements from the input list to the 
       corresponding positions in the output list.
    5. Return the output list.
    """
    
    n = len(input_grid)
    # 1. Initialize output_grid with zeros
    output_grid = [0] * n

    # 2 & 3. Find the longest non-zero block
    start_index, length = find_longest_nonzero_block(input_grid)

    # 4. Copy the longest block to the output grid if found
    if start_index != -1:
        for i in range(length):
            output_grid[start_index + i] = input_grid[start_index + i]

    # 5. Return the modified output grid
    return output_grid

```
```python
import math
import collections

"""
Identifies the longest contiguous sequence of non-zero integers within the single row 
of the input grid and preserves only this sequence in the corresponding row of 
the output grid, setting all other elements to zero.
"""

def find_longest_nonzero_block(data):
    """
    Finds the start index and length of the longest contiguous block of non-zero numbers.

    Args:
        data: A list of numbers (representing a row).

    Returns:
        A tuple (start_index, length) of the longest block. 
        Returns (-1, 0) if no non-zero numbers are found or the list is empty.
    """
    if not data:
        return -1, 0
        
    max_len = 0
    best_start = -1
    
    current_start = -1
    current_len = 0
    
    for i, x in enumerate(data):
        if x != 0:
            # If starting a new block
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            # If a block just ended
            if current_len > 0:
                # Check if this block is the new longest
                if current_len > max_len:
                    max_len = current_len
                    best_start = current_start
                # Reset current block tracking
                current_len = 0
                current_start = -1

    # Check the last block if the list ends with non-zero numbers
    if current_len > 0:
        if current_len > max_len:
            max_len = current_len
            best_start = current_start
            
    return best_start, max_len

def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    # Workflow Steps:
    # 1. Extract the single row from the input grid.
    # 2. Handle empty input case.
    # 3. Initialize an output row of the same size as the input row, filled with zeros.
    # 4. Find the longest contiguous block of non-zero numbers in the input row.
    # 5. If a longest block exists (length > 0), copy its elements from the input row 
    #    to the corresponding positions in the output row.
    # 6. Construct the output grid containing only the transformed row.
    # 7. Return the output grid.

    # 1. Extract the single row
    if not input_grid or not input_grid[0]:
        # 2. Handle empty input case
        return [] 
    input_row = input_grid[0]
    n = len(input_row)

    # 3. Initialize output_row with zeros
    output_row = [0] * n

    # 4. Find the longest non-zero block
    start_index, length = find_longest_nonzero_block(input_row)

    # 5. Copy the longest block to the output row if found
    if start_index != -1 and length > 0:
        for i in range(length):
            # Ensure we don't go out of bounds (shouldn't happen with correct logic, but safe)
            if start_index + i < n: 
                output_row[start_index + i] = input_row[start_index + i]

    # 6. Construct the output grid
    output_grid = [output_row]

    # 7. Return the output grid
    return output_grid
```
