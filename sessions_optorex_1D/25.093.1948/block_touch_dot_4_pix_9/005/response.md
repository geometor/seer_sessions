```python
import copy # For creating a mutable copy of the input list

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
    Finds the index of the first occurrence (left-to-right) of the pattern X, 0, 2.
    X must not be 0 or 2.
    Returns the index 'i' of X if found, otherwise returns -1.
    """
    n = len(grid)
    # Iterate up to n-3 because the pattern is 3 elements long (indices i, i+1, i+2)
    for i in range(n - 2):
        x = grid[i]
        zero = grid[i+1]
        two = grid[i+2]
        # Check if the pattern conditions are met
        if x != 0 and x != 2 and zero == 0 and two == 2:
            return i  # Return the index of X (start of the pattern)
    return -1 # Pattern not found

def find_pattern2_shift(grid):
    """
    Finds the details of the first occurrence (left-to-right) of the pattern 2, 0..., 0, Y.
    - '2' is the literal number 2.
    - '0..., 0' is one or more zeros (Zero_Block).
    - 'Y' is a non-empty contiguous block of numbers != 0 and != 2 (Movable_Block).
    
    Returns a tuple: (idx_2, num_zeros, block_y, idx_block_end) 
    if the pattern is found, otherwise returns None.
    
    - idx_2: index of the '2'
    - num_zeros: count of zeros in the Zero_Block
    - block_y: list containing the elements of the Movable_Block Y
    - idx_block_end: ending index (exclusive) of the original Movable_Block Y
    """
    n = len(grid)
    for i in range(n):
        # Find the first '2'
        if grid[i] == 2:
            idx_2 = i
            
            # --- Find the contiguous block of zeros following the '2' ---
            idx_after_2 = idx_2 + 1
            if idx_after_2 >= n: # Check if '2' is the last element
                continue # Cannot have zeros or block Y after it

            num_zeros = 0
            idx_first_non_zero = -1
            for j in range(idx_after_2, n):
                if grid[j] == 0:
                    num_zeros += 1
                else:
                    idx_first_non_zero = j
                    break
            
            # Check if at least one zero was found
            if num_zeros == 0:
                continue # Pattern requires at least one zero after '2'
            
            # --- Find the contiguous block Y (non-zero, non-2) following the zeros ---
            if idx_first_non_zero == -1: # No non-zero element found after zeros
                continue 

            block_y = []
            idx_block_end = idx_first_non_zero # Start of block Y determines initial end
            for k in range(idx_first_non_zero, n):
                val = grid[k]
                # Check if element belongs to a valid Movable_Block
                if val != 0 and val != 2:
                    block_y.append(val)
                    idx_block_end = k + 1 # Update end index (exclusive)
                else:
                    # Block Y ends if 0 or 2 is encountered
                    break 
                    
            # Check if a valid, non-empty block Y was found
            if len(block_y) > 0:
                # Found the complete pattern 2, return its details
                # Note: idx_block_start is idx_first_non_zero
                return (idx_2, num_zeros, block_y, idx_block_end)
                
            # If we reach here, this '2' did not start a valid Pattern 2.
            # Continue the outer loop to check for the next '2'.

    # If the loop completes without finding the pattern
    return None


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rules to the input grid (list of integers).
    """
    # Create a deep copy to avoid modifying the original input list
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid) # Should always be 12 based on examples

    # --- Rule 1: Check for Pattern 1 (X, 0, 2 swap) ---
    # Scan for the first occurrence of the pattern.
    swap_index = find_pattern1_swap(output_grid)
    
    # If Pattern 1 is found, perform the swap and return immediately.
    if swap_index != -1:
        # Perform the swap of X (at swap_index) and 0 (at swap_index + 1)
        output_grid[swap_index], output_grid[swap_index + 1] = output_grid[swap_index + 1], output_grid[swap_index]
        return output_grid # Transformation complete

    # --- Rule 2: Check for Pattern 2 (2, 0s, Y shift) ---
    # This section executes only if Pattern 1 was NOT found.
    # Scan for the first occurrence of the pattern.
    shift_details = find_pattern2_shift(output_grid)
    
    # If Pattern 2 is found, perform the shift and return.
    if shift_details is not None:
        # Unpack the details found by the helper function
        idx_2, num_zeros, block_y, idx_block_end = shift_details
        
        # Reconstruct the list segments for the shift operation
        prefix = output_grid[:idx_2 + 1]          # Elements up to and including the '2'
        moved_block_y = block_y                   # The Movable_Block Y itself
        moved_zeros = [0] * num_zeros             # The Zero_Block that was between '2' and 'Y'
        suffix = output_grid[idx_block_end:]      # Elements originally after the Movable_Block Y
        
        # Combine the segments to form the new grid arrangement
        new_grid_list = prefix + moved_block_y + moved_zeros + suffix
        
        # Defensive check: Ensure the list length remains correct (12). 
        # Pad with 0s or truncate if necessary, although reconstruction should preserve length.
        if len(new_grid_list) < n:
            new_grid_list.extend([0] * (n - len(new_grid_list)))
        elif len(new_grid_list) > n:
            new_grid_list = new_grid_list[:n]
            
        # Update the output grid with the rearranged list
        output_grid = new_grid_list
        return output_grid # Transformation complete

    # --- No Change ---
    # If neither Pattern 1 nor Pattern 2 was found and executed, 
    # return the unmodified (copied) input grid.
    return output_grid
```