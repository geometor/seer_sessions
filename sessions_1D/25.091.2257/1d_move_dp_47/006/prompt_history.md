
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 1 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
```


## train_2

**input:**
```
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 1 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 1 0
```

*   **Perception of task elements:**
    *   The input and output are single-row grids (1D arrays) of the same length.
    *   Each input grid contains a distinct structure: an optional initial block of white pixels (0), followed by a contiguous block of a single non-white, non-blue color (the "color block"), followed by a contiguous block of white pixels (the "middle zero block"), and finally ending with a fixed sequence of a blue pixel (1) followed by a white pixel (0).
    *   The output grid rearranges these blocks. The initial white block (if present) remains at the beginning. The "middle zero block" is moved to immediately follow the initial white block. The "color block" is moved to immediately follow the relocated "middle zero block". The final blue-white sequence `[1, 0]` remains at the very end of the grid.
    *   The transformation is essentially swapping the positions of the "color block" and the "middle zero block" relative to each other, while keeping the start and end segments fixed.

*   **YAML Facts:**
    
```yaml
    GridDimensions:
      Input: 1xN
      Output: 1xN
    Objects:
      - Name: EndSequence
        Pattern: [1, 0] (Blue, White)
        Position: Always the last two elements of the grid.
        Transformation: Remains fixed at the end.
      - Name: MiddleZeroBlock
        Pattern: Contiguous sequence of 0 (White)
        Position: Immediately precedes the EndSequence in the input.
        Transformation: Moved earlier in the sequence in the output.
      - Name: ColorBlock
        Pattern: Contiguous sequence of a single color C (where C is not 0 or 1).
        Position: Immediately precedes the MiddleZeroBlock in the input.
        Transformation: Moved later in the sequence in the output (after the MiddleZeroBlock).
      - Name: InitialPart
        Pattern: Any sequence of elements preceding the ColorBlock (can be empty or contain only 0s).
        Position: At the beginning of the grid, before the ColorBlock.
        Transformation: Remains fixed at the beginning.
    Relationships:
      - Input Order: InitialPart -> ColorBlock -> MiddleZeroBlock -> EndSequence
      - Output Order: InitialPart -> MiddleZeroBlock -> ColorBlock -> EndSequence
    Action:
      - Reorder the identified blocks according to the Output Order.
    ```


*   **Natural Language Program:**
    1.  Identify the fixed sequence `[1, 0]` (blue, white) at the end of the input grid.
    2.  Identify the contiguous block of white pixels (0) located immediately before the `[1, 0]` sequence. Call this the `MiddleZeroBlock`.
    3.  Identify the contiguous block of a single non-white, non-blue color located immediately before the `MiddleZeroBlock`. Call this the `ColorBlock`.
    4.  Identify all elements preceding the `ColorBlock`. Call this the `InitialPart`.
    5.  Construct the output grid by concatenating the `InitialPart`, followed by the `MiddleZeroBlock`, followed by the `ColorBlock`, and finally followed by the fixed `[1, 0]` sequence.
```python
import numpy as np
from typing import List

