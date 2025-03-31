import numpy as np

"""
Identify the widest contiguous vertical stripe (block of columns) where all pixels in those columns are white (0) in the input grid. 
Then, change the color of all pixels within this identified stripe to green (3) in the output grid. Pixels outside this stripe remain unchanged.
"""

def find_widest_contiguous_stripe(indices):
    """
    Finds the start and end indices of the longest contiguous sequence in a sorted list of indices.

    Args:
        indices: A sorted list of integer indices.

    Returns:
        A tuple (start_index, end_index) of the widest stripe, or (-1, -1) if no stripe exists.
    """
    if not indices:
        return -1, -1 # No relevant columns

    max_len = 0
    current_len = 0
    start_index_max = -1
    current_start_index = -1

    for i in range(len(indices)):
        # Check if it's the first element or contiguous with the previous
        if i == 0 or indices[i] == indices[i-1] + 1:
            if current_len == 0:
                 # Start of a new sequence
                 current_start_index = indices[i]
            current_len += 1
        else:
            # Sequence broken, check if the ended sequence was the longest so far
            if current_len > max_len:
                max_len = current_len
                start_index_max = current_start_index
            # Start a new sequence
            current_start_index = indices[i]
            current_len = 1

    # Check the last sequence after the loop finishes
    if current_len > max_len:
        max_len = current_len
        start_index_max = current_start_index
    
    # If no sequence was ever started (e.g., single element list was processed)
    elif max_len == 0 and current_len > 0:
         max_len = current_len
         start_index_max = current_start_index


    if start_index_max != -1:
        # Return the start and end index (inclusive) of the widest stripe
        return start_index_max, start_index_max + max_len - 1
    else:
        # This case should technically be covered by the initial empty check,
        # but serves as a fallback if only non-contiguous single columns were found.
        # Or if the input list was truly empty.
         if indices: # If there were indices, but no contiguous sequence > 1
             # Find the first single column as the 'widest' (length 1)
             start_index_max = indices[0]
             max_len = 1
             return start_index_max, start_index_max + max_len - 1
         else: # List was empty
            return -1, -1


def transform(input_grid):
    """
    Transforms the input grid by finding the widest vertical stripe of white pixels
    and coloring it green.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Convert input to numpy array for easier slicing and column operations
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # --- Identify all-white columns ---
    all_white_cols = []
    for j in range(cols):
        # Check if all elements in the column are 0 (white)
        if np.all(input_np[:, j] == 0):
            all_white_cols.append(j)

    # --- Find the widest contiguous stripe of all-white columns ---
    # The list of indices is already sorted as we iterated from 0 to cols-1
    start_col, end_col = find_widest_contiguous_stripe(all_white_cols)

    # --- Fill the widest stripe with green (3) ---
    if start_col != -1:
        # Select the columns from start_col to end_col (inclusive)
        # and set all their values to 3 (green)
        output_grid[:, start_col:end_col+1] = 3

    # Return the modified grid as a numpy array 
    # (or convert back to list of lists if required by the environment)
    # return output_grid.tolist() 
    return output_grid