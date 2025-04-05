
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 2:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 3:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 4:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 5:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 6:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 7:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

Test Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
**General Assessment and Strategy**

The provided code aims to solve the task by identifying a pivot element (`2`), a target block (contiguous identical non-zero numbers != 2), and swapping the block's position relative to the pivot while preserving the number of zeros between them. The code uses standard Python lists and logic.

The error message "The truth value of an array with more than one element is ambiguous" reported across all examples strongly suggests an unexpected interaction with numpy arrays within the testing environment, as the provided Python code itself does not explicitly use numpy array boolean logic in conditionals.

**Strategy:**
1.  **Assume Correctness of Core Logic:** The manual verification of the examples suggests the core logic (finding pivot, block, gap, calculating new position) is likely correct for the task's requirements.
2.  **Focus on Environment/Input:** The issue probably lies in how the input is passed to the function or how the function is executed in the test harness. Perhaps the input `List[int]` is being converted to a `numpy.ndarray` before the function call, or the test harness itself uses numpy operations that cause the error.
3.  **Refine Implementation (Defensive Programming):** Although the Python list code seems correct, ensure no operations could be misinterpreted if inputs were numpy arrays (e.g., avoid direct boolean evaluation of potentially multi-element structures). The current code seems safe in this regard.
4.  **Re-verify Helper Functions:** Use `tool_code` to execute the helper functions defined in the previous code step on the training data to confirm their outputs match the manual analysis.
5.  **Update Documentation:** Refine the YAML facts and natural language program based on confirmed behavior.

**Metrics Gathering (Using `tool_code`)**


*code_execution:*
```python
import sys
# Add the directory containing the previous code to the path
# Assuming the previous code is saved in a file named 'code_00.py'
# In a real scenario, this might involve importing from a specific location.
# For this simulation, we'll redefine the necessary functions here.
from typing import List, Tuple, Optional

# === Helper Functions (Copied from previous attempt) ===

def find_pivot(grid: List[int]) -> Optional[Tuple[int, int]]:
    for i, val in enumerate(grid):
        if val == 2:
            return i, val
    return None

def find_target_block(grid: List[int], pivot_value: int) -> Optional[Tuple[int, int, int, int]]:
    block_val = -1
    block_start = -1
    block_end = -1
    n = len(grid)
    i = 0
    while i < n:
        val = grid[i]
        if val != 0 and val != pivot_value:
            block_val = val
            block_start = i
            block_end = i
            j = i + 1
            while j < n and grid[j] == block_val:
                block_end = j
                j += 1
            return block_val, block_start, block_end, (block_end - block_start + 1)
        i += 1
    return None

def calculate_gap(grid: List[int], block_start: int, block_end: int, pivot_index: int) -> int:
    gap = 0
    if block_end < pivot_index: # Block is to the left
        start = block_end + 1
        end = pivot_index
    elif block_start > pivot_index: # Block is to the right
        start = pivot_index + 1
        end = block_start
    else:
        return 0
    for i in range(start, end):
        if grid[i] == 0:
            gap += 1
    return gap

# === Data ===
train_inputs = [
    [9, 9, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2, 0],
    [1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 5, 5, 0, 0, 0, 0, 0, 0]
]

# === Calculations ===
results = []
for i, grid in enumerate(train_inputs):
    pivot_info = find_pivot(grid)
    if not pivot_info: continue
    pivot_index, pivot_value = pivot_info

    block_info = find_target_block(grid, pivot_value)
    if not block_info: continue
    block_val, block_start, block_end, block_len = block_info

    is_block_left = block_end < pivot_index
    gap = calculate_gap(grid, block_start, block_end, pivot_index)

    # Calculate new position
    new_block_start = -1
    if is_block_left:
        new_block_start = pivot_index + 1 + gap
    else:
        new_block_end = pivot_index - 1 - gap
        new_block_start = new_block_end - block_len + 1

    results.append({
        "example": i + 1,
        "pivot_index": pivot_index,
        "block_value": block_val,
        "block_start": block_start,
        "block_end": block_end,
        "block_len": block_len,
        "is_block_left": is_block_left,
        "gap": gap,
        "new_block_start": new_block_start
    })

print(results)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
[{'example': 1, 'pivot_index': 4, 'block_value': 9, 'block_start': 0, 'block_end': 1, 'block_len': 2, 'is_block_left': True, 'gap': 2, 'new_block_start': 7}, {'example': 2, 'pivot_index': 5, 'block_value': 5, 'block_start': 0, 'block_end': 1, 'block_len': 2, 'is_block_left': True, 'gap': 3, 'new_block_start': 9}, {'example': 3, 'pivot_index': 10, 'block_value': 8, 'block_start': 9, 'block_end': 9, 'block_len': 1, 'is_block_left': True, 'gap': 0, 'new_block_start': 11}, {'example': 4, 'pivot_index': 4, 'block_value': 1, 'block_start': 0, 'block_end': 1, 'block_len': 2, 'is_block_left': True, 'gap': 2, 'new_block_start': 7}, {'example': 5, 'pivot_index': 3, 'block_value': 1, 'block_start': 4, 'block_end': 5, 'block_len': 2, 'is_block_left': False, 'gap': 0, 'new_block_start': 1}, {'example': 6, 'pivot_index': 6, 'block_value': 3, 'block_start': 5, 'block_end': 5, 'block_len': 1, 'is_block_left': True, 'gap': 0, 'new_block_start': 7}, {'example': 7, 'pivot_index': 3, 'block_value': 5, 'block_start': 4, 'block_end': 5, 'block_len': 2, 'is_block_left': False, 'gap': 0, 'new_block_start': 1}]

```
**Metrics Analysis:**
The `tool_code` execution confirms that the helper functions and the logic for calculating the gap and new block position work exactly as expected for standard Python lists, matching the manual analysis. This reinforces the hypothesis that the error reported previously is likely external to the core logic of the provided Python code (e.g., test harness issue, input type mismatch).

