
## train_1

**input:**
```
0 0 0 0 2 0 0 5 5 5 5 5
```


**output:**
```
0 0 0 0 2 0 5 5 5 5 5 0
```


## train_2

**input:**
```
0 7 7 7 7 2 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 7 2 0 0 0 0 0 0
```


## train_3

**input:**
```
2 8 8 8 8 0 0 0 0 0 0 0
```


**output:**
```
2 8 8 8 8 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 2 0 0 5 5 5 0 0 0 0
```


**output:**
```
0 0 2 0 5 5 5 0 0 0 0 0
```


## train_5

**input:**
```
0 8 8 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 8 8 0 0 2 0 0 0 0 0
```


## train_6

**input:**
```
9 9 9 9 9 9 9 9 9 9 2 0
```


**output:**
```
9 9 9 9 9 9 9 9 9 9 2 0
```


## train_7

**input:**
```
0 2 0 0 0 0 6 6 6 6 6 0
```


**output:**
```
0 2 0 0 0 6 6 6 6 6 0 0
```

*   **Perception of Elements:** The input and output are 1D sequences (arrays) of single digits. The digit '0' appears frequently and seems to represent empty space or background. The digit '2' appears exactly once in each sequence and acts as a reference point or pivot. Other non-zero digits ('5', '6', '7', '8', '9') form contiguous blocks. The transformation involves the potential movement (shifting) of one such block relative to the '2'.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: sequence
        properties:
          - type: 1D array of digits
          - contains_pivot: true
      - element: digit_0
        properties:
          - role: background/empty_space
          - condition_for_shift: must be adjacent to a block on the side away from the pivot
      - element: digit_2
        properties:
          - role: pivot/reference_point
          - cardinality: exactly one per sequence
          - determines_shift_direction: true
      - element: non_zero_digit_block
        properties:
          - type: contiguous sequence of identical non-zero digits (e.g., 5 5 5)
          - can_be_subject_to_action: true
    actions:
      - action: shift_block
        properties:
          - target: non_zero_digit_block
          - direction: towards_pivot ('2')
          - magnitude: one position
          - condition: block must be adjacent to a '0' on the side away from the pivot
          - effect_on_block: moves one position towards pivot
          - effect_on_adjacent_0: replaced by the digit from the moving block
          - effect_on_original_end_of_block: the cell at the original trailing edge (leftmost for right shift, rightmost for left shift) becomes '0'
          - cardinality: at most one shift per transformation
    relationships:
      - relationship: position_relative_to_pivot
        between: [non_zero_digit_block, digit_2]
        properties:
          - determines if a potential shift is leftward or rightward
      - relationship: adjacency
        between: [non_zero_digit_block, digit_0]
        properties:
          - required condition for shift (on the side opposite the pivot)
    invariants:
      - The digit '2' remains in its original position.
      - Digits not part of the shifted block and not the replaced '0' remain in their original positions.
      - The length of the sequence remains constant.
      - Only one block shifts per transformation.
    ```


*   **Natural Language Program:**
    1.  Identify the position of the unique digit '2' in the input sequence.
    2.  Scan the sequence to find all contiguous blocks of identical non-zero digits.
    3.  For each block found:
        a.  Determine if the block is located entirely to the left or entirely to the right of the '2'.
        b.  **If the block is to the right of '2':** Check if the cell immediately preceding the block contains a '0'. If it does, this block is the target for shifting.
        c.  **If the block is to the left of '2':** Check if the cell immediately following the block contains a '0'. If it does, this block is the target for shifting.
    4.  If a target block for shifting was identified:
        a.  **If the target block was to the right of '2' (and preceded by '0'):** Create the output sequence by copying the input, then change the '0' immediately before the block to the digit of the block, and change the last digit of the original block position to '0'.
        b.  **If the target block was to the left of '2' (and followed by '0'):** Create the output sequence by copying the input, then change the '0' immediately after the block to the digit of the block, and change the first digit of the original block position to '0'.
    5.  If no target block for shifting was identified (either no blocks exist, or none meet the adjacency-to-'0' condition), the output sequence is identical to the input sequence.
```python
import re

"""
Identifies the unique pivot digit '2'. Finds contiguous blocks of identical non-zero digits. 
If a block is found adjacent to a '0' on the side away from the pivot ('2'), 
the block shifts one position towards the pivot, replacing the adjacent '0' with the block's digit 
and leaving a '0' at the trailing edge of the original block position. 
Only one such shift occurs per transformation. If no block meets the shift condition, 
the input remains unchanged.
"""

def parse_input(input_str):
    """Converts the input string "0 1 1 0 2" to a list [0, 1, 1, 0, 2]."""
    return [int(d) for d in input_str.split()]

def format_output(output_list):
    """Converts the list [0, 1, 1, 0, 2] to the output string "0 1 1 0 2"."""
    return " ".join(map(str, output_list))

def find_pivot(grid):
    """Finds the index of the pivot element '2'."""
    try:
        return grid.index(2)
    except ValueError:
        return -1 # Pivot not found

def find_blocks(grid):
    """Finds contiguous blocks of identical non-zero digits."""
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        if grid[i] != 0 and grid[i] != 2:
            digit = grid[i]
            start_index = i
            j = i
            while j < n and grid[j] == digit:
                j += 1
            end_index = j - 1
            blocks.append({'start': start_index, 'end': end_index, 'digit': digit})
            i = j # Continue scan after the block
        else:
            i += 1
    return blocks

