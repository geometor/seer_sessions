
## train_1

**input:**
```
0 0 3 3 0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 3 3 0 0 0 0 2 0
```


## train_2

**input:**
```
5 5 5 0 2 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 2 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 7 0 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 7 0 0 0 0 2 0 0 0
```


## train_4

**input:**
```
1 1 1 1 1 2 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 2 0 0 0 0 0 0
```


## train_5

**input:**
```
0 2 0 0 0 0 0 1 1 1 1 1
```


**output:**
```
0 2 0 0 0 1 1 1 1 1 0 0
```


## train_6

**input:**
```
6 6 6 6 6 6 6 6 2 0 0 0
```


**output:**
```
6 6 6 6 6 6 6 6 2 0 0 0
```


## train_7

**input:**
```
0 0 2 0 8 8 8 8 8 8 8 8
```


**output:**
```
0 0 2 8 8 8 8 8 8 8 8 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Data Structure:** The input and output are sequences (lists) of 12 integers.
2.  **Key Element '2':** The number `2` appears exactly once in every input and output sequence. Its position remains unchanged during the transformation. It acts as a fixed pivot point.
3.  **Data Block:** Apart from the `2` and `0`s, there is typically a contiguous block of other non-zero integers (e.g., `3 3`, `5 5 5`, `7`, `1 1 1 1 1`, `8 8 8 8 8 8 8 8`). Let's call this the "data block". In some cases (`train_4`, `train_6`), the `2` is immediately adjacent to this block.
4.  **Zeros:** Zeros act as background or padding elements.
5.  **Transformation:** The core transformation involves shifting the "data block" relative to the fixed position of the `2`. Zeros fill the space created or displaced by the shift.
6.  **Shift Logic:**
    *   If the data block is to the left of the `2`, it shifts rightwards towards the `2`.
    *   If the data block is to the right of the `2`, it shifts leftwards towards the `2`.
    *   If the data block is already adjacent to the `2` (or if there's no data block other than `2`), no shift occurs.
7.  **Shift Amount:** The amount of the shift depends on the gap (number of zeros) between the data block and the `2`.
    *   If the gap is 0 (adjacent), the shift is 0.
    *   If the gap is 1, the shift is 1 position (towards the `2`).
    *   If the gap is greater than 1, the shift is 2 positions (towards the `2`).

**YAML Facts:**


```yaml
Objects:
  - Sequence:
      Properties:
        - Type: List of Integers
        - Length: 12
  - Pivot:
      Properties:
        - Value: 2
        - Count: 1
        - Position: Fixed (remains same in output as input)
  - DataBlock:
      Properties:
        - Type: Contiguous sub-sequence of non-zero integers (excluding Pivot)
        - Existence: Typically one per sequence (can be absent or adjacent to Pivot)
        - Position: Relative to Pivot (Left, Right, Adjacent)
        - Length: Variable
  - Filler:
      Properties:
        - Value: 0
        - Role: Background, occupies space not used by Pivot or DataBlock

Relationships:
  - RelativePosition: Between DataBlock and Pivot (Left, Right, Adjacent)
  - Gap:
      Properties:
        - Type: Number of Fillers (zeros) strictly between DataBlock and Pivot
        - Value: Integer >= 0

Actions:
  - LocatePivot: Find the index of the Pivot (value 2).
  - IdentifyDataBlock: Find the start index, end index, and values of the contiguous non-zero sequence (excluding Pivot).
  - CalculateGap: Determine the number of zeros between the DataBlock and the Pivot based on their indices.
  - DetermineShift:
      Based on Gap:
        - If Gap = 0, Shift Amount = 0
        - If Gap = 1, Shift Amount = 1
        - If Gap > 1, Shift Amount = 2
      Based on RelativePosition:
        - If DataBlock is Left of Pivot, Shift Direction = Right
        - If DataBlock is Right of Pivot, Shift Direction = Left
        - If DataBlock is Adjacent or Absent, Shift Direction = None
  - ApplyShift: Calculate the new start and end indices for the DataBlock.
  - ConstructOutput: Create a new sequence of length 12, place the Pivot at its original index, place the shifted DataBlock at its new indices, and fill remaining positions with Filler (0).

```


**Natural Language Program:**

1.  Receive the input sequence of 12 integers.
2.  Find the index (position) of the integer `2`; this is the `pivot_index`.
3.  Scan the input sequence to locate the contiguous block of non-zero integers, excluding the `2`. Record its starting index (`block_start`), ending index (`block_end`), and the sequence of values (`block_values`). If no such block exists, proceed to step 8.
4.  Determine the relative position of the block to the `pivot_index`:
    *   If `block_end < pivot_index`, the block is "Left".
    *   If `block_start > pivot_index`, the block is "Right".
    *   Otherwise, the block is "Adjacent".
5.  Calculate the `gap` (number of zeros strictly between the block and the `2`):
    *   If "Left", `gap = pivot_index - block_end - 1`.
    *   If "Right", `gap = block_start - pivot_index - 1`.
    *   If "Adjacent", `gap = 0`.
6.  Calculate the `shift_amount`:
    *   If `gap == 0`, `shift_amount = 0`.
    *   If `gap == 1`, `shift_amount = 1`.
    *   If `gap > 1`, `shift_amount = 2`.
7.  Calculate the new indices for the block (`new_block_start`, `new_block_end`):
    *   If "Left", `new_block_start = block_start + shift_amount`, `new_block_end = block_end + shift_amount`.
    *   If "Right", `new_block_start = block_start - shift_amount`, `new_block_end = block_end - shift_amount`.
    *   If "Adjacent", `new_block_start = block_start`, `new_block_end = block_end`.
8.  Create the output sequence, initially filled with 12 zeros.
9.  Place the integer `2` at the `pivot_index` in the output sequence.
10. If a data block was found in step 3, place the `block_values` into the output sequence starting at `new_block_start` and ending at `new_block_end`.
11. Return the completed output sequence.
```python
import re

