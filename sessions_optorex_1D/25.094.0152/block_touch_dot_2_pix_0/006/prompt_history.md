
## train_1

**input:**
```
0 0 0 0 0 0 0 0 2 9 9 9
```


**output:**
```
0 0 0 0 0 0 0 0 2 9 9 9
```


## train_2

**input:**
```
0 0 7 7 7 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 0 2 0 0 0
```


## train_3

**input:**
```
0 4 4 4 4 0 2 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 2 0 0 0 0 0
```


## train_4

**input:**
```
6 6 6 0 0 2 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 2 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 2 0 0 0 3 3 3 3 3 0
```


**output:**
```
0 0 2 0 3 3 3 3 3 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 2 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 2 7 7 7
```


## train_7

**input:**
```
2 0 3 3 3 3 3 3 3 3 3 0
```


**output:**
```
2 3 3 3 3 3 3 3 3 3 0 0
```

Okay, let's break down the transformation logic for these examples.

**Perception of Elements:**

1.  **Data Format:** The input and output are sequences of single-digit integers, presented as space-separated strings. They can be interpreted as 1D arrays or lists.
2.  **Key Digits:**
    *   `0`: Appears to represent empty space or background.
    *   `2`: Acts as a fixed point or separator. Its position does not change from input to output.
    *   Other non-zero digits (`3`, `4`, `6`, `7`, `9` in the examples): Form contiguous blocks.
3.  **Core Transformation:** The primary action is the shifting of the contiguous block of non-zero digits (excluding '2') towards the '2'.
4.  **Direction of Shift:**
    *   If the block is initially to the left of '2', it shifts rightward until its rightmost digit is immediately adjacent to the left of '2'.
    *   If the block is initially to the right of '2', it shifts leftward until its leftmost digit is immediately adjacent to the right of '2'.
5.  **Integrity:** The digits within the non-zero block maintain their relative order during the shift. The length of the sequence remains constant.
6.  **Filling:** The positions previously occupied by the shifted block become '0'.

**YAML Facts:**


```yaml
task_description: "Shift a contiguous block of non-zero digits (excluding '2') adjacent to the fixed digit '2'."
elements:
  - object: Sequence
    description: "A 1D list of single-digit integers."
    properties:
      - length: Integer, the number of digits in the sequence.
      - digits: List of integers [0-9].
  - object: Separator
    description: "The digit '2' which serves as a fixed anchor point."
    properties:
      - value: 2
      - index: Integer, the position of '2' in the sequence (remains constant).
  - object: NumberBlock
    description: "A contiguous sub-sequence of digits that are not '0' and not '2'."
    properties:
      - digits: List of non-zero, non-2 integers.
      - start_index: Integer, the starting position in the input sequence.
      - end_index: Integer, the ending position in the input sequence.
      - length: Integer, the number of digits in the block.
      - relative_position: String, either 'left_of_separator' or 'right_of_separator'.
  - object: Zero
    description: "The digit '0' representing empty space."
    properties:
      - value: 0
actions:
  - action: FindSeparator
    description: "Locate the index of the digit '2' in the input sequence."
    inputs: [InputSequence]
    outputs: [separator_index]
  - action: FindNumberBlock
    description: "Identify the contiguous block of non-zero, non-2 digits, its start/end indices, and its position relative to the separator."
    inputs: [InputSequence, separator_index]
    outputs: [NumberBlock (or null if none exists)]
  - action: ShiftBlock
    description: "Calculate the target start and end indices for the NumberBlock in the output sequence, placing it adjacent to the Separator."
    inputs: [NumberBlock, separator_index, sequence_length]
    outputs: [target_start_index, target_end_index]
  - action: ConstructOutput
    description: "Create the output sequence by placing the Separator at its original index, the NumberBlock at its target indices, and filling remaining positions with '0'."
    inputs: [sequence_length, separator_index, Separator.value, target_start_index, target_end_index, NumberBlock.digits]
    outputs: [OutputSequence]
relationships:
  - type: Adjacency
    description: "The NumberBlock in the output sequence is positioned immediately next to the Separator."
    condition_left: "If NumberBlock was left_of_separator, its end_index in output is separator_index - 1."
    condition_right: "If NumberBlock was right_of_separator, its start_index in output is separator_index + 1."
  - type: Preservation
    description: "The Separator ('2') maintains its original index. The relative order of digits within the NumberBlock is preserved."
  - type: Replacement
    description: "Positions not occupied by the Separator or the shifted NumberBlock in the output sequence are filled with Zero ('0')."
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Find the index of the digit '2' (the separator).
3.  Scan the sequence to find the start and end indices of the contiguous block of digits that are neither '0' nor '2'. Record the digits within this block.
4.  If no such block exists, the output is identical to the input; stop.
5.  Determine if the identified block is located to the left or right of the separator's index.
6.  Create a new output sequence of the same length as the input, initially filled entirely with '0'.
7.  Place the digit '2' into the output sequence at its original index (found in step 2).
8.  If the block was found to the left of the separator:
    a. Calculate the target end index for the block in the output sequence as `separator_index - 1`.
    b. Calculate the target start index as `target_end_index - length_of_block + 1`.
    c. Copy the recorded block digits into the output sequence from the target start index to the target end index.
9.  If the block was found to the right of the separator:
    a. Calculate the target start index for the block in the output sequence as `separator_index + 1`.
    b. Calculate the target end index as `target_start_index + length_of_block - 1`.
    c. Copy the recorded block digits into the output sequence from the target start index to the target end index.
10. Return the constructed output sequence.
```python
import re