def transform(input_str):
    """
    Applies the block shifting transformation based on the pivot '2'.

    Args:
        input_str: A string representing the 1D sequence of digits separated by spaces.

    Returns:
        A string representing the transformed 1D sequence, or the original
        string if no transformation occurs.
    """
    # Parse the input string into a list of integers
    input_grid = parse_input(input_str)
    output_grid = list(input_grid) # Start with a copy
    n = len(output_grid)

    # 1. Identify the position of the unique digit '2'
    pivot_index = find_pivot(output_grid)
    if pivot_index == -1:
        # No pivot found, return original grid (as per observed behavior)
        return input_str 

    # 2. Scan the sequence to find all contiguous blocks of identical non-zero digits
    blocks = find_blocks(output_grid)

    target_block = None
    shift_direction = None # 'left' or 'right'

    # 3. For each block found, check if it can be shifted
    for block in blocks:
        start, end, digit = block['start'], block['end'], block['digit']

        # a. Determine if the block is to the left or right of '2'
        if start > pivot_index:
            # b. Block is to the right of '2'
            # Check if the cell immediately preceding the block contains a '0'
            if start > 0 and output_grid[start - 1] == 0:
                target_block = block
                shift_direction = 'left' # Shift towards the pivot
                break # Only one shift allowed
        elif end < pivot_index:
             # c. Block is to the left of '2'
             # Check if the cell immediately following the block contains a '0'
             if end < n - 1 and output_grid[end + 1] == 0:
                 target_block = block
                 shift_direction = 'right' # Shift towards the pivot
                 break # Only one shift allowed

    # 4. If a target block for shifting was identified, perform the shift
    if target_block:
        start, end, digit = target_block['start'], target_block['end'], target_block['digit']
        if shift_direction == 'left':
            # a. Shift block left (towards pivot)
            output_grid[start - 1] = digit # Replace '0' before the block
            output_grid[end] = 0           # Leave '0' at the original end
        elif shift_direction == 'right':
            # b. Shift block right (towards pivot)
            output_grid[end + 1] = digit   # Replace '0' after the block
            output_grid[start] = 0         # Leave '0' at the original start

    # 5. If no target block was identified, output_grid remains the same as input_grid

    # Format the list back into a space-separated string
    return format_output(output_grid)
```
```python
import copy

"""
Identifies the unique pivot digit '2' in a 1D list of integers. Finds the single 
contiguous block of identical non-zero digits (excluding '2'). If this block is 
found adjacent to a '0' on the side *away* from the pivot ('2'), the block shifts 
one position towards the pivot. This shift involves replacing the adjacent '0' with 
the block's digit and setting the cell at the original trailing edge of the block 
(leftmost for a right shift, rightmost for a left shift) to '0'. If no block is 
found, the pivot is missing, or the adjacency condition is not met, the input 
list remains unchanged. The function returns the transformed list.
"""

# Helper functions

def find_pivot(grid):
    """Finds the index of the pivot element '2'."""
    try:
        return grid.index(2)
    except ValueError:
        return -1 # Pivot not found

def find_block(grid):
    """
    Finds the single contiguous block of identical non-zero, non-pivot digits.
    Returns a dictionary {'start': int, 'end': int, 'digit': int} or None.
    """
    n = len(grid)
    found_block = None
    i = 0
    while i < n:
        if grid[i] != 0 and grid[i] != 2:
            digit = grid[i]
            start_index = i
            j = i
            while j < n and grid[j] == digit:
                j += 1
            end_index = j - 1
            # Assuming only one such block exists based on examples
            found_block = {'start': start_index, 'end': end_index, 'digit': digit}
            break # Found the block, stop searching
        else:
            i += 1
    return found_block

# Main transformation function

def transform(input_grid):
    """
    Applies the block shifting transformation based on the pivot '2'.

    Args:
        input_grid: A list of integers representing the 1D sequence.

    Returns:
        A list of integers representing the transformed sequence, or a copy of
        the original list if no transformation occurs.
    """
    # 1. Accept the input as a list of integers.
    # 2. Create a copy of the input list to serve as the potential output list.
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid)

    # 3. Identify the index (position) of the unique digit '2' (the pivot).
    pivot_index = find_pivot(output_grid)
    # If '2' is not found, return the original list.
    if pivot_index == -1:
        return output_grid

    # 4. Scan the list to find the single contiguous block.
    block = find_block(output_grid)
    # 5. If no such block is found, return the original list.
    if not block:
        return output_grid

    start, end, digit = block['start'], block['end'], block['digit']

    # 6. Determine if the found block is located to the left or right of the pivot index.
    # 7. Handle block to the right of the pivot
    if start > pivot_index:
        # a. Check if the index immediately before the block's start is valid and '0'.
        if start > 0 and output_grid[start - 1] == 0:
            # b. Modify the output grid: perform leftward shift.
            output_grid[start - 1] = digit # Replace '0' before the block
            output_grid[end] = 0           # Leave '0' at the original end
            
    # 8. Handle block to the left of the pivot
    elif end < pivot_index:
        # a. Check if the index immediately after the block's end is valid and '0'.
        if end < n - 1 and output_grid[end + 1] == 0:
            # b. Modify the output grid: perform rightward shift.
            output_grid[end + 1] = digit   # Replace '0' after the block
            output_grid[start] = 0         # Leave '0' at the original start

    # 9. If neither shift condition was met, output_grid remains unchanged.
    # 10. Return the (potentially modified) output list.
    return output_grid
```
