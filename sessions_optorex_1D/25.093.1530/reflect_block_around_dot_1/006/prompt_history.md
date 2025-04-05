
## train_1

**input:**
```
9 9 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 0 0 9 9 0 0 0
```


## train_2

**input:**
```
5 5 0 0 0 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 0 0 0 5 5 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 8 2 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 2 8
```


## train_4

**input:**
```
1 1 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 0 0 1 1 0 0 0
```


## train_5

**input:**
```
0 0 0 2 1 1 0 0 0 0 0 0
```


**output:**
```
0 1 1 2 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 3 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 3 0 0 0 0
```


## train_7

**input:**
```
0 0 0 2 5 5 0 0 0 0 0 0
```


**output:**
```
0 5 5 2 0 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are lists/sequences of 12 integers.
2.  **Key Elements:** The sequences contain:
    *   Zeros (`0`).
    *   A pivot element: the number `2`, which appears exactly once in every example.
    *   A target block: a contiguous sequence of one or more identical non-zero integers (e.g., `9 9`, `5 5`, `8`, `1 1`, `3`). This block is distinct from the pivot `2`.
3.  **Implicit Structure:** The sequence represents positions in a line. The core components are the pivot `2` and the target block. Zeros act as spacers or filler.
4.  **Transformation Goal:** The fundamental change involves altering the relative positions of the target block and the pivot `2`.

**YAML Fact Documentation:**


```yaml
task_description: Swap the relative position of a target block of identical non-zero numbers with respect to a fixed pivot element '2', preserving the gap between them.

elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12
  - object: pivot
    properties:
      - value: 2
      - count: 1 per sequence
      - role: fixed reference point
  - object: target_block
    properties:
      - type: contiguous subsequence
      - content: identical non-zero integers (not equal to 2)
      - length: variable (>= 1)
      - count: 1 per sequence
      - role: element to be repositioned
  - object: zero
    properties:
      - value: 0
      - role: filler/spacer

relationships:
  - type: position
    between: [target_block, pivot]
    states: [target_block_left_of_pivot, target_block_right_of_pivot]
  - type: separation
    between: [target_block, pivot]
    properties:
      - name: gap
      - value: number of zeros between the block and the pivot
      - conserved: yes (the gap size is preserved during transformation)

actions:
  - action: identify
    target: pivot (2)
    details: Find its value and index.
  - action: identify
    target: target_block
    details: Find its value, start index, end index, and length.
  - action: determine_relative_position
    elements: [target_block, pivot]
    output: left or right
  - action: calculate_gap
    elements: [target_block, pivot]
    output: number of zeros between them
  - action: construct_output_sequence
    details: Create a new sequence of 12 zeros.
  - action: place_pivot
    target: output_sequence
    details: Place the pivot '2' at its original index.
  - action: place_target_block
    target: output_sequence
    details: |
      Place the target block on the opposite side of the pivot '2'
      compared to its input position, ensuring the calculated gap
      (number of zeros) between the pivot and the block is maintained.
```


**Natural Language Program:**

1.  Start with an empty output sequence of 12 zeros.
2.  Find the index (position) of the pivot element `2` in the input sequence.
3.  Place the pivot element `2` into the output sequence at this same index.
4.  Identify the contiguous block of identical non-zero numbers in the input sequence that are not `2` (this is the "target block"). Record its value, start index, end index, and length.
5.  Determine if the target block is located to the left or right of the pivot `2` in the input sequence.
6.  Calculate the "gap", which is the number of zeros strictly between the target block and the pivot `2` in the input sequence.
7.  If the target block was to the left of the pivot `2` in the input:
    *   Calculate the starting index for the target block in the output sequence as `(index of 2) + 1 + gap`.
    *   Place the target block into the output sequence starting at this calculated index.
8.  If the target block was to the right of the pivot `2` in the input:
    *   Calculate the ending index for the target block in the output sequence as `(index of 2) - 1 - gap`.
    *   Calculate the starting index by subtracting the block length minus 1 from the ending index.
    *   Place the target block into the output sequence starting at this calculated starting index.
9.  The resulting sequence, containing the correctly placed pivot `2`, the repositioned target block, and zeros elsewhere, is the final output.
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Swaps the relative position of a target block of identical non-zero numbers 
(not equal to 2) with respect to a fixed pivot element '2', preserving the 
number of zeros (gap) between them. The pivot '2' remains in its original position.
"""

# === Helper Functions ===

def find_pivot(grid: List[int]) -> Optional[Tuple[int, int]]:
    """Finds the index and value of the pivot element (2)."""
    for i, val in enumerate(grid):
        if val == 2:
            return i, val
    return None # Should not happen based on examples

def find_target_block(grid: List[int], pivot_value: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the target block (contiguous identical non-zero, non-pivot numbers).
    Returns: (value, start_index, end_index, length) or None if not found.
    """
    block_val = -1
    block_start = -1
    block_end = -1

    for i, val in enumerate(grid):
        # Look for the start of a potential block
        if val != 0 and val != pivot_value:
            block_val = val
            block_start = i
            block_end = i
            # Look for contiguous identical elements
            j = i + 1
            while j < len(grid) and grid[j] == block_val:
                block_end = j
                j += 1
            # Found a complete block
            return block_val, block_start, block_end, (block_end - block_start + 1)
    return None # Should not happen based on examples

def calculate_gap(grid: List[int], block_start: int, block_end: int, pivot_index: int) -> int:
    """Calculates the number of zeros between the block and the pivot."""
    gap = 0
    if block_end < pivot_index: # Block is to the left
        start = block_end + 1
        end = pivot_index
    elif block_start > pivot_index: # Block is to the right
        start = pivot_index + 1
        end = block_start
    else: # Should not happen if block and pivot are distinct
        return 0

    for i in range(start, end):
        if grid[i] == 0:
            gap += 1
    return gap

# === Main Transformation Function ===

def transform(input_grid_str: str) -> str:
    """
    Applies the transformation rule to the input grid string.

    Args:
        input_grid_str: A string representing the space-separated integer list.

    Returns:
        A string representing the transformed space-separated integer list.
    """
    # Parse input string into a list of integers
    input_grid = [int(x) for x in input_grid_str.split()]
    n = len(input_grid)

    # Initialize output grid with zeros
    output_grid = [0] * n

    # 1. Find the pivot element (2)
    pivot_info = find_pivot(input_grid)
    if not pivot_info:
        # Handle error: Pivot not found (though examples imply it always exists)
        return " ".join(map(str, output_grid)) # Or raise an error
    pivot_index, pivot_value = pivot_info

    # 2. Place the pivot in the output grid at its original index
    output_grid[pivot_index] = pivot_value

    # 3. Find the target block
    block_info = find_target_block(input_grid, pivot_value)
    if not block_info:
        # Handle error: Target block not found
        return " ".join(map(str, output_grid)) # Or raise an error
    block_val, block_start, block_end, block_len = block_info

    # 4. Determine relative position and calculate the gap
    is_block_left = block_end < pivot_index
    gap = calculate_gap(input_grid, block_start, block_end, pivot_index)

    # 5. Calculate the new position for the target block
    new_block_start = -1
    if is_block_left:
        # Place block to the right of the pivot in the output
        new_block_start = pivot_index + 1 + gap
    else: # Block was to the right
        # Place block to the left of the pivot in the output
        new_block_end = pivot_index - 1 - gap
        new_block_start = new_block_end - block_len + 1

    # 6. Place the target block in the output grid
    # Ensure the calculated indices are within bounds (optional check)
    if 0 <= new_block_start < n and 0 <= new_block_start + block_len - 1 < n:
        for i in range(block_len):
            output_grid[new_block_start + i] = block_val
    else:
         # Handle error: Calculated position is out of bounds
         print(f"Warning: Calculated block position out of bounds. Pivot: {pivot_index}, Block: {block_start}-{block_end}, Gap: {gap}, NewStart: {new_block_start}")
         # Returning partially filled grid or raising error might be options
         pass


    # Convert output list back to space-separated string
    return " ".join(map(str, output_grid))

```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Swaps the relative position of a target block of identical non-zero numbers 
(not equal to 2) with respect to a fixed pivot element '2', preserving the 
number of zeros (gap) between them. The pivot '2' remains in its original position.
The input and output are lists of integers.
"""

# === Helper Functions ===

def find_pivot(grid: List[int]) -> Optional[Tuple[int, int]]:
    """Finds the index and value of the pivot element (2)."""
    for i, val in enumerate(grid):
        if val == 2:
            return i, val
    return None # Should not happen based on examples

def find_target_block(grid: List[int], pivot_value: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the target block (contiguous identical non-zero, non-pivot numbers).
    Returns: (value, start_index, end_index, length) or None if not found.
    """
    block_val = -1
    block_start = -1
    block_end = -1
    n = len(grid)

    i = 0
    while i < n:
        val = grid[i]
        # Look for the start of a potential block
        if val != 0 and val != pivot_value:
            block_val = val
            block_start = i
            block_end = i
            # Look for contiguous identical elements
            j = i + 1
            while j < n and grid[j] == block_val:
                block_end = j
                j += 1
            # Found a complete block
            return block_val, block_start, block_end, (block_end - block_start + 1)
        i += 1 # Move to the next element if not start of target block
    return None # Should not happen based on examples

def calculate_gap(grid: List[int], block_start: int, block_end: int, pivot_index: int) -> int:
    """Calculates the number of zeros strictly between the block and the pivot."""
    gap = 0
    if block_end < pivot_index: # Block is to the left
        start = block_end + 1
        end = pivot_index
    elif block_start > pivot_index: # Block is to the right
        start = pivot_index + 1
        end = block_start
    else: # Should not happen if block and pivot are distinct and non-overlapping
        return 0 # Or raise error

    # Iterate through the indices *between* the block and pivot
    for i in range(start, end):
        if grid[i] == 0:
            gap += 1
    return gap

# === Main Transformation Function ===

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid list.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    n = len(input_grid)

    # Initialize output grid with zeros
    output_grid = [0] * n

    # 1. Find the pivot element (2)
    pivot_info = find_pivot(input_grid)
    if not pivot_info:
        # Handle error: Pivot not found (though examples imply it always exists)
        print("Error: Pivot '2' not found in input.")
        return output_grid # Return empty grid or raise an error
    pivot_index, pivot_value = pivot_info

    # 2. Place the pivot in the output grid at its original index
    output_grid[pivot_index] = pivot_value

    # 3. Find the target block
    block_info = find_target_block(input_grid, pivot_value)
    if not block_info:
        # Handle error: Target block not found
        print("Error: Target block not found in input.")
        return output_grid # Return grid with only pivot or raise an error
    block_val, block_start, block_end, block_len = block_info

    # 4. Determine relative position (left/right) of the block w.r.t. the pivot
    is_block_left = block_end < pivot_index

    # 5. Calculate the gap (number of zeros) between the block and the pivot
    gap = calculate_gap(input_grid, block_start, block_end, pivot_index)

    # 6. Calculate the new starting position for the target block in the output grid
    new_block_start = -1
    if is_block_left:
        # Block was left, move it to the right of the pivot
        # New start = pivot_index + 1 (immediately after pivot) + gap (zeros)
        new_block_start = pivot_index + 1 + gap
    else: # Block was right, move it to the left of the pivot
        # New end = pivot_index - 1 (immediately before pivot) - gap (zeros)
        new_block_end = pivot_index - 1 - gap
        # New start = new_end - length + 1
        new_block_start = new_block_end - block_len + 1

    # 7. Place the target block into the output grid at the calculated position
    # Add boundary checks to prevent index errors
    if 0 <= new_block_start < n and 0 <= new_block_start + block_len - 1 < n:
        for i in range(block_len):
            output_grid[new_block_start + i] = block_val
    else:
         # Handle error: Calculated position is out of bounds
         print(f"Warning: Calculated block position ({new_block_start} to {new_block_start + block_len - 1}) is out of bounds for grid size {n}.")
         # Depending on requirements, could raise error or return partially filled grid.

    # Return the final transformed grid
    return output_grid
```
```python
"""
Transforms an input sequence by swapping the relative position of a target block 
(a contiguous sequence of identical non-zero numbers, not equal to 2) with 
respect to a fixed pivot element '2'. The transformation preserves the number 
of zeros (gap) between the target block and the pivot. The pivot element '2' 
maintains its original absolute position in the sequence. The input and output 
are lists of integers.
"""

from typing import List, Tuple, Optional

# === Helper Functions ===

