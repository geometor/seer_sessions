
## train_1

**input:**
```
0 0 0 0 0 0 2 0 0 7 7 7
```


**output:**
```
0 7 7 7 0 0 2 0 0 0 0 0
```


## train_2

**input:**
```
3 3 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 3 3 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 2 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 2 0 0 0 0
```


## train_4

**input:**
```
0 9 9 9 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 9 9 9 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 2 4 4 4 0 0 0 0
```


**output:**
```
0 4 4 4 2 0 0 0 0 0 0 0
```


## train_6

**input:**
```
5 5 5 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 5 5 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 8 8 0 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 0 8 8 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are both sequences (lists) of 12 single-digit integers.
    *   Each input sequence contains exactly one instance of the digit `2`.
    *   Each input sequence also contains one or more occurrences of another non-zero digit, forming a contiguous block. All other elements are `0`.
    *   The digit `2` acts as a fixed pivot; its position remains unchanged from input to output.
    *   The contiguous block of the other non-zero digit ("the block") changes its position in the output relative to the pivot `2`.
    *   The transformation involves relocating the block based on its initial position relative to the pivot. The relative distance between the pivot and the nearest edge of the block seems preserved but mirrored.

*   **YAML Facts:**
    
```yaml
    task_description: Reposition a block of digits relative to a fixed pivot digit '2'.
    elements:
      - object: sequence
        properties:
          format: list of 12 integers (0-9)
          role: input/output container
      - object: pivot
        properties:
          value: 2
          occurrence: exactly one per sequence
          behavior: position is fixed between input and output
          identifier: idx_2 (index of the pivot)
      - object: block
        properties:
          value: non-zero integer (not 2)
          occurrence: one contiguous block per sequence
          structure: sequence of identical digits
          length: variable (>= 1)
          identifier: block_val, block_start_in, block_end_in, block_len
      - object: padding
        properties:
          value: 0
          role: fills remaining positions
    action:
      name: reposition_block
      inputs:
        - pivot (idx_2)
        - block (block_start_in, block_end_in, block_len, block_val)
        - input_sequence
      output: output_sequence
      logic: |
        The block's position is mirrored relative to the pivot, maintaining the distance
        between the pivot and the nearest edge of the block.
        If the block is initially before the pivot, it moves after the pivot.
        If the block is initially after the pivot, it moves before the pivot.
    relationships:
      - type: relative_position
        object1: block
        object2: pivot
        condition: Determines the direction of movement (block_start_in < idx_2 or block_start_in > idx_2).
      - type: distance
        object1: block (nearest edge)
        object2: pivot
        condition: Determines the placement offset in the output (abs(idx_2 - block_end_in) or abs(block_start_in - idx_2)).
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of the same length as
```python
import math
import re # Using re for potential parsing, although simple split might suffice here

"""
Reposition a contiguous block of identical non-zero digits relative to a fixed 
pivot digit '2'. The block's position is mirrored across the pivot, maintaining 
the distance between the pivot and the nearest edge of the block. If the block 
is initially before the pivot, it moves after the pivot in the output. If the 
block is initially after the pivot, it moves before the pivot in the output. 
All other positions are filled with '0'.
"""

def find_pivot(grid):
  """Finds the index of the pivot element '2'."""
  try:
    return grid.index(2)
  except ValueError:
    raise ValueError("Pivot element '2' not found in the input grid.")

def find_block(grid, pivot_index):
  """Finds the non-zero, non-pivot block's value, start index, end index, and length."""
  block_val = -1
  block_start = -1
  block_end = -1
  n = len(grid)

  # Find the first non-zero, non-pivot element to determine block_val
  for i, val in enumerate(grid):
    if val != 0 and val != 2:
      block_val = val
      break
  
  if block_val == -1:
      # Handle case where only 0s and potentially a 2 exist (though constraints say otherwise)
      # Or more likely, the input format is different than expected.
      # Based on examples, a block always exists.
      raise ValueError("No block value found (non-zero, non-2 digit).")

  # Find the start and end of the block
  in_block = False
  for i, val in enumerate(grid):
      if val == block_val and not in_block:
          block_start = i
          in_block = True
      elif val != block_val and in_block:
          block_end = i - 1
          break
  # Handle case where block extends to the end of the grid
  if in_block and block_end == -1:
      block_end = n - 1
      
  if block_start == -1:
      raise ValueError(f"Block with value {block_val} not found.")

  block_len = block_end - block_start + 1
  return block_val, block_start, block_end, block_len


def transform(input_grid_str):
    """
    Transforms the input grid string according to the described rule.
    
    Args:
        input_grid_str: A string representing the input grid, 
                         with digits separated by spaces.
                         Example: "0 0 0 0 0 0 2 0 0 7 7 7"

    Returns:
        A string representing the transformed output grid, 
        with digits separated by spaces.
        Example: "0 7 7 7 0 0 2 0 0 0 0 0"
    """
    # Parse input string into a list of integers
    input_grid = [int(x) for x in input_grid_str.split()]
    n = len(input_grid)

    # Initialize output_grid with zeros
    output_grid = [0] * n

    # Find the pivot '2'
    pivot_index = find_pivot(input_grid)
    
    # Place the pivot in the output grid
    output_grid[pivot_index] = 2

    # Find the block details
    try:
        block_val, block_start_in, block_end_in, block_len = find_block(input_grid, pivot_index)
    except ValueError:
        # If no block is found (shouldn't happen based on examples), 
        # return the grid with just the pivot placed.
         return " ".join(map(str, output_grid))


    # Determine new block position based on mirroring
    new_block_start = -1
    
    if block_start_in > pivot_index: 
        # Block is currently AFTER the pivot
        # Calculate distance from pivot to start of block
        distance = block_start_in - pivot_index - 1
        # New block should end 'distance' away from pivot, on the other side
        new_block_end = pivot_index - distance - 1
        # Calculate new start based on new end and length
        new_block_start = new_block_end - block_len + 1
        
    elif block_end_in < pivot_index:
        # Block is currently BEFORE the pivot
        # Calculate distance from end of block to pivot
        distance = pivot_index - block_end_in - 1
        # New block should start 'distance' away from pivot, on the other side
        new_block_start = pivot_index + distance + 1
    else:
        # This case (block adjacent or overlapping pivot) is not represented 
        # in the examples and the logic might need adjustment if it occurs.
        # Assuming it doesn't happen based on provided examples.
        raise ValueError("Block appears adjacent to or overlapping the pivot, which is an undefined case.")

    # Check bounds for the new block position
    if new_block_start < 0 or (new_block_start + block_len) > n:
        # This indicates an issue with the logic or an unexpected input pattern
        # where the mirrored block goes out of bounds.
         raise ValueError(f"Calculated new block position [{new_block_start}-{new_block_start + block_len - 1}] is out of bounds [0-{n-1}].")


    # Place the block in the output grid
    for i in range(block_len):
        output_grid[new_block_start + i] = block_val

    # Format output list back into a space-separated string
    return " ".join(map(str, output_grid))

```
```python
import math
import re # Not strictly needed now, but kept from previous iteration just in case
import numpy as np # Allow input to be numpy array

"""
Reposition a contiguous block of identical non-zero digits relative to a fixed 
pivot digit '2' within a sequence of 12 integers. The block's position is 
mirrored across the pivot, maintaining the distance (number of zeros) between 
the pivot and the nearest edge of the block. If the block is initially before 
the pivot, it moves after the pivot in the output. If the block is initially 
after the pivot, it moves before the pivot in the output. All other positions 
in the output are filled with '0'.
"""

def find_pivot(grid):
  """Finds the index of the pivot element '2'."""
  # Convert to list if it's a numpy array for index method compatibility
  grid_list = list(grid) 
  try:
    return grid_list.index(2)
  except ValueError:
    raise ValueError("Pivot element '2' not found in the input grid.")

def find_block(grid):
  """Finds the non-zero, non-pivot block's value, start index, end index, and length."""
  block_val = -1
  block_start = -1
  block_end = -1
  n = len(grid)
  
  # Convert to list if it's a numpy array for easier iteration/checking
  grid_list = list(grid) 

  # Find the first non-zero, non-pivot element to determine block_val
  for i, val in enumerate(grid_list):
    if val != 0 and val != 2:
      block_val = val
      break
  
  if block_val == -1:
      # This case should not happen based on problem constraints/examples
      raise ValueError("No block value found (non-zero, non-2 digit).")

  # Find the start and end of the block
  in_block = False
  for i, val in enumerate(grid_list):
      if val == block_val and not in_block:
          block_start = i
          in_block = True
      # End condition: either value changes or we hit the pivot (block cannot contain pivot)
      elif (val != block_val or val == 2) and in_block: 
          block_end = i - 1
          break
          
  # Handle case where block extends to the end of the grid
  if in_block and block_end == -1:
      block_end = n - 1
      
  if block_start == -1:
      # This case should not happen
      raise ValueError(f"Block with value {block_val} not found.")

  block_len = block_end - block_start + 1
  return block_val, block_start, block_end, block_len


def transform(input_grid):
    """
    Transforms the input grid (list or numpy array) according to the mirroring rule.
    
    Args:
        input_grid: A list or numpy array of 12 integers representing the input state.

    Returns:
        A list of 12 integers representing the transformed output state.
    """
    n = len(input_grid)
    # Initialize output_grid with zeros
    output_grid = [0] * n

    # Find the pivot '2'
    pivot_index = find_pivot(input_grid)
    
    # Place the pivot in the output grid
    output_grid[pivot_index] = 2

    # Find the block details
    try:
        block_val, block_start_in, block_end_in, block_len = find_block(input_grid)
    except ValueError as e:
        # If no block is found (shouldn't happen based on examples), 
        # return the grid with just the pivot placed. This might occur
        # if the input violates assumptions.
        print(f"Warning/Error finding block: {e}. Returning grid with only pivot.")
        return output_grid


    # Determine new block position based on mirroring
    new_block_start = -1
    
    # Case 1: Block is AFTER the pivot in the input
    if block_start_in > pivot_index: 
        # Calculate distance (number of zeros) between pivot and start of block
        distance = block_start_in - pivot_index - 1
        # New block should end 'distance' away FROM pivot, on the other side (before pivot)
        new_block_end = pivot_index - distance - 1
        # Calculate new start based on new end and length
        new_block_start = new_block_end - block_len + 1
        
    # Case 2: Block is BEFORE the pivot in the input
    elif block_end_in < pivot_index:
        # Calculate distance (number of zeros) between end of block and pivot
        distance = pivot_index - block_end_in - 1
        # New block should start 'distance' away FROM pivot, on the other side (after pivot)
        new_block_start = pivot_index + distance + 1
        
    # Case 3: Block is adjacent or overlapping pivot (not expected from examples)
    else: 
        raise ValueError("Block appears adjacent to or overlapping the pivot, which is an undefined case based on examples.")

    # Check bounds for the new block position
    new_block_end_calc = new_block_start + block_len - 1
    if new_block_start < 0 or new_block_end_calc >= n:
         raise ValueError(f"Calculated new block position [{new_block_start}-{new_block_end_calc}] is out of bounds [0-{n-1}]. Pivot: {pivot_index}, Orig Block: [{block_start_in}-{block_end_in}]")

    # Place the block in the output grid
    for i in range(block_len):
        # Ensure we don't overwrite the pivot if bounds calculation somehow allows it
        if output_grid[new_block_start + i] == 2:
             raise ValueError(f"Attempting to overwrite pivot at index {pivot_index} with block value {block_val}.")
        output_grid[new_block_start + i] = block_val

    return output_grid
```
```python
import numpy as np # Using numpy for potential array operations, though lists work fine

"""
Mirrors the position of a contiguous block of identical non-zero digits 
relative to a fixed pivot digit '2' within a sequence of 12 integers. 
The mirroring preserves the distance (number of zeros) between the pivot 
and the nearest edge of the block. If the block is initially before the 
pivot, it moves after the pivot in the output. If the block is initially 
after the pivot, it moves before the pivot in the output. All other positions 
in the output are filled with '0'.
"""

def find_pivot(grid):
  """Finds the index of the pivot element '2'."""
  # Convert to list if it's a numpy array for index method compatibility
  grid_list = list(grid) 
  try:
    return grid_list.index(2)
  except ValueError:
    # This should not happen based on task constraints
    raise ValueError("Pivot element '2' not found in the input grid.")

def find_block(grid):
  """
  Finds the non-zero, non-pivot block's value, start index, end index, 
  and length. Assumes exactly one such block exists per constraints.
  """
  block_val = -1
  block_start = -1
  block_end = -1
  n = len(grid)
  
  # Convert to list if it's a numpy array for easier iteration/checking
  grid_list = list(grid) 

  # Find the first non-zero, non-pivot element to determine block_val
  for i, val in enumerate(grid_list):
    if val != 0 and val != 2:
      block_val = val
      break
  
  if block_val == -1:
      # This case should not happen based on problem constraints/examples
      raise ValueError("No block value found (non-zero, non-2 digit).")

  # Find the start and end of the block
  in_block = False
  for i, val in enumerate(grid_list):
      # Start of the block
      if val == block_val and not in_block:
          block_start = i
          in_block = True
          block_end = i # Initialize end in case block has length 1
      # Continuation of the block
      elif val == block_val and in_block:
          block_end = i
      # End of the block (value changes or hits pivot)
      elif (val != block_val or val == 2) and in_block: 
          # block_end is already correctly set to the last index of the block
          break # Found the full block extent

  # Check if block was found        
  if block_start == -1:
      # This case should not happen
      raise ValueError(f"Block with value {block_val} not found or logic error.")

  block_len = block_end - block_start + 1
  return block_val, block_start, block_end, block_len

def transform(input_grid):
    """
    Transforms the input grid (list or numpy array) according to the mirroring rule.
    
    Args:
        input_grid: A list or numpy array of 12 integers representing the input state.

    Returns:
        A list of 12 integers representing the transformed output state.
    """
    # Ensure input is a list for consistent processing
    input_list = list(input_grid)
    n = len(input_list)

    # 1. Initialize output_grid with zeros
    output_grid = [0] * n

    # 2. Find Pivot and place it in the output
    pivot_idx = find_pivot(input_list)
    output_grid[pivot_idx] = 2

    # 3. Find Block details
    try:
        block_val, block_start_in, block_end_in, block_len = find_block(input_list)
    except ValueError as e:
        # Handle potential error if assumptions are violated, return grid with pivot only
        print(f"Error finding block: {e}. Returning grid with only pivot.")
        return output_grid

    # 4. Calculate Gap (distance)
    distance = -1
    new_block_start = -1
    
    # Case A: Block is AFTER the pivot in the input
    if block_start_in > pivot_idx: 
        distance = block_start_in - pivot_idx - 1 # Zeros between pivot and block start
        
        # 5. Determine New Position (Mirroring) - Block moves BEFORE pivot
        new_block_end = pivot_idx - distance - 1
        new_block_start = new_block_end - block_len + 1
        
    # Case B: Block is BEFORE the pivot in the input
    elif block_end_in < pivot_idx:
        distance = pivot_idx - block_end_in - 1 # Zeros between block end and pivot
        
        # 5. Determine New Position (Mirroring) - Block moves AFTER pivot
        new_block_start = pivot_idx + distance + 1
        
    # Case C: Block adjacent/overlapping (Error based on constraints)
    else: 
        raise ValueError("Block appears adjacent to or overlapping the pivot, violating constraints.")

    # --- Boundary Checks (Optional but good practice) ---
    new_block_end_calc = new_block_start + block_len - 1
    if new_block_start < 0 or new_block_end_calc >= n:
         # This indicates an issue with the logic or an unexpected input violating constraints
         raise ValueError(f"Calculated new block position [{new_block_start}-{new_block_end_calc}] is out of bounds [0-{n-1}]. Input: {input_list}")
    # --- End Boundary Checks ---

    # 6. Place Block in the output grid
    for i in range(block_len):
        current_idx = new_block_start + i
        # Ensure we don't overwrite the pivot (shouldn't happen with correct logic/constraints)
        if output_grid[current_idx] != 0:
             raise ValueError(f"Attempting to overwrite existing value {output_grid[current_idx]} at index {current_idx} with block value {block_val}. Output should be 0.")
        output_grid[current_idx] = block_val

    # 7. Finalize and return
    return output_grid
```