"""
Identifies segments within a 1D input grid and rearranges them.

The input grid is expected to have the structure:
[InitialPart][ColorBlock][MiddleZeroBlock][EndSequence]
where:
- EndSequence is always [1, 0] (blue, white) at the very end.
- MiddleZeroBlock is a contiguous block of 0s (white) immediately preceding the EndSequence.
- ColorBlock is a contiguous block of a single non-white, non-blue color immediately preceding the MiddleZeroBlock.
- InitialPart is everything before the ColorBlock (can be empty or contain only 0s).

The transformation swaps the positions of the ColorBlock and the MiddleZeroBlock:
Output = [InitialPart][MiddleZeroBlock][ColorBlock][EndSequence]
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by rearranging identified blocks.

    Args:
        input_grid: A list containing a single list of integers representing the 1xN grid.

    Returns:
        A list containing a single list of integers representing the transformed 1xN grid.
    """
    # Ensure input is a 1D array (represented as a list within a list)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle error or unexpected format if necessary
        # For now, assume valid input based on examples
        # Or raise ValueError("Input must be a list containing a single list (1xN grid)")
        # Based on examples, let's try to handle flat list input too
        if isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
             row = input_grid # Treat as the row directly
        else:
             # If it's not a flat list either, it's unexpected format
             raise ValueError("Input format not recognized. Expected List[List[int]] or List[int].")
    else:
        row = input_grid[0]


    n = len(row)

    # 1. Identify the fixed EndSequence [1, 0]
    if n < 2 or row[n-2:] != [1, 0]:
        # If the end sequence is not [1, 0] or grid is too short,
        # return the original grid or handle as an error.
        # Based on task description, this sequence is always present.
        # Returning original wrapped in list of lists format if needed.
        if isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
            return [row] 
        else:
             return input_grid


    end_sequence = [1, 0]
    idx_before_end = n - 3 # Index of the last element before the end sequence

    # 2. Identify the MiddleZeroBlock (contiguous 0s before EndSequence)
    i = idx_before_end
    while i >= 0 and row[i] == 0:
        i -= 1
    start_idx_middle_zero = i + 1
    # Slice the middle zero block
    middle_zero_block = row[start_idx_middle_zero : idx_before_end + 1]

    # 3. Identify the ColorBlock (contiguous non-0, non-1 color before MiddleZeroBlock)
    idx_before_middle = start_idx_middle_zero - 1
    start_idx_color = start_idx_middle_zero # Default if no color block found
    color_block = [] # Default empty block

    if idx_before_middle >= 0:
        color = row[idx_before_middle]
        # Check if it's a valid color for the color block (not 0 or 1)
        if color != 0 and color != 1:
            i = idx_before_middle
            # Find the start of the contiguous block of this color
            while i >= 0 and row[i] == color:
                i -= 1
            start_idx_color = i + 1
            # Slice the color block
            color_block = row[start_idx_color : idx_before_middle + 1]
        # else: color is 0 or 1, meaning no valid ColorBlock immediately precedes MiddleZeroBlock

    # 4. Identify the InitialPart (everything before the ColorBlock)
    initial_part = row[0 : start_idx_color]

    # 5. Construct the output grid by concatenating the parts in the new order
    output_row = initial_part + middle_zero_block + color_block + end_sequence

    # Return the result in the standard ARC format (list of lists)
    return [output_row]

```
```python
import numpy as np
from typing import List