"""
Transformation Rule Natural Language Description:

1.  Identify the fixed pivot element '2' within the 12-integer sequence. Its position remains unchanged.
2.  Locate the contiguous block of non-zero integers (excluding the '2'), referred to as the 'data block'. Note its start index, end index, and values. If no such block exists, the sequence remains unchanged except for the pivot.
3.  Determine the relative position of the data block with respect to the pivot ('Left', 'Right', or 'Adjacent').
4.  Calculate the gap, defined as the number of zeros strictly between the data block and the pivot.
5.  Determine the shift amount based on the gap: 0 if the gap is 0 (adjacent), 1 if the gap is 1, and 2 if the gap is greater than 1.
6.  Calculate the new start and end indices for the data block by shifting it towards the pivot by the calculated shift amount.
7.  Construct the output sequence by placing the pivot '2' at its original position, placing the data block at its new calculated position, and filling all other positions with zeros.
"""

def find_pivot(sequence):
    """Finds the index of the pivot element (2)."""
    try:
        return sequence.index(2)
    except ValueError:
        # Should not happen based on problem description, but good practice
        return -1 

def find_data_block(sequence, pivot_index):
    """
    Finds the first contiguous block of non-zero, non-pivot integers.
    Returns (start_index, end_index, values) or (None, None, None) if no block found.
    """
    block_start = -1
    block_values = []
    
    for i, val in enumerate(sequence):
        is_block_element = (val != 0 and i != pivot_index)
        
        if is_block_element and block_start == -1:
            # Start of a potential block
            block_start = i
            block_values.append(val)
        elif is_block_element and block_start != -1:
            # Continuing a block
            block_values.append(val)
        elif not is_block_element and block_start != -1:
            # End of the block found
            block_end = i - 1
            return block_start, block_end, block_values
            
    # Check if block runs to the end of the sequence
    if block_start != -1:
        block_end = len(sequence) - 1
        return block_start, block_end, block_values
        
    # No block found
    return None, None, None


def transform(input_str):
    """
    Applies the transformation rule to the input sequence string.
    
    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the 12 space-separated integers of the transformed sequence.
    """
    # Parse input string into a list of integers
    input_sequence = [int(x) for x in input_str.split()]
    n = len(input_sequence)
    
    # Initialize output_sequence with zeros
    output_sequence = [0] * n

    # 1. Find the pivot index
    pivot_index = find_pivot(input_sequence)
    if pivot_index == -1:
        # Handle error case if pivot '2' is not found (though examples imply it always exists)
        return " ".join(map(str, input_sequence)) # Return original if no pivot

    # Place pivot in the output sequence (it never moves)
    output_sequence[pivot_index] = 2

    # 2. Find the data block
    block_start, block_end, block_values = find_data_block(input_sequence, pivot_index)

    # If no data block found, the transformation is just placing the pivot
    if block_start is None:
        return " ".join(map(str, output_sequence))

    # 3. Determine relative position and 4. Calculate gap
    gap = 0
    relative_position = "Adjacent" # Default assumption
    if block_end < pivot_index:
        relative_position = "Left"
        gap = pivot_index - block_end - 1
    elif block_start > pivot_index:
        relative_position = "Right"
        gap = block_start - pivot_index - 1
        
    # Ensure gap isn't negative (can happen if adjacent)
    gap = max(0, gap) 

    # 5. Calculate shift amount
    shift_amount = 0
    if gap == 1:
        shift_amount = 1
    elif gap > 1:
        shift_amount = 2
        
    # 6. Calculate new block indices
    new_block_start = block_start
    new_block_end = block_end

    if relative_position == "Left":
        new_block_start += shift_amount
        new_block_end += shift_amount
    elif relative_position == "Right":
        new_block_start -= shift_amount
        new_block_end -= shift_amount
        
    # Ensure indices stay within bounds (shouldn't be necessary with correct logic, but safe)
    new_block_start = max(0, new_block_start)
    new_block_end = min(n - 1, new_block_end)

    # 7. Construct output: Place the shifted data block
    # Make sure the target slice has the correct length
    block_len = len(block_values)
    # Recalculate end based on start and length for safety
    actual_new_block_end = new_block_start + block_len -1 

    # Check potential index overlap with pivot before placing
    current_idx = new_block_start
    for val in block_values:
         # Ensure we don't overwrite the pivot's fixed position
         # If the target index is the pivot index, skip writing this value
         # (This implicitly handles cases where block 'collides' with pivot)
        if current_idx != pivot_index and 0 <= current_idx < n:
             output_sequence[current_idx] = val
        current_idx += 1

    # Return the transformed sequence as a space-separated string
    return " ".join(map(str, output_sequence))

```
