```python
import numpy as np

"""
Shift a single contiguous block of non-zero, non-2 digits within a 1D sequence 
to be immediately adjacent to the unique digit '2', preserving the block's 
internal order and the '2's position. If the block is already adjacent, or if 
no such block exists, or if '2' is not present, the sequence remains unchanged. 
Assumes at most one such block and at most one '2' exists per sequence.
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
        A dictionary containing 'digits' (np.array), 'start' (int), 'end' (int), 
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
            "digits": block_digits, # Return as numpy array
            "start": start_index,
            "end": end_index,
            "len": len(block_digits)
        }
    else:
        # Found non-zero/non-2 elements, but they don't form a single contiguous block.
        return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Get the size of the input grid
    n = input_grid.shape[0]

    # Locate the index of the unique digit '2' (the separator).
    separator_index = find_separator_index(input_grid)

    # If '2' is not found, return the original sequence.
    if separator_index == -1:
        return input_grid.copy() 

    # Search the sequence for a single, contiguous block of digits that are neither '0' nor '2'.
    block_info = find_number_block(input_grid)

    # If no such block is found, return the original sequence.
    if block_info is None:
        return input_grid.copy()

    # Determine block properties
    block_start = block_info["start"]
    block_end = block_info["end"]
    block_digits = block_info["digits"]
    block_length = block_info["len"]
    
    # Check if the block is already adjacent to the separator
    is_adjacent_left = (block_end == separator_index - 1)
    is_adjacent_right = (block_start == separator_index + 1)

    # If the block *is* already adjacent, return the original sequence.
    if is_adjacent_left or is_adjacent_right:
        return input_grid.copy()

    # If the block exists and is *not* adjacent, perform the shift.
    
    # Create a new output sequence of the same length as the input, filled with '0's.
    output_grid = np.zeros_like(input_grid)

    # Place the digit '2' into the output sequence at its original separator_index.
    output_grid[separator_index] = 2

    # Determine if the block was to the left or right of the separator.
    if block_start < separator_index:
        # Block was to the left, calculate target position so block ends at separator_index - 1.
        target_end_index = separator_index - 1
        target_start_index = target_end_index - block_length + 1
    else: # block_start > separator_index 
        # Block was to the right, calculate target position so block starts at separator_index + 1.
        target_start_index = separator_index + 1
        target_end_index = target_start_index + block_length - 1

    # Copy the block digits into the output sequence at the calculated target position.
    # Basic boundary check included for robustness, although not expected based on examples.
    if 0 <= target_start_index <= target_end_index < n: 
         output_grid[target_start_index : target_end_index + 1] = block_digits
    else:
         # In case of unexpected calculation error, fallback to returning input to avoid crash
         print(f"Warning: Calculated target indices [{target_start_index}, {target_end_index}] out of bounds for grid size {n}. Returning original grid.")
         return input_grid.copy() 

    # Return the newly constructed output sequence.
    return output_grid
```