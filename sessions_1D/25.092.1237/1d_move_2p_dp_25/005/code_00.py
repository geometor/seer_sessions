import numpy as np

"""
Transformation Rule:
1.  Receive the input sequence of pixels (as a NumPy array).
2.  Locate the index of the first occurrence of the maroon (9) pixel (the delimiter). If no delimiter is found, return the input sequence unchanged.
3.  Split the input sequence into two parts:
    *   `prefix`: The subsequence of pixels from the beginning up to (but not including) the delimiter index.
    *   `suffix`: The subsequence of pixels starting from the delimiter index to the end of the sequence.
4.  If the `prefix` is empty, return the input sequence unchanged.
5.  Identify the contiguous block of white (0) pixels located immediately at the end of the `prefix` (i.e., just before the delimiter).
6.  Determine the starting index (`split_point`) of this contiguous white block within the `prefix`. If no white block exists at the end, the `split_point` is the length of the `prefix`.
7.  Separate the `prefix` into two parts based on the `split_point`:
    *   `part_before_moved_whites`: Pixels from the start of the `prefix` up to the `split_point` (exclusive).
    *   `moved_whites`: The contiguous block of white pixels from the `split_point` to the end of the `prefix`.
8.  Create the `transformed_prefix` by concatenating the `moved_whites` followed by the `part_before_moved_whites`.
9.  Construct the final output sequence by concatenating the `transformed_prefix` and the original `suffix`.
10. Return the final output sequence as a NumPy array.
"""

# Imports
import numpy as np

# Define constants
WHITE = 0
MAROON = 9

def find_first_delimiter(sequence: np.ndarray, delimiter_value: int) -> int:
    """
    Finds the index of the first occurrence of the delimiter value in a NumPy array.
    
    Args:
        sequence: The input NumPy array.
        delimiter_value: The integer value to search for.
        
    Returns:
        The index of the first occurrence of the delimiter. Returns -1 if not found.
    """
    indices = np.where(sequence == delimiter_value)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        return -1 # Indicate not found

def find_start_of_trailing_zeros(sequence: np.ndarray) -> int:
    """
    Finds the starting index of a contiguous block of zeros at the end of a sequence.
    
    Args:
        sequence: The input NumPy array (prefix).
        
    Returns:
        The index where the trailing block of zeros begins. If no zeros are
        at the end, returns the length of the sequence.
    """
    if sequence.size == 0:
        return 0 # Empty sequence has no trailing zeros, split point is 0

    split_point = sequence.size # Initialize assuming no trailing zeros
    # Iterate backwards from the end
    for i in range(sequence.size - 1, -1, -1):
        if sequence[i] == WHITE:
            split_point = i # Update split_point to current index
        else:
            break # Stop when a non-zero element is found
    return split_point

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D grid (NumPy array) by moving the contiguous block
    of white (0) pixels located immediately before the first maroon (9) pixel 
    to the beginning of that segment. The relative order of other pixels in 
    that segment is preserved. The segment starting from the maroon pixel 
    remains unchanged.

    Args:
        input_grid: A NumPy array of integers representing the input sequence.

    Returns:
        A NumPy array of integers representing the transformed sequence.
    """
    
    # Find the index of the first maroon pixel (delimiter)
    delimiter_index = find_first_delimiter(input_grid, MAROON)

    # If delimiter not found, return the original grid unchanged
    if delimiter_index == -1:
        return input_grid.copy() # Return a copy to avoid modifying original

    # Split the sequence into prefix and suffix using NumPy slicing
    prefix = input_grid[:delimiter_index]
    suffix = input_grid[delimiter_index:]

    # If prefix is empty (delimiter was the first element), return original grid
    if prefix.size == 0:
        return input_grid.copy()

    # Find the starting index of the block of trailing zeros in the prefix
    split_point = find_start_of_trailing_zeros(prefix)

    # If split_point is the length of the prefix, means no trailing zeros were found
    if split_point == prefix.size:
        # No transformation needed for the prefix, return original grid
        return input_grid.copy() 
        
    # Separate the prefix into the part before the trailing zeros and the zeros themselves
    part_before_moved_whites = prefix[:split_point]
    moved_whites = prefix[split_point:]

    # Create the transformed prefix by concatenating moved_whites + part_before
    # Ensure both parts are valid NumPy arrays before concatenation
    if moved_whites.size > 0 and part_before_moved_whites.size > 0:
        transformed_prefix = np.concatenate((moved_whites, part_before_moved_whites))
    elif moved_whites.size > 0:
        transformed_prefix = moved_whites # Only trailing zeros in prefix
    elif part_before_moved_whites.size > 0:
        # This case means split_point was 0 but prefix was not empty,
        # implying the entire prefix was trailing zeros.
        # However, the initial split_point == prefix.size check should handle this.
        # Let's refine: if split_point is 0, the entire prefix is moved_whites.
        if split_point == 0: 
             transformed_prefix = prefix # The whole prefix was zeros
        else: # Should not happen based on logic, but safer
             transformed_prefix = part_before_moved_whites
    else: 
        # Prefix was empty, handled earlier
        transformed_prefix = np.array([], dtype=input_grid.dtype)
        
    # If split_point is 0, means the entire prefix consisted of zeros.
    # In this case, transformed_prefix is just the original prefix.
    if split_point == 0:
        transformed_prefix = prefix # No change needed as all were zeros to be moved
        
    # If split_point is not 0 and not prefix.size, perform the concatenation
    elif split_point < prefix.size :
        transformed_prefix = np.concatenate((moved_whites, part_before_moved_whites))

    # Construct the final output sequence by joining the transformed prefix and the original suffix
    # Ensure suffix is a valid NumPy array
    if transformed_prefix.size > 0 and suffix.size > 0:
         output_grid = np.concatenate((transformed_prefix, suffix))
    elif transformed_prefix.size > 0:
         output_grid = transformed_prefix # Suffix was empty 
    elif suffix.size > 0:
         # Should only happen if prefix was empty, already handled
         output_grid = suffix 
    else:
         # Empty input grid case
         output_grid = np.array([], dtype=input_grid.dtype)
         
    return output_grid