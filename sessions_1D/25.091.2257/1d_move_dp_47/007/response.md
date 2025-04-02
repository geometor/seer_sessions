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

def _find_contiguous_block_before(row: List[int], end_index_exclusive: int, condition_func) -> Tuple[List[int], int]:
    """
    Finds a contiguous block of elements satisfying a condition, ending just before a given index.

    Scans backwards from `end_index_exclusive - 1`.

    Args:
        row: The list of integers representing the grid row.
        end_index_exclusive: The index *after* the last potential element of the block.
                               The scan starts at `end_index_exclusive - 1`.
        condition_func: A function that takes a color value and returns True if it belongs to the block.

    Returns:
        A tuple containing:
        - The found block (list of integers). Empty if no block found meeting condition.
        - The start index of the found block (inclusive). -1 if no block found.
    """
    start_idx = -1
    block = []
    
    # Index of the last potential element in the block
    current_idx = end_index_exclusive - 1 
    
    # Check if the element immediately before the exclusive end index meets the condition
    if current_idx >= 0 and condition_func(row[current_idx]):
        end_idx_inclusive = current_idx # Mark the end of the block
        
        # Scan backwards from this element to find the start of the contiguous block
        while current_idx >= 0 and condition_func(row[current_idx]):
            start_idx = current_idx  # Update start index as we move left
            current_idx -= 1         # Move to the previous element
            
        # Extract the block using the determined start and end indices
        if start_idx != -1: # Should always be true if we entered the outer if block
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
    # Check if input is a list containing exactly one list (the row)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Invalid format, return original
        return input_grid
        
    row = input_grid[0]
    n = len(row)

    # --- 2. Identify End Sequence ---
    # Check for minimum length (need at least [1, 0]) and the sequence itself
    if n < 2 or row[n-2:] != [1, 0]:
        # Required EndSequence [1, 0] not found or grid too short, return original
        return input_grid
    end_sequence = [1, 0]
    # The index *before* the EndSequence starts. Segments end here.
    index_before_end = n - 2 

    # --- 3. Identify Middle Zero Block ---
    # Find contiguous block of 0s ending just before index_before_end
    middle_zero_block, start_idx_middle_zero = _find_contiguous_block_before(
        row, 
        index_before_end, # Search ends before this index
        lambda color: color == 0 # Condition: element must be 0 (white)
    )
    
    # Determine the index *before* the MiddleZeroBlock starts.
    # This marks the exclusive end index for the ColorBlock search.
    if start_idx_middle_zero != -1:
        # A block of zeros was found, ColorBlock search ends before its start index
        index_before_middle = start_idx_middle_zero 
    else:
        # No zero block found, ColorBlock search ends just before the EndSequence
        index_before_middle = index_before_end 

    # --- 4. Identify Color Block ---
    color_block = []
    start_idx_color = -1 # Initialize start index for color block
    
    # Check if there is an element before the MiddleZeroBlock (or before EndSequence if middle block was empty)
    # index_before_middle is the exclusive end for ColorBlock, so check element at index_before_middle - 1
    potential_color_idx = index_before_middle - 1
    if potential_color_idx >= 0:
         # Get the color of the element potentially starting the ColorBlock
         potential_color = row[potential_color_idx]
         # Check if it's a valid color for the ColorBlock (not 0/White or 1/Blue)
         if potential_color != 0 and potential_color != 1:
             # Define the condition function for this specific color
             # Need to capture potential_color in the lambda's default argument
             color_condition = lambda c, target_color=potential_color: c == target_color
             
             # Find the contiguous block of this color ending before index_before_middle
             color_block, start_idx_color = _find_contiguous_block_before(
                 row,
                 index_before_middle, # Search ends before the MiddleZeroBlock starts
                 color_condition      # Condition: element must match potential_color
             )
             # start_idx_color will be the actual start index of the found block, or -1 if none found

    # --- 5. Identify Initial Part ---
    # Determine the end index (exclusive) of the InitialPart based on where the ColorBlock starts.
    if start_idx_color != -1:
        # Color block was found, InitialPart includes everything before it.
        end_idx_initial_exclusive = start_idx_color
    else:
        # No ColorBlock found. InitialPart includes everything before the MiddleZeroBlock
        # (or before the EndSequence if MiddleZeroBlock was also empty).
        end_idx_initial_exclusive = index_before_middle 
        
    # Extract the InitialPart using slicing. Handles empty case correctly (slice [0:0] is [])
    initial_part = row[0 : end_idx_initial_exclusive]

    # --- 6. Construct Output ---
    # Concatenate the identified parts in the desired new order.
    # If a block wasn't found, its corresponding list (e.g., color_block) will be empty.
    output_row = initial_part + middle_zero_block + color_block + end_sequence

    # --- 7. Final Validation ---
    # Check if the constructed row has the same length as the input row.
    # This is a sanity check; if lengths differ, the parsing logic might have errors.
    if len(output_row) != n:
        # Parsing likely failed, return original to avoid incorrect output.
        # Consider adding logging or raising an error in a production scenario.
        # print(f"Warning: Output length ({len(output_row)}) mismatch with input ({n}). Returning original.")
        return input_grid
        
    # --- 8. Return Output ---
    # Wrap the transformed row in a list to match the ARC grid format List[List[int]]
    return [output_row]
```