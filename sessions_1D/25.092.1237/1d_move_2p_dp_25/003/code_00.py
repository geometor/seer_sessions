import numpy as np

"""
Transformation Rule:
1.  Receive the input sequence (as a NumPy array of integers).
2.  Locate the index of the first occurrence of the maroon (9) pixel, which acts as a delimiter.
3.  Split the input sequence into two parts based on the delimiter index:
    *   `prefix`: The subsequence of pixels from the beginning up to (but not including) the delimiter.
    *   `suffix`: The subsequence of pixels starting from the delimiter to the end of the sequence.
4.  Within the `prefix`, identify and separate pixels into two groups:
    *   `white_pixels`: All pixels with the value 0.
    *   `non_white_pixels`: All pixels with values other than 0, maintaining their original relative order.
5.  Create the `transformed_prefix` by concatenating the `white_pixels` array followed by the `non_white_pixels` array.
6.  Construct the final output sequence by concatenating the `transformed_prefix` and the original `suffix`.
7.  Return the final output sequence as a NumPy array.
"""

# Imports
import numpy as np

# Define color constants
WHITE = 0
MAROON = 9

def find_first_delimiter(sequence: np.ndarray, delimiter_value: int) -> int:
    """
    Finds the index of the first occurrence of the delimiter value in a NumPy array.
    
    Args:
        sequence: The input NumPy array.
        delimiter_value: The integer value to search for.
        
    Returns:
        The index of the first occurrence of the delimiter. If the delimiter
        is not found, returns the length of the sequence.
    """
    indices = np.where(sequence == delimiter_value)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        # If delimiter not found, standard behavior is to treat entire sequence as prefix
        return len(sequence)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D grid (NumPy array) by moving all white (0) pixels 
    before the first maroon (9) pixel to the beginning of that segment, while 
    preserving the relative order of other non-white pixels. The segment 
    starting from the maroon pixel remains unchanged.

    Args:
        input_grid: A NumPy array of integers representing the input sequence.

    Returns:
        A NumPy array of integers representing the transformed sequence.
    """
    
    # Find the index of the first maroon pixel (delimiter)
    delimiter_index = find_first_delimiter(input_grid, MAROON)

    # Split the sequence into prefix and suffix using NumPy slicing
    prefix = input_grid[:delimiter_index]
    suffix = input_grid[delimiter_index:]

    # Check if prefix is empty; if so, no transformation needed, return original grid
    if prefix.size == 0:
        # Handle case where delimiter is the first element or grid is empty
         # If the suffix is also empty (empty input grid), return empty array
        if suffix.size == 0:
             return np.array([], dtype=input_grid.dtype)
        # If prefix is empty but suffix exists, return the original grid (as suffix is unchanged)
        return input_grid # or suffix, but returning input_grid covers empty input case too
        
    # Separate white (0) and non-white pixels from the prefix using boolean indexing
    # Boolean indexing inherently preserves the relative order of the selected elements
    white_pixels = prefix[prefix == WHITE]
    non_white_pixels = prefix[prefix != WHITE]

    # Create the transformed prefix by concatenating the separated arrays
    # np.concatenate requires a tuple or list of arrays
    # Handle cases where one or both might be empty
    if white_pixels.size > 0 and non_white_pixels.size > 0:
        transformed_prefix = np.concatenate((white_pixels, non_white_pixels))
    elif white_pixels.size > 0:
        transformed_prefix = white_pixels # Only white pixels were in prefix
    elif non_white_pixels.size > 0:
        transformed_prefix = non_white_pixels # Only non-white pixels were in prefix
    else:
        # This case should technically be covered by the prefix.size == 0 check earlier,
        # but included for completeness. An empty prefix results in an empty transformed_prefix.
        transformed_prefix = np.array([], dtype=input_grid.dtype)

    # Construct the final output sequence by joining the transformed prefix and the original suffix
    # Handle cases where transformed_prefix or suffix might be empty
    if transformed_prefix.size > 0 and suffix.size > 0:
         output_grid = np.concatenate((transformed_prefix, suffix))
    elif transformed_prefix.size > 0:
         output_grid = transformed_prefix # Suffix was empty (delimiter was last element or not found)
    elif suffix.size > 0:
         # This implies prefix was empty, handled earlier, but for robustness:
         output_grid = suffix # Transformed prefix was empty
    else:
         # If both transformed_prefix and suffix are empty (implies empty input)
         output_grid = np.array([], dtype=input_grid.dtype)
         
    return output_grid