"""
Transforms a 1xN input grid by rearranging identified segments based on their content and position.

The input grid is expected to be a single row with the structure:
[InitialPart][ColorBlock][MiddleZeroBlock][EndSequence]

1.  **EndSequence**: Always [1, 0] (Blue, White) at the very end.
2.  **MiddleZeroBlock**: A contiguous block of 0s (White) immediately preceding the EndSequence.
3.  **ColorBlock**: A contiguous block of a single color C (where C is not 0 or 1) immediately preceding the MiddleZeroBlock.
4.  **InitialPart**: All elements before the ColorBlock (can be empty or only contain 0s).

The transformation swaps the positions of the ColorBlock and the MiddleZeroBlock, resulting in the output structure:
[InitialPart][MiddleZeroBlock][ColorBlock][EndSequence]
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the segment rearrangement transformation to the input grid.

    Args:
        input_grid: A list containing a single list of integers (1xN grid).

    Returns:
        A list containing a single list of integers representing the transformed grid.
        Returns the original input grid if the expected structure is not found.
    """
    # Ensure input is in the expected List[List[int]] format and contains one row.
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Return original grid if format is unexpected. Consider raising an error in a stricter context.
        return input_grid
        
    row = input_grid[0]
    n = len(row)

    # Check minimum length for the structure (at least EndSequence + 1 element)
    if n < 3:
        return input_grid # Not long enough for the pattern

    # --- 1. Identify the fixed EndSequence [1, 0] ---
    end_sequence = [1, 0]
    if row[n-2:] != end_sequence:
        # If the end sequence is not [1, 0], the pattern doesn't match.
        return input_grid

    idx_before_end = n - 3 # Index of the last element before the end sequence

    # --- 2. Identify the MiddleZeroBlock (contiguous 0s before EndSequence) ---
    end_idx_middle_zero = idx_before_end
    start_idx_middle_zero = -1 
    
    # Find the start index by moving left while encountering 0s
    i = end_idx_middle_zero
    while i >= 0 and row[i] == 0:
        start_idx_middle_zero = i
        i -= 1
        
    # Check if any zeros were found
    if start_idx_middle_zero == -1:
         # No MiddleZeroBlock found where expected
         # Although examples suggest it's always present, handle case defensively
         middle_zero_block = [] 
         # The element before where the block *should* start is i 
         # (which is still end_idx_middle_zero if the loop didn't run)
         idx_before_middle = i 
    else:
        middle_zero_block = row[start_idx_middle_zero : end_idx_middle_zero + 1]
        # Index before the start of the found block
        idx_before_middle = start_idx_middle_zero - 1

    # --- 3. Identify the ColorBlock (contiguous non-0, non-1 color before MiddleZeroBlock) ---
    start_idx_color = -1
    color_block = []

    # Check if there are elements before the MiddleZeroBlock
    if idx_before_middle >= 0:
        color = row[idx_before_middle]
        # Check if it's a valid color for the ColorBlock (not 0 or 1)
        if color != 0 and color != 1:
            end_idx_color = idx_before_middle
            # Find the start of the contiguous block of this color
            i = end_idx_color
            while i >= 0 and row[i] == color:
                start_idx_color = i
                i -= 1
            
            # Check if block was actually identified (start_idx_color should be set)
            if start_idx_color != -1:
                 color_block = row[start_idx_color : end_idx_color + 1]
            # else: no color block found (e.g., if row[idx_before_middle] was 0 or 1)
            
        # else: the element before MiddleZeroBlock is 0 or 1, so no valid ColorBlock directly precedes it.
        
    # --- 4. Identify the InitialPart (everything before the ColorBlock) ---
    # If ColorBlock was found, InitialPart is everything before it.
    # If ColorBlock was *not* found, determine where the InitialPart should logically end.
    # If no ColorBlock identified, InitialPart ends where ColorBlock *would* have started.
    # This is index `idx_before_middle + 1`.
    
    if start_idx_color != -1: # ColorBlock was found
        initial_part = row[0 : start_idx_color]
    else: # No valid ColorBlock found
        # The initial part goes up to the element before MiddleZeroBlock (inclusive)
        # or up to index -1 if MiddleZeroBlock starts at index 0.
        end_idx_initial = idx_before_middle 
        if end_idx_initial < 0:
            initial_part = []
        else:
            initial_part = row[0 : end_idx_initial + 1]
        # Since no ColorBlock was found, color_block remains []

    # --- 5. Construct the output grid by concatenating the parts ---
    # Handle the case where ColorBlock wasn't found correctly - it's empty
    output_row = initial_part + middle_zero_block + color_block + end_sequence

    # Check if the constructed row length matches the original length
    # This acts as a sanity check for the parsing logic
    if len(output_row) != n:
        # If lengths don't match, something went wrong in parsing. Return original.
        print(f"Warning: Output length mismatch. Input: {n}, Output: {len(output_row)}. Returning original.")
        return input_grid

    # Return the result in the standard ARC format (list of lists)
    return [output_row]
