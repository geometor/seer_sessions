"""
Transforms an input grid (2D NumPy array, typically 1xN) based on the following rules:
1. Extracts the first row as the data sequence.
2. Identifies the contiguous sub-sequence in the data sequence starting from the 
   index of the first non-zero digit and ending at the index of the last 
   non-zero digit (the "active segment").
3. If no non-zero digits exist in the data sequence, the output grid is 
   identical to the input grid.
4. Determines the digit that appears most frequently within the original 
   active segment (the "dominant digit").
5. Constructs a new 1D sequence by:
   a. Taking the elements from the original data sequence before the active segment.
   b. Appending the dominant digit, repeated for the length of the active segment.
   c. Appending the elements from the original data sequence after the active segment.
6. Formats this new 1D sequence into a 2D NumPy array with the same shape as the 
   original input grid.
"""

import numpy as np
from collections import Counter

def _find_active_segment_indices(sequence):
    """
    Finds the start and end indices of the first and last non-zero elements 
    in a 1D sequence (list or 1D numpy array).
    Returns (None, None) if no non-zero elements are found.
    """
    # Convert to list for consistent indexing and iteration
    sequence_list = list(sequence) 
    non_zero_indices = [i for i, x in enumerate(sequence_list) if x != 0]
    if not non_zero_indices:
        return None, None
    return non_zero_indices[0], non_zero_indices[-1]

def _find_dominant_digit(segment):
    """
    Finds the most frequent digit in a given segment (list or sequence of digits).
    If there's a tie, Counter.most_common(1) returns one of the most frequent.
    Returns None if the segment is empty.
    """
    if not segment:
        return None 
    counts = Counter(segment)
    # most_common(1) returns a list like [(element, count)], so access [0][0]
    dominant_digit, _ = counts.most_common(1)[0]
    return dominant_digit

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (2D NumPy array).
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        # This case might occur if the testing framework deviates
        # or for robustness. Assume list of lists if not ndarray.
        input_grid = np.array(input_grid)

    # Handle empty input grid edge case
    if input_grid.size == 0:
        return input_grid.copy() # Return an empty array of the same shape

    # 1. Extract the first row as the data sequence (assuming 1xN or MxN where we process row 0)
    # Use .tolist() for easier slicing and processing with helper functions
    data_sequence = input_grid[0].tolist() 

    # 2. Identify the active segment indices
    start_index, end_index = _find_active_segment_indices(data_sequence)

    # 3. Handle the case where there are no non-zero digits
    if start_index is None:
        # Return a copy of the original grid
        return input_grid.copy() 

    # 4. Extract the original active segment using the found indices
    # Slicing is end-exclusive, so add 1 to end_index
    active_segment = data_sequence[start_index : end_index + 1]

    # 5. Find the dominant digit in the original active segment
    dominant_digit = _find_dominant_digit(active_segment)
    
    # If dominant_digit is None (e.g., empty active_segment, though unlikely here), handle defensively
    if dominant_digit is None:
         # This shouldn't happen if start_index is not None, but good practice
         return input_grid.copy() 

    # 6. Construct the output sequence (as a list first)
    #    a. Get the part before the active segment
    prefix = data_sequence[:start_index]
    
    #    b. Create the new middle part with the dominant digit
    segment_length = end_index - start_index + 1
    middle = [dominant_digit] * segment_length
    
    #    c. Get the part after the active segment
    suffix = data_sequence[end_index + 1:]

    # Combine the parts into the new 1D sequence
    output_sequence_list = prefix + middle + suffix

    # 7. Format the output sequence back into a 2D NumPy array matching the input shape
    # Convert the list back to a numpy array, preserving original dtype if possible
    output_row_np = np.array(output_sequence_list, dtype=input_grid.dtype)
    
    # Create the output grid, assuming the transformation only affects the first row
    # If input has more rows, copy them; otherwise, just reshape the modified row.
    # A safer assumption based on examples is that input is always (1, N)
    output_grid = np.copy(input_grid) # Start with a copy
    output_grid[0] = output_row_np # Replace the first row

    # Alternatively, if strictly 1xN input is guaranteed:
    # output_grid = output_row_np.reshape(input_grid.shape) 

    return output_grid