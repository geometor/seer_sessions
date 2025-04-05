
Previous Code:
```python
import math # Not strictly required for this logic, but good practice
import copy # To ensure the input list isn't modified directly

"""
Transforms an input list of 12 integers based on two prioritized local patterns involving the numbers 0 and 2.

1.  **Pattern 1 (Swap - Highest Priority):** Searches for the first occurrence (left-to-right) 
    of a sub-sequence `X, 0, 2`, where `X` is any integer other than 0 or 2. 
    If found, it swaps `X` and `0` to `0, X, 2` and the transformation is complete.

2.  **Pattern 2 (Shift - Lower Priority):** If Pattern 1 is not found, searches for the 
    first occurrence (left-to-right) of a sub-sequence starting with `2`, followed by 
    one or more `0`s, followed immediately by a non-empty contiguous block `Y` of integers 
    that are neither `0` nor `2`. If found, it moves block `Y` to be immediately after 
    the initial `2`, followed by the block of `0`s that were originally between the `2` 
    and `Y`. The transformation is then complete.

3.  **No Change:** If neither pattern is found, the original input list is returned unchanged.
"""

# --- Helper Functions ---

def find_pattern1_swap(grid):
    """
    Finds the index of the first occurrence of the pattern X, 0, 2.
    X must not be 0 or 2.
    Returns the index 'i' of X if found, otherwise returns -1.
    """
    n = len(grid)
    for i in range(n - 2):
        x = grid[i]
        zero = grid[i+1]
        two = grid[i+2]
        if x != 0 and x != 2 and zero == 0 and two == 2:
            return i  # Return the index of X
    return -1

def find_pattern2_shift(grid):
    """
    Finds the details of the first occurrence of the pattern 2, 0..., 0, Y.
    - '2' is the literal number 2.
    - '0..., 0' is one or more zeros.
    - 'Y' is a non-empty contiguous block of numbers != 0 and != 2.
    
    Returns a tuple: (idx_2, num_zeros, block_y, idx_block_start, idx_block_end) 
    if the pattern is found, otherwise returns None.
    
    - idx_2: index of the '2'
    - num_zeros: count of zeros between '2' and 'Y'
    - block_y: list containing the elements of block Y
    - idx_block_start: starting index of the original block Y
    - idx_block_end: ending index (exclusive) of the original block Y
    """
    n = len(grid)
    for i in range(n):
        # Find the first '2'
        if grid[i] == 2:
            idx_2 = i
            
            # Check if there are elements after '2'
            if idx_2 + 1 < n:
                # Find the block of zeros
                idx_first_zero = idx_2 + 1
                num_zeros = 0
                idx_first_non_zero_after_zeros = -1
                for j in range(idx_first_zero, n):
                    if grid[j] == 0:
                        num_zeros += 1
                    else:
                        idx_first_non_zero_after_zeros = j
                        break
                
                # Check if at least one zero was found and there's something after zeros
                if num_zeros > 0 and idx_first_non_zero_after_zeros != -1:
                    # Find the block Y (non-zero, non-2 elements)
                    idx_block_start = idx_first_non_zero_after_zeros
                    idx_block_end = idx_block_start
                    block_y = []
                    contains_invalid_in_block = False # Checks for 0 or 2 within Y
                    
                    for k in range(idx_block_start, n):
                        val = grid[k]
                        if val != 0 and val != 2:
                            block_y.append(val)
                            idx_block_end = k + 1
                        else:
                            # Block Y ends if 0 or 2 is encountered.
                            # Note: The description implies Y *only* contains valid numbers,
                            # so encountering 0 or 2 means the block ends *before* it.
                            break 
                            
                    # Check if a valid, non-empty block Y was found
                    if len(block_y) > 0:
                        # Found the complete pattern 2, return its details
                        return (idx_2, num_zeros, block_y, idx_block_start, idx_block_end)
                        
            # If we found a '2' but the rest of the pattern didn't match, 
            # continue searching for the next '2' that might start a valid pattern.
            # However, the rule is to act on the *first* valid pattern occurrence.
            # So if we found a valid pattern above, we returned. If we are here, 
            # it means this '2' didn't lead to a valid pattern 2. We need to break
            # the outer loop only AFTER finding the first complete pattern.
            # The 'return' inside the successful pattern check handles this.

    # If the loop completes without finding the pattern
    return None


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rules to the input grid (list of integers).
    """
    # Initialize output_grid as a deep copy to avoid modifying the original input list
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid)

    # --- Rule 1: Check for Pattern 1 (X, 0, 2 swap) ---
    swap_index = find_pattern1_swap(output_grid)
    if swap_index != -1:
        # Perform the swap
        output_grid[swap_index], output_grid[swap_index + 1] = output_grid[swap_index + 1], output_grid[swap_index]
        # Return immediately after the first swap
        return output_grid

    # --- Rule 2: Check for Pattern 2 (2, 0s, Y shift) ---
    # This runs only if Rule 1 did not apply
    shift_details = find_pattern2_shift(output_grid)
    if shift_details is not None:
        idx_2, num_zeros, block_y, idx_block_start, idx_block_end = shift_details
        
        # Perform the shift by reconstructing the list
        prefix = output_grid[:idx_2 + 1]          # Elements up to and including '2'
        moved_part = block_y                      # The block Y
        zeros_part = [0] * num_zeros              # The zeros that were between 2 and Y
        suffix = output_grid[idx_block_end:]      # Elements after the original block Y
        
        # Combine parts
        new_grid_list = prefix + moved_part + zeros_part + suffix
        
        # Ensure the list remains the correct length (it should, but defensively check/pad/truncate)
        if len(new_grid_list) < n:
            new_grid_list.extend([0] * (n - len(new_grid_list)))
        elif len(new_grid_list) > n:
            new_grid_list = new_grid_list[:n]
            
        # Return the result of the shift
        return new_grid_list

    # --- No Change ---
    # If neither pattern was found and applied, return the original grid copy
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
