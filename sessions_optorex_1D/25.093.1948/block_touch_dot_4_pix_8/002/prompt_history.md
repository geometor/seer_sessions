
## train_1

**input:**
```
0 0 0 0 9 9 9 9 9 9 2 0
```


**output:**
```
0 0 0 0 9 9 9 9 9 9 2 0
```


## train_2

**input:**
```
0 0 7 7 7 7 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 2 0
```


## train_3

**input:**
```
0 0 0 0 2 0 3 3 3 3 3 3
```


**output:**
```
0 0 0 0 2 3 3 3 3 3 3 0
```


## train_4

**input:**
```
2 0 0 6 0 0 0 0 0 0 0 0
```


**output:**
```
2 6 0 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 2 0 0 0 0 5 5 5 0 0
```


**output:**
```
0 0 2 5 5 5 0 0 0 0 0 0
```


## train_6

**input:**
```
3 3 3 3 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 2 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 2 0 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 3 0 0
```

Okay, let's break down the transformation.

**Perception of Elements:**

*   **Objects:** The core objects are sequences of digits. Within these sequences, we can identify:
    *   Individual digits.
    *   A special digit `2`, acting as a pivot or anchor.
    *   The digit `0`, acting as a filler or spacer that can be moved.
    *   Contiguous blocks of identical digits other than `0` or `2`. Let's call these "value blocks".
*   **Properties:**
    *   Sequences have a fixed length.
    *   The digit `2` appears exactly once in all examples.
    *   Each example (except train_1) features exactly one "value block". In train_1, the value block (`9`s) is adjacent to the `2`.
    *   Digits `0` can appear multiple times and are located between the value block and the `2`, or elsewhere.
*   **Actions:** The primary action is rearranging the sequence elements. Specifically:
    *   A value block moves towards the `2`.
    *   The `0`s originally separating the value block and the `2` are relocated.
*   **Relationships:** The key relationship is the relative position of the value block with respect to the `2`.
    *   Value block is to the left of `2`.
    *   Value block is to the right of `2`.
    *   Value block is adjacent to `2` (a special case where no `0`s are between them).

**YAML Facts:**


```yaml
task_description: Rearrange a sequence of digits based on the relative positions of a 'value block' and the digit '2'.
elements:
  - object: sequence
    properties:
      - type: list of digits
      - fixed_length
  - object: digit_2
    properties:
      - role: pivot/anchor
      - count: exactly one per sequence
  - object: digit_0
    properties:
      - role: filler/spacer
      - count: variable
      - behavior: movable
  - object: value_block
    properties:
      - type: contiguous sequence of identical digits (not 0 or 2)
      - count: at most one per sequence (in examples)
      - behavior: moves towards digit_2
relations:
  - type: spatial
    subject: value_block
    object: digit_2
    states:
      - left_of
      - right_of
      - adjacent_to
actions:
  - name: rearrange
    inputs:
      - sequence
      - position_of_2
      - value_block (if exists)
      - zeros_between_block_and_2 (if any)
    outputs:
      - rearranged_sequence
    logic:
      - If value_block is left_of 2:
          - move value_block to be immediately left_of 2
          - move zeros_between_block_and_2 to the start of the sequence
      - If value_block is right_of 2:
          - move value_block to be immediately right_of 2
          - move zeros_between_block_and_2 to the end of the sequence
      - If no value_block exists or it's adjacent_to 2:
          - sequence remains unchanged
```


**Natural Language Program:**

1.  Parse the input string into a list of digits.
2.  Locate the index of the digit `2`.
3.  Search the list for the first occurrence of a contiguous block of identical digits `B` where the digit is neither `0` nor `2`.
4.  If no such block `B` is found, return the original input sequence unchanged.
5.  Determine if the block `B` is positioned to the left or right of the digit `2`.
6.  Identify the sub-sequence of digits `Z` located strictly between the block `B` and the digit `2`. Note that `Z` will consist only of `0`s based on the examples. If `B` and `2` are adjacent, `Z` is empty.
7.  Construct the output sequence by removing both block `B` and the intermediate sequence `Z` from their original positions.
8.  If the block `B` was originally to the left of `2`:
    a.  Insert the digits from `Z` at the beginning of the sequence.
    b.  Insert the digits from block `B` immediately before the digit `2`.
9.  If the block `B` was originally to the right of `2`:
    a.  Insert the digits from block `B` immediately after the digit `2`.
    b.  Append the digits from `Z` to the end of the sequence.
