import math # Not used in this specific logic, but common practice

def parse_input(input_str):
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(grid):
    """Formats the list of integers back into a space-separated string."""
    return ' '.join(map(str, grid))

def transform(input_str):
    """
    Transforms the input sequence based on two primary patterns involving 0 and 2:
    1. If a pattern `X, 0, 2` (where X is non-zero and not 2) is found,
       swap X and 0 to `0, X, 2` and return. This action happens only for the
       first occurrence found scanning left-to-right.
    2. If Pattern 1 is not found, search for the first pattern `2, 0..., 0, Y`
       (where there's at least one 0, and Y is a non-empty block of non-zero,
       non-2 digits immediately following the zeros). Move block Y immediately
       after the 2, followed by the zeros that were originally between 2 and Y.
       Return the result. This action happens only for the first valid occurrence found.
    3. If neither pattern is found, return the original sequence.
    """
    grid = parse_input(input_str)
    n = len(grid)
    # Initialize output_grid as a copy of the input
    output_grid = list(grid) 

    # --- Check for Pattern 1: X, 0, 2 ---
    pattern1_found = False
    # Iterate up to n-3 because we need to check i, i+1, and i+2
    for i in range(n - 2):
        x = output_grid[i]
        zero = output_grid[i+1]
        two = output_grid[i+2]
        
        # Condition: X is non-zero and not 2, followed by 0, followed by 2
        if x != 0 and x != 2 and zero == 0 and two == 2:
            # Perform the swap: X and 0
            output_grid[i], output_grid[i+1] = output_grid[i+1], output_grid[i]
            pattern1_found = True
            # Stop processing after the first pattern match
            break 
            
    # If Pattern 1 was found and applied, return the result immediately
    if pattern1_found:
        return format_output(output_grid)

    # --- Check for Pattern 2: 2, 0..., 0, Y ---
    # This section only runs if Pattern 1 was NOT found
    pattern2_found = False
    # Iterate through the grid to find the first '2' that initiates the pattern
    for i in range(n):
        # Is the current element 2?
        if output_grid[i] == 2:
            idx_2 = i
            
            # Check if there are elements after the '2' to form the rest of the pattern
            if idx_2 + 1 < n:
                
                # --- Find the block of zeros immediately following the '2' ---
                idx_first_zero = idx_2 + 1
                idx_first_non_zero_after_zeros = -1
                num_zeros = 0
                # Scan from after '2' to find contiguous zeros
                for j in range(idx_first_zero, n):
                    if output_grid[j] == 0:
                        num_zeros += 1
                    else:
                        # Found the first non-zero element after the zero block
                        idx_first_non_zero_after_zeros = j
                        break
                
                # --- Check if the zero block is valid (at least one zero) ---
                # Also need a non-zero element following the zeros to form block Y
                if num_zeros > 0 and idx_first_non_zero_after_zeros != -1:
                    
                    # --- Find the block Y (non-zero, non-2 elements) ---
                    idx_block_start = idx_first_non_zero_after_zeros
                    idx_block_end = idx_block_start # Initialize end index (exclusive)
                    block_y = []
                    contains_2_in_block = False
                    
                    # Scan from the start of the potential block Y
                    for k in range(idx_block_start, n):
                        val = output_grid[k]
                        # Block continues if element is non-zero and not 2
                        if val != 0 and val != 2:
                            block_y.append(val)
                            idx_block_end = k + 1 # Update end index
                        else:
                            # Block ends if 0 or 2 is encountered
                            if val == 2:
                                # Mark if the block is invalid because it contains a 2
                                contains_2_in_block = True 
                            break # Stop scanning for this block

                    # --- Check if a valid block Y was found ---
                    # Block Y must be non-empty and must not contain any 2s
                    if len(block_y) > 0 and not contains_2_in_block:
                        len_y = len(block_y)
                        
                        # --- Perform the transformation ---
                        # Construct the new sequence segments
                        prefix = output_grid[:idx_2 + 1]          # Elements up to and including '2'
                        moved_part = block_y + ([0] * num_zeros) # The moved block Y followed by the zeros
                        suffix = output_grid[idx_block_end:]      # Elements after the original block Y
                        
                        # Combine segments to form the new grid
                        new_grid_list = prefix + moved_part + suffix
                        
                        # Basic sanity check for length preservation
                        if len(new_grid_list) == n:
                           output_grid = new_grid_list # Update the grid with the transformation
                           pattern2_found = True
                           # Stop searching for patterns after the first successful transformation
                           break 
                        # else: # If length changed, there's a logic error (should not happen here)
                           # print("Error: Length mismatch during Pattern 2 transformation") 
                           # pass

            # If Pattern 2 was successfully applied for this '2', stop the outer loop
            if pattern2_found:
                 break

    # Return the final state of the grid, formatted as a string
    # This will be the result of Pattern 2 if applied, or the original grid if no patterns matched
    return format_output(output_grid)
