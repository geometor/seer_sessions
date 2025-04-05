import copy

"""
Transforms an input sequence of 0s and 1s into an output sequence where 0s adjacent 
to blocks of exactly two consecutive 1s are changed to 3s. All other numbers (1s 
and 0s not adjacent to exactly two 1s) remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (list or array).

    Args:
        input_grid: A list or array of integers (0s and 1s).

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Ensure input is a list for easier manipulation if it's a numpy array
    input_list = list(input_grid) 
    n = len(input_list)
    
    # Initialize output_grid as a copy of input_list
    # Use deepcopy if elements were mutable, but integers are not, so list() is fine.
    output_list = list(input_list) 

    # Iterate through the list to find potential starting positions of '1 1' blocks
    # We only need to check up to index n-2 because we need pairs input_list[i] and input_list[i+1]
    for i in range(n - 1):
        # Check if the current element and the next element form a '1 1' block
        if input_list[i] == 1 and input_list[i+1] == 1:
            
            # --- Verify it's *exactly* two 1s ---
            # Check the element *before* the block (if it exists) is not a 1
            is_start_ok = (i == 0 or input_list[i-1] != 1)
            
            # Check the element *after* the block (if it exists) is not a 1
            is_end_ok = (i + 2 >= n or input_list[i+2] != 1)

            # --- If it's exactly two 1s, modify adjacent 0s ---
            if is_start_ok and is_end_ok:
                # Modify the element *before* the block if it's a 0 and within bounds
                if i > 0 and input_list[i-1] == 0:
                    output_list[i-1] = 3
                
                # Modify the element *after* the block if it's a 0 and within bounds
                if i + 2 < n and input_list[i+2] == 0:
                    output_list[i+2] = 3

    # Return the modified list
    return output_list