```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1xN input grid by rearranging identified segments based on their content and position.

The input grid is expected to be a single row with the structure:
[InitialPart][ColorBlock][MiddleZeroBlock][EndSequence]

1.  **EndSequence**: Always [1, 0] (Blue, White) at the very end.
2.  **MiddleZeroBlock**: A contiguous block of 0s (White) immediately preceding the EndSequence. Can be empty.
3.  **ColorBlock**: A contiguous block of a single color C (where C is not 0 or 1) immediately preceding the MiddleZeroBlock. Can be empty if the preceding element is 0, 1, or the start of the grid.
4.  **InitialPart**: All elements before the ColorBlock (or before MiddleZeroBlock if ColorBlock is absent). Can be empty.

The transformation swaps the positions of the ColorBlock and the MiddleZeroBlock, resulting in the output structure:
[InitialPart][MiddleZeroBlock][ColorBlock][EndSequence]
"""

def find_contiguous_block_before(row: List[int], end_index_exclusive: int, condition_func) -> Tuple[List[int], int]:
    """
    Finds a contiguous block of elements satisfying a condition, ending just before a given index.

    Scans backwards from `end_index_exclusive - 1`.

    Args:
        row: The list of integers representing the grid row.
        end_index_exclusive: The index *after* the last element of the potential block.
        condition_func: A function that takes a color value and returns True if it belongs to the block.

    Returns:
        A tuple containing:
        - The found block (list of integers). Empty if no block found.
        - The start index of the found block. -1 if no block found.
    """
    start_idx = -1
    block = []
    # Start checking from the element *before* the end_index_exclusive
    i = end_index_exclusive - 1 
    
    # Find the end of the block (first element matching condition)
    if i >= 0 and condition_func(row[i]):
        end_idx_inclusive = i
        # Scan backwards to find the start of the block
        while i >= 0 and condition_func(row[i]):
            start_idx = i
            i -= 1
        # Extract the block
        if start_idx != -1:
            block = row[start_idx : end_idx_inclusive + 1]
            
    return block, start_idx

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the segment rearrangement transformation to the input grid.

    Args:
        input_grid: A list containing a single list of integers (1xN grid).

    Returns:
        A list containing a single list of integers representing the transformed grid.
        Returns the original input grid if the expected structure is not found or parsing fails.
    """
    # --- 1. Input Validation ---
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Invalid format
        return input_grid
        
    row = input_grid[0]
    n = len(row)

    # --- 2. Identify End Sequence ---
    if n < 2 or row[n-2:] != [1, 0]:
        # Required EndSequence not found or grid too short
        return input_grid
    end_sequence = [1, 0]
    index_before_end = n - 2 # Index where the MiddleZeroBlock ends (exclusive)

    # --- 3. Identify Middle Zero Block ---
    # Find contiguous block of 0s ending just before index_before_end
    middle_zero_block, start_idx_middle_zero = find_contiguous_block_before(
        row, 
        index_before_end, 
        lambda color: color == 0
    )
    # Determine the index before this block starts
    if start_idx_middle_zero != -1:
        index_before_middle = start_idx_middle_zero
    else:
        # No zero block found, the potential color block ends just before the end sequence
        index_before_middle = index_before_end 

    # --- 4. Identify Color Block ---
    color_block = []
    start_idx_color = -1
    # Check if there's an element before the middle block (or before EndSequence if middle was empty)
    if index_before_middle > 0: # index_before_middle is exclusive, so check index-1
         potential_color = row[index_before_middle - 1]
         # Check if it's a valid color for the ColorBlock
         if potential_color != 0 and potential_color != 1:
             # Define the condition for this specific color
             color_condition = lambda c, target_color=potential_color: c == target_color
             # Find the contiguous block of this color
             color_block, start_idx_color = find_contiguous_block_before(
                 row,
                 index_before_middle, # Block ends before the MiddleZeroBlock starts
                 color_condition
             )
             # Note: start_idx_color will be -1 if the element at index_before_middle-1
             # satisfies the color criteria but is not part of a contiguous block extending left.
             # The find function handles finding the *actual* start. If it's just one element, start_idx == end_idx.


    # --- 5. Identify Initial Part ---
    # Determine the end index (exclusive) of the initial part
    if start_idx_color != -1:
        # Color block was found, initial part ends before it
        end_idx_initial_exclusive = start_idx_color
    else:
        # No color block found, initial part ends before the middle zero block (or where it would start)
        end_idx_initial_exclusive = index_before_middle # This is the index *after* the last element of InitialPart
        
    initial_part = row[0 : end_idx_initial_exclusive]

    # --- 6. Construct Output ---
    output_row = initial_part + middle_zero_block + color_block + end_sequence

    # --- 7. Final Validation ---
    if len(output_row) != n:
        # If lengths don't match, parsing likely failed. Return original.
        # This can happen if the helper function logic has a bug or edge case miss.
        print(f"Warning: Output length ({len(output_row)}) mismatch with input ({n}). Returning original.")
        return input_grid
        
    # --- 8. Return Output ---
    return [output_row]
```