"""
Shift a contiguous block of non-zero digits (excluding '2') to be adjacent 
to the fixed digit '2'. The '2' acts as a separator, and its position remains 
unchanged. Digits '0' fill the remaining space. If the block is to the left of 
'2', it moves right until its rightmost digit touches '2'. If the block is to 
the right of '2', it moves left until its leftmost digit touches '2'. If no 
such block exists, the input remains unchanged.
"""

def find_separator_index(grid):
    """Finds the index of the digit '2'."""
    try:
        return grid.index(2)
    except ValueError:
        return -1 # Indicate '2' not found

def find_number_block(grid, separator_index):
    """
    Finds the contiguous block of digits that are not 0 and not 2.
    Returns a tuple: (block_digits, start_index, end_index) or None if not found.
    """
    block_digits = []
    start_index = -1
    end_index = -1
    in_block = False

    for i, digit in enumerate(grid):
        if digit != 0 and digit != 2:
            if not in_block:
                start_index = i
                in_block = True
            block_digits.append(digit)
            end_index = i # Keep updating end_index while in block
        elif in_block:
            # Found the end of the block
            break # Assume only one block per line as per examples

    if not block_digits:
        return None
    else:
        return block_digits, start_index, end_index

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string representing the sequence.

    Args:
        input_str: A space-separated string of digits.

    Returns:
        A space-separated string of digits representing the transformed sequence.
    """
    # 1. Read the input sequence of digits.
    input_grid = [int(d) for d in input_str.split()]
    n = len(input_grid)

    # 2. Find the index of the digit '2' (the separator).
    separator_index = find_separator_index(input_grid)

    # Handle case where '2' is not present (though not seen in examples)
    if separator_index == -1:
        return input_str # Or handle as error, based on task rules

    # 3. Scan the sequence to find the contiguous block of non-zero, non-2 digits.
    block_info = find_number_block(input_grid, separator_index)

    # 4. If no such block exists, the output is identical to the input.
    if block_info is None:
        return input_str

    block_digits, block_start, block_end = block_info
    block_length = len(block_digits)

    # 6. Create a new output sequence of the same length, initially filled with '0'.
    output_grid = [0] * n

    # 7. Place the digit '2' into the output sequence at its original index.
    output_grid[separator_index] = 2

    # 5. Determine if the block is left or right of the separator.
    # 8. If the block was found to the left of the separator:
    if block_start < separator_index:
        # a. Calculate the target end index.
        target_end_index = separator_index - 1
        # b. Calculate the target start index.
        target_start_index = target_end_index - block_length + 1
        # c. Copy the block digits into the output sequence.
        output_grid[target_start_index : target_end_index + 1] = block_digits
    # 9. If the block was found to the right of the separator:
    elif block_start > separator_index:
        # a. Calculate the target start index.
        target_start_index = separator_index + 1
        # b. Calculate the target end index.
        target_end_index = target_start_index + block_length - 1
        # c. Copy the block digits into the output sequence.
        output_grid[target_start_index : target_end_index + 1] = block_digits
    # Handle edge case where block contains '2' (shouldn't happen based on find_number_block logic)
    # or if block start == separator_index (also shouldn't happen)

    # 10. Return the constructed output sequence as a string.
    return " ".join(map(str, output_grid))

```
```python
import numpy as np

"""
Shift a contiguous block of non-zero digits (excluding 2) within a 1D numerical 
array to be adjacent to the fixed digit 2. The digit 2 acts as a separator, 
and its position remains unchanged. Digits 0 fill the remaining space. If the 
block is initially to the left of 2, it moves rightward until its rightmost digit 
is immediately adjacent to the left of 2. If the block is initially to the 
right of 2, it shifts leftward until its leftmost digit is immediately adjacent 
to the right of 2. If no such block exists or if 2 is not present, the input 
array remains unchanged. Assumes only one such contiguous block exists per input.
"""

def find_separator_index(grid: np.ndarray) -> int:
    """
    Locates the index of the digit 2 (separator) in the input array.

    Args:
        grid: The 1D input NumPy array.

    Returns:
        The index of the first occurrence of 2, or -1 if not found.
    """
    separator_indices = np.where(grid == 2)[0]
    if len(separator_indices) > 0:
        return separator_indices[0]
    else:
        return -1

def find_number_block(grid: np.ndarray, separator_index: int):
    """
    Finds the single contiguous block of digits that are not 0 and not 2.

    Args:
        grid: The 1D input NumPy array.
        separator_index: The index of the separator (2).

    Returns:
        A tuple: (block_digits, start_index, end_index) 
        or None if no such contiguous block is found.
        block_digits is a NumPy array slice.
    """
    # Find indices of all elements that are neither 0 nor 2
    candidate_indices = np.where((grid != 0) & (grid != 2))[0]

    if len(candidate_indices) == 0:
        return None # No block found

    # Check for contiguity
    if len(candidate_indices) == 1:
        # Single element block is contiguous
        start_index = candidate_indices[0]
        end_index = candidate_indices[0]
        block_digits = grid[start_index : end_index + 1]
        return block_digits, start_index, end_index
    elif np.all(np.diff(candidate_indices) == 1):
        # Multiple elements, check if differences are all 1
        start_index = candidate_indices[0]
        end_index = candidate_indices[-1]
        block_digits = grid[start_index : end_index + 1]
        return block_digits, start_index, end_index
    else:
        # Indices exist but are not contiguous - assumes this case won't happen based on examples
        # Or could indicate multiple blocks, which is also not handled based on examples
        # Returning None for now, implying no *single contiguous* block found
        return None 


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Get the size of the input grid
    n = input_grid.shape[0]

    # 1. Find the index of the separator '2'.
    separator_index = find_separator_index(input_grid)

    # If separator '2' is not found, return the original grid.
    if separator_index == -1:
        return input_grid.copy() # Return a copy to avoid modifying original if needed elsewhere

    # 2. Find the contiguous block of non-zero, non-2 digits.
    block_info = find_number_block(input_grid, separator_index)

    # 3. If no such block exists, return the original grid (with '2' present).
    if block_info is None:
         # Check if block is *already* adjacent (special case of 'no shift needed')
         # Although the main logic below handles this, explicit check might be clearer
         # For train_1 and train_6, block_info will be None because the block is already adjacent in those cases
         # Let's re-evaluate find_number_block: it should find the block regardless of adjacency.
         # The issue might be in how find_number_block was interpreted. Let's assume it finds ANY block.

         # Re-find the block without assuming non-adjacency
         block_info = find_number_block(input_grid, separator_index) # Call again for clarity

         if block_info is None: # Truly no block
             return input_grid.copy()

         block_digits, block_start, block_end = block_info
         # Check if already adjacent
         if block_end == separator_index - 1 or block_start == separator_index + 1:
             return input_grid.copy() # Already in the correct place
         # If block exists but wasn't adjacent, proceed. If truly no block, return above.

    # If block_info was initially None (no non-zero/non-2 digits), we already returned.
    # If block exists and is not adjacent, proceed:
    block_digits, block_start, block_end = block_info
    block_length = len(block_digits)

    # 4. Initialize the output grid with zeros, preserving shape and dtype.
    output_grid = np.zeros_like(input_grid)

    # 5. Place the separator '2' in the output grid at its original position.
    output_grid[separator_index] = 2

    # 6. Determine if the block was to the left or right of the separator.
    if block_start < separator_index:
        # Block is to the left, shift it right.
        # Calculate target end index (adjacent to the left of '2')
        target_end_index = separator_index - 1
        # Calculate target start index
        target_start_index = target_end_index - block_length + 1
        
        # Check for boundary issues (shouldn't happen if input is valid)
        if target_start_index < 0:
             # This case implies the block + separator wouldn't fit,
             # which contradicts the problem setup where lengths are preserved.
             # Handle defensively or assume valid inputs.
             # For now, assume valid inputs based on examples.
             pass # Or raise an error?

        # 7a. Copy the block digits to the target position in the output grid.
        output_grid[target_start_index : target_end_index + 1] = block_digits

    elif block_start > separator_index:
        # Block is to the right, shift it left.
        # Calculate target start index (adjacent to the right of '2')
        target_start_index = separator_index + 1
        # Calculate target end index
        target_end_index = target_start_index + block_length - 1

        # Check for boundary issues
        if target_end_index >= n:
            # Similar to the left case, implies block + separator don't fit.
            # Assume valid inputs.
            pass

        # 7b. Copy the block digits to the target position in the output grid.
        output_grid[target_start_index : target_end_index + 1] = block_digits
        
    # If block_start == separator_index, this shouldn't happen because find_number_block excludes '2'.

    # 8. Return the constructed output grid.
    return output_grid
```
```python
import numpy as np

"""
Shift a contiguous block of non-zero digits (excluding 2) within a 1D numerical 
array to be adjacent to the fixed digit 2, unless the block is already adjacent. 
The digit 2 acts as a separator, and its position remains unchanged. Digits 0 
fill the remaining space. If the block is initially to the left of 2, it moves 
rightward until its rightmost digit is immediately adjacent to the left of 2. 
If the block is initially to the right of 2, it shifts leftward until its 
leftmost digit is immediately adjacent to the right of 2. If no such block 
exists, if 2 is not present, or if the block is already adjacent to 2, the 
input array remains unchanged. Assumes at most one such contiguous block exists 
per input.
"""

def find_separator_index(grid: np.ndarray) -> int:
    """
    Locates the index of the digit 2 (separator) in the input array.

    Args:
        grid: The 1D input NumPy array.

    Returns:
        The index of the first occurrence of 2, or -1 if not found.
    """
    separator_indices = np.where(grid == 2)[0]
    if len(separator_indices) > 0:
        # Assuming only one '2' based on examples, take the first found
        return separator_indices[0]
    else:
        return -1

def find_number_block(grid: np.ndarray):
    """
    Finds the single contiguous block of digits that are not 0 and not 2.

    Args:
        grid: The 1D input NumPy array.

    Returns:
        A dictionary containing 'digits' (list), 'start' (int), 'end' (int), 
        and 'len' (int) of the block, or None if no such single contiguous 
        block is found.
    """
    # Find indices of all potential block elements
    candidate_indices = np.where((grid != 0) & (grid != 2))[0]

    if len(candidate_indices) == 0:
        return None # No block elements found

    # Check for contiguity: difference between consecutive indices should be 1
    if len(candidate_indices) == 1:
        # A single element is always contiguous
        is_contiguous = True
    else:
        is_contiguous = np.all(np.diff(candidate_indices) == 1)

    if is_contiguous:
        start_index = candidate_indices[0]
        end_index = candidate_indices[-1]
        block_digits = grid[start_index : end_index + 1]
        return {
            "digits": block_digits.tolist(), # Return as list for easier slicing later
            "start": start_index,
            "end": end_index,
            "len": len(block_digits)
        }
    else:
        # Found non-zero/non-2 elements, but they don't form a single contiguous block.
        # Based on problem description/examples, we assume this won't happen or 
        # means no valid block exists for the transformation rule.
        return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Get the size of the input grid
    n = input_grid.shape[0]

    # 1. Find the index of the separator '2'.
    separator_index = find_separator_index(input_grid)

    # If separator '2' is not found, return the original grid.
    if separator_index == -1:
        return input_grid.copy() 

    # 2. Find the contiguous block of non-zero, non-2 digits.
    block_info = find_number_block(input_grid)

    # 3. If no such block exists, return the original grid.
    if block_info is None:
        return input_grid.copy()

    # 4. Check if the block is already adjacent to the separator.
    block_start = block_info["start"]
    block_end = block_info["end"]
    is_adjacent_left = (block_end == separator_index - 1)
    is_adjacent_right = (block_start == separator_index + 1)

    if is_adjacent_left or is_adjacent_right:
        # Block is already in the correct position, return original grid.
        return input_grid.copy()

    # 5. If the block exists and is *not* adjacent, perform the shift.
    
    # 5a. Initialize the output grid with zeros.
    output_grid = np.zeros_like(input_grid)

    # 5b. Place the separator '2' in the output grid.
    output_grid[separator_index] = 2

    # 5c. Determine target position based on original relative position.
    block_digits = np.array(block_info["digits"]) # Convert back to numpy array for assignment
    block_length = block_info["len"]
    
    if block_start < separator_index:
        # Block was to the left, move it right against the separator.
        target_end_index = separator_index - 1
        target_start_index = target_end_index - block_length + 1
    else: # block_start > separator_index (cannot be equal due to find_number_block logic)
        # Block was to the right, move it left against the separator.
        target_start_index = separator_index + 1
        target_end_index = target_start_index + block_length - 1

    # 5d. Check for boundary issues (optional, assumes valid inputs based on problem)
    # if target_start_index < 0 or target_end_index >= n:
    #     # Handle error: block shift leads out of bounds.
    #     # Based on examples, this shouldn't happen.
    #     return input_grid.copy() # Or raise an error

    # 5e. Copy the block digits to the target position in the output grid.
    if 0 <= target_start_index <= target_end_index < n: # Basic boundary check
         output_grid[target_start_index : target_end_index + 1] = block_digits
    else:
         # Handle unexpected boundary issue if necessary
         print(f"Warning: Calculated target indices [{target_start_index}, {target_end_index}] seem out of bounds for grid size {n}.")
         return input_grid.copy() # Fallback to input if calculation is wrong


    # 6. Return the constructed output grid.
    return output_grid
```
