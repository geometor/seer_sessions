```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Convert the input NumPy array (assumed 1D) into a Python list of integers.
2. Scan the list from right to left to find the rightmost occurrence where a contiguous block of identical digits `d` (where `d` is not 0 and not 2), called the `value_block` (B), is immediately adjacent to a contiguous block of zeros, called the `zero_block` (Z). The adjacency can be `BZ` (value block followed by zero block) or `ZB` (zero block followed by value block).
3. If such a pair is found:
    a. Determine the full start and end indices of the `value_block` (B).
    b. Determine the full start and end indices of the adjacent `zero_block` (Z).
    c. Calculate the length of the segment of the `zero_block` that will be swapped: `swap_len = min(length of Z, 3)`.
    d. Identify the indices of this zero segment:
        - If the pattern is `BZ`, the segment comprises the first `swap_len` zeros of Z.
        - If the pattern is `ZB`, the segment comprises the last `swap_len` zeros of Z.
    e. Construct the output list by swapping the entire `value_block` (B) with the identified `swap_len` segment of the `zero_block` (Z). The remaining part of the `zero_block` (if any) stays in place relative to the swapped segment.
4. If no such adjacent pair is found, the output list is identical to the input list.
5. Convert the resulting list back into the format expected (likely a NumPy array mirroring the input format).
"""

def _find_block_indices(data: List[int], index: int) -> Tuple[int, int]:
    """Finds the start and end indices of the contiguous block containing the element at `index`."""
    val = data[index]
    start = index
    end = index
    n = len(data)
    # Find start
    while start > 0 and data[start - 1] == val:
        start -= 1
    # Find end
    while end < n - 1 and data[end + 1] == val:
        end += 1
    return start, end

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: swaps the rightmost adjacent pair of a 
    (non-zero, non-2) value block and a zero block segment (max length 3).
    """
    # Convert input numpy array (assumed 1D) to list
    if input_grid.ndim > 1:
         # Assuming the task works on 1D sequences based on examples
         # If it's a grid, flatten or handle appropriately.
         # For now, assume it's meant to be 1D or take the first row.
         input_list = input_grid.flatten().tolist()
         # Or if only one row: input_list = input_grid[0].tolist()
    else:
         input_list = input_grid.tolist()

    n = len(input_list)
    if n < 2:
        return input_grid # Cannot have adjacent blocks

    rightmost_swap_details = None

    # Iterate backwards through potential boundaries between elements
    # i is the index *before* the boundary (left element)
    for i in range(n - 2, -1, -1):
        left_val = input_list[i]
        right_val = input_list[i+1]

        # Potential BZ pattern: value_block | zero_block
        if left_val != 0 and left_val != 2 and right_val == 0:
            # Found a potential BZ boundary at i | i+1
            b_start, b_end = _find_block_indices(input_list, i)
            z_start, z_end = _find_block_indices(input_list, i + 1)

            # Check if the identified blocks are actually adjacent
            if b_end == i and z_start == i + 1:
                # Store details and break (found rightmost)
                rightmost_swap_details = {
                    'type': 'BZ',
                    'b_start': b_start, 'b_end': b_end,
                    'z_start': z_start, 'z_end': z_end
                }
                break

        # Potential ZB pattern: zero_block | value_block
        elif left_val == 0 and right_val != 0 and right_val != 2:
            # Found a potential ZB boundary at i | i+1
            z_start, z_end = _find_block_indices(input_list, i)
            b_start, b_end = _find_block_indices(input_list, i + 1)

            # Check if the identified blocks are actually adjacent
            if z_end == i and b_start == i + 1:
                 # Store details and break (found rightmost)
                rightmost_swap_details = {
                    'type': 'ZB',
                    'z_start': z_start, 'z_end': z_end,
                    'b_start': b_start, 'b_end': b_end
                }
                break

    # If no suitable adjacent pair was found, return the original grid
    if rightmost_swap_details is None:
        return input_grid

    # --- Perform the swap ---
    output_list = []
    details = rightmost_swap_details

    if details['type'] == 'BZ':
        # Structure: Prefix | B | Z | Suffix
        b_block = input_list[details['b_start'] : details['b_end'] + 1]
        z_block = input_list[details['z_start'] : details['z_end'] + 1]
        z_len = len(z_block)
        swap_len = min(z_len, 3)

        prefix = input_list[0 : details['b_start']]
        z_segment_to_swap = z_block[0 : swap_len]
        z_remainder = z_block[swap_len : ] # May be empty
        suffix = input_list[details['z_end'] + 1 : n]

        # New structure: Prefix | Z_segment | B | Z_remainder | Suffix
        output_list = prefix + z_segment_to_swap + b_block + z_remainder + suffix

    elif details['type'] == 'ZB':
        # Structure: Prefix | Z | B | Suffix
        z_block = input_list[details['z_start'] : details['z_end'] + 1]
        b_block = input_list[details['b_start'] : details['b_end'] + 1]
        z_len = len(z_block)
        swap_len = min(z_len, 3)

        prefix = input_list[0 : details['z_start']]
        z_remainder = z_block[0 : z_len - swap_len] # May be empty
        z_segment_to_swap = z_block[z_len - swap_len : ]
        suffix = input_list[details['b_end'] + 1 : n]

        # New structure: Prefix | Z_remainder | B | Z_segment | Suffix
        output_list = prefix + z_remainder + b_block + z_segment_to_swap + suffix

    # Ensure output has the same shape as input
    output_array = np.array(output_list, dtype=input_grid.dtype)
    # If input was multi-dimensional, reshape might be needed
    # output_array = output_array.reshape(input_grid.shape)

    return output_array
```