def find_pivot(grid: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the index and value of the pivot element (2).

    Args:
        grid: The input list of integers.

    Returns:
        A tuple (index, value) of the pivot, or None if not found.
    """
    for i, val in enumerate(grid):
        if val == 2:
            return i, val
    return None # Pivot should always exist based on examples

def find_target_block(grid: List[int], pivot_value: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the target block (contiguous identical non-zero, non-pivot numbers).

    Args:
        grid: The input list of integers.
        pivot_value: The value of the pivot element (to exclude it).

    Returns:
        A tuple (value, start_index, end_index, length) of the block,
        or None if not found.
    """
    block_val = -1
    block_start = -1
    block_end = -1
    n = len(grid)

    i = 0
    while i < n:
        val = grid[i]
        # Look for the start of a potential block (non-zero, non-pivot)
        if val != 0 and val != pivot_value:
            block_val = val
            block_start = i
            block_end = i
            # Look for contiguous identical elements forming the block
            j = i + 1
            while j < n and grid[j] == block_val:
                block_end = j
                j += 1
            # Found the complete block
            block_len = block_end - block_start + 1
            return block_val, block_start, block_end, block_len
        i += 1 # Move to the next element if not the start of the target block
    return None # Target block should always exist based on examples

def calculate_gap(grid: List[int], block_start: int, block_end: int, pivot_index: int) -> int:
    """
    Calculates the number of zeros strictly between the block and the pivot.

    Args:
        grid: The input list of integers.
        block_start: The starting index of the target block.
        block_end: The ending index of the target block.
        pivot_index: The index of the pivot element.

    Returns:
        The count of zeros between the block and pivot.
    """
    gap = 0
    if block_end < pivot_index: # Block is to the left of the pivot
        # Define the range between the block and pivot
        start_range = block_end + 1
        end_range = pivot_index
    elif block_start > pivot_index: # Block is to the right of the pivot
        # Define the range between the pivot and block
        start_range = pivot_index + 1
        end_range = block_start
    else: # Should not happen if block and pivot are distinct and non-overlapping
        return 0 # Or raise an error, depending on assumptions

    # Count zeros within the defined range
    for i in range(start_range, end_range):
        if grid[i] == 0:
            gap += 1
    return gap

# === Main Transformation Function ===

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid list.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    n = len(input_grid)
    # Initialize output_grid with zeros, same length as input
    output_grid = [0] * n

    # Step 1: Find the pivot element (2) and its index
    pivot_info = find_pivot(input_grid)
    if not pivot_info:
        print("Error: Pivot '2' not found in input.")
        return output_grid # Return empty grid or handle error appropriately
    pivot_index, pivot_value = pivot_info

    # Step 2: Place the pivot in the output grid at its original index
    output_grid[pivot_index] = pivot_value

    # Step 3: Find the target block (value, start/end indices, length)
    block_info = find_target_block(input_grid, pivot_value)
    if not block_info:
        print("Error: Target block not found in input.")
        # Return grid with only pivot or handle error
        return output_grid
    block_val, block_start, block_end, block_len = block_info

    # Step 4: Determine the relative position (left/right) of the block w.r.t. the pivot
    is_block_left = block_end < pivot_index

    # Step 5: Calculate the gap (number of zeros) between the block and the pivot in the input
    gap = calculate_gap(input_grid, block_start, block_end, pivot_index)

    # Step 6: Calculate the new starting position for the target block in the output grid
    new_block_start = -1
    if is_block_left:
        # Block was originally left, move it to the right of the pivot
        # New position starts after pivot + gap
        new_block_start = pivot_index + 1 + gap
    else: # Block was originally right, move it to the left of the pivot
        # Calculate the new ending position first (before pivot - gap)
        new_block_end = pivot_index - 1 - gap
        # Calculate the new starting position based on the new end and length
        new_block_start = new_block_end - block_len + 1

    # Step 7: Place the target block into the output grid at the calculated new position
    # Check if the calculated indices are valid before writing
    if 0 <= new_block_start < n and 0 <= new_block_start + block_len - 1 < n:
        for i in range(block_len):
            output_grid[new_block_start + i] = block_val
    else:
         # Handle cases where the new position might be out of bounds
         print(f"Warning: Calculated block position ({new_block_start} to {new_block_start + block_len - 1}) is out of bounds for grid size {n}. Input: {input_grid}")
         # Depending on requirements, might raise error or return partially filled grid.

    # Step 8: Return the final transformed grid
    return output_grid
```