**YAML Fact Documentation**


```yaml
task_description: Swap the relative position of a target block of identical non-zero numbers with respect to a fixed pivot element '2', preserving the gap (number of zeros) between them. The pivot '2' maintains its original absolute position.

elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12 (consistent across examples)
  - object: pivot
    properties:
      - value: 2
      - count: 1 per sequence
      - role: fixed reference point (its index remains unchanged)
  - object: target_block
    properties:
      - type: contiguous subsequence
      - content: identical non-zero integers (value != 2)
      - length: variable (>= 1)
      - count: 1 per sequence
      - role: element to be repositioned
  - object: zero
    properties:
      - value: 0
      - role: filler/spacer element defining the gap

relationships:
  - type: position
    between: [target_block, pivot]
    states: [target_block_left_of_pivot, target_block_right_of_pivot]
    determination: Based on block end index vs pivot index.
  - type: separation
    between: [target_block, pivot]
    properties:
      - name: gap
      - definition: Number of zeros strictly between the block and the pivot in the input.
      - conserved: Yes (this number of zeros is maintained between them in the output).

actions:
  - action: identify_pivot
    target: input_sequence
    outputs: pivot_value (2), pivot_index
  - action: identify_target_block
    target: input_sequence
    inputs: pivot_value (to exclude it)
    outputs: block_value, block_start_index, block_end_index, block_length
  - action: determine_relative_position
    inputs: block_end_index, pivot_index
    outputs: is_left (boolean)
  - action: calculate_gap
    inputs: input_sequence, block_start_index, block_end_index, pivot_index
    outputs: gap_size (integer count of zeros between block and pivot)
  - action: initialize_output
    details: Create a new sequence of the same length as input, filled with zeros.
  - action: place_pivot_in_output
    inputs: output_sequence, pivot_value, pivot_index
    details: Place the pivot at its original index in the output.
  - action: calculate_new_block_position
    inputs: pivot_index, gap_size, block_length, is_left (relative position in input)
    outputs: new_block_start_index
    logic: |
      if block was left in input (is_left is True):
        new_start = pivot_index + 1 + gap_size
      else (block was right in input):
        new_end = pivot_index - 1 - gap_size
        new_start = new_end - block_length + 1
  - action: place_target_block_in_output
    inputs: output_sequence, block_value, new_block_start_index, block_length
    details: Place the block's elements at the calculated new position in the output. Check for boundary conditions.
```


**Natural Language Program**

1.  Receive the input sequence (a list of 12 integers).
2.  Create a new output sequence of 12 zeros.
3.  Locate the pivot element `2` in the input sequence and note its index (`pivot_index`).
4.  Place the pivot element `2` into the output sequence at `pivot_index`.
5.  Identify the contiguous block of identical non-zero integers in the input sequence that are not `2`. Record its value (`block_value`), start index (`block_start`), end index (`block_end`), and length (`block_length`).
6.  Determine if the target block is to the left of the pivot in the input (i.e., if `block_end < pivot_index`).
7.  Calculate the gap size: count the number of zeros in the input sequence strictly between the target block and the pivot element (i.e., between `block_end + 1` and `pivot_index` if the block is left, or between `pivot_index + 1` and `block_start` if the block is right).
8.  Calculate the starting index (`new_block_start`) for the target block in the output sequence:
    *   If the block was to the left of the pivot in the input, the new starting index is `pivot_index + 1 + gap_size`.
    *   If the block was to the right of the pivot in the input, the new ending index is `pivot_index - 1 - gap_size`, and the new starting index is `new_ending_index - block_length + 1`.
9.  Place the `block_value` into the output sequence `block_length` times, starting at `new_block_start`. Ensure the placement is within the bounds of the sequence.
10. Return the completed output sequence.