10. Format the resulting list of digits back into a space-separated string for the output.
```python
import re

"""
Rearrange a sequence of digits based on the relative positions of a 'value block' (contiguous identical digits other than 0 or 2) and the digit '2'. 
If a value block exists and is separated from the '2' by zeros:
- If the block is to the left of '2', move the block immediately to the left of '2' and move the intervening zeros to the start of the sequence.
- If the block is to the right of '2', move the block immediately to the right of '2' and move the intervening zeros to the end of the sequence.
- If the block is adjacent to '2' or no such block exists, the sequence remains unchanged.
"""

def _find_pivot_index(grid, pivot_value=2):
    """Finds the index of the pivot value (2) in the grid."""
    try:
        return grid.index(pivot_value)
    except ValueError:
        return -1 # Pivot not found

def _find_first_value_block(grid, pivot_index):
    """
    Finds the first contiguous block of identical digits != 0 and != 2.
    Returns (start_index, end_index, value) or (None, None, None).
    end_index is exclusive.
    """
    n = len(grid)
    for i in range(n):
        # Skip 0s and the pivot value
        if grid[i] == 0 or grid[i] == 2:
            continue
        
        # Found a potential start of a block
        block_value = grid[i]
        j = i + 1
        while j < n and grid[j] == block_value:
            j += 1
            
        # Check if it's a block (length > 0)
        if j > i: 
            return i, j, block_value # Found the first block
            
    return None, None, None # No value block found


def transform(input_str):
    """
    Transforms the input string based on the described rules.
    
    Args:
        input_str: A string of space-separated digits.

    Returns:
        A string of space-separated digits representing the transformed sequence.
    """
    # 1. Parse the input string into a list of digits.
    grid = [int(d) for d in input_str.split()]
    n = len(grid)

    # 2. Locate the index of the digit 2.
    pivot_index = _find_pivot_index(grid, 2)
    if pivot_index == -1:
        # Should not happen based on examples, but good practice
        return input_str 

    # 3. Search for the first value block B.
    block_start, block_end, block_value = _find_first_value_block(grid, pivot_index)

    # 4. If no such block B is found, return the original input sequence unchanged.
    if block_start is None:
        return input_str

    # Determine intermediate zeros Z and relative position
    intermediate_zeros = []
    block_is_left = False
    
    if block_end <= pivot_index: # Block is to the left of or touching the pivot from left
        block_is_left = True
        # 6. Identify the sub-sequence of digits Z between B and 2.
        for i in range(block_end, pivot_index):
            if grid[i] == 0:
                intermediate_zeros.append(0)
            # else: Should ideally only be zeros based on problem description
                # pass # Or handle unexpected values
        # If adjacent, intermediate_zeros will be empty
        if not intermediate_zeros and block_end == pivot_index: # Check for adjacency
             return input_str # Return unchanged if adjacent

    elif block_start > pivot_index: # Block is to the right of the pivot
        block_is_left = False
        # 6. Identify the sub-sequence of digits Z between 2 and B.
        for i in range(pivot_index + 1, block_start):
             if grid[i] == 0:
                intermediate_zeros.append(0)
             # else: Should ideally only be zeros based on problem description
                # pass # Or handle unexpected values
        # If adjacent, intermediate_zeros will be empty
        if not intermediate_zeros and block_start == pivot_index + 1: # Check for adjacency
            return input_str # Return unchanged if adjacent
    else:
        # This case (block contains pivot) shouldn't occur if block value != 2
        return input_str


    # 7. Construct the output sequence by removing B and Z.
    output_grid = []
    indices_to_remove = set(range(block_start, block_end))
    
    if block_is_left:
        indices_to_remove.update(range(block_end, pivot_index))
    else: # block is right
        indices_to_remove.update(range(pivot_index + 1, block_start))

    for i in range(n):
        if i not in indices_to_remove:
            output_grid.append(grid[i])

    # Find the new pivot index after removals
    # Since we know pivot was never removed, we can find it again
    new_pivot_index = _find_pivot_index(output_grid, 2) 
    
    # Extract the block elements
    value_block_elements = [block_value] * (block_end - block_start)

    # 8. If B was originally to the left of 2:
    if block_is_left:
        # a. Insert Z at the beginning.
        final_grid = intermediate_zeros + output_grid
        # Find pivot index again after adding zeros at start
        new_pivot_index = _find_pivot_index(final_grid, 2) 
        # b. Insert B immediately before 2.
        final_grid = final_grid[:new_pivot_index] + value_block_elements + final_grid[new_pivot_index:]
        
    # 9. If B was originally to the right of 2:
    else: # block_is_right
        # a. Insert B immediately after 2.
        # We use the pivot index found *before* adding zeros at the end
        final_grid = output_grid[:new_pivot_index+1] + value_block_elements + output_grid[new_pivot_index+1:]
        # b. Append Z to the end.
        final_grid = final_grid + intermediate_zeros

    # 10. Format the resulting list back into a string.
    return " ".join(map(str, final_grid))

```
