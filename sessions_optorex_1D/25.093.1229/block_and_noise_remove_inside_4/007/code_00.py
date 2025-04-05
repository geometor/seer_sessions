import collections
import numpy as np
import math # Available, but not used

"""
Transforms an input grid (typically a single row representing a sequence of digits) 
by identifying contiguous subsequences (islands) of non-zero digits. Within each 
island, it finds the most frequently occurring digit (the dominant digit). All 
digits within that island are then replaced by this dominant digit in the output 
sequence. Zero digits act as separators between islands and remain unchanged. 
The output grid retains the format of the input grid (list-of-lists or NumPy array).
"""

def _find_dominant_digit(island_digits):
  """
  Helper function to find the most frequent digit in a list of non-zero digits.
  If there's a tie, collections.Counter.most_common(1) returns one of the most common.
  
  Args:
    island_digits: A list of integers representing the digits in an island.

  Returns:
    The integer digit that appears most frequently in the list. Returns None if 
    the list is empty.
  """
  if not island_digits:
    return None 
  # Count occurrences of each digit
  counts = collections.Counter(island_digits)
  # Find the digit with the highest count. most_common(1) returns list like [(digit, count)]
  dominant_digit = counts.most_common(1)[0][0]
  return dominant_digit

def transform(input_grid):
    """
    Applies the island dominance transformation to the sequence within the input grid.

    Args:
      input_grid: A NumPy array or list of lists representing the input grid. 
                  Expected to contain a single row for this task's examples.

    Returns:
      A NumPy array or list of lists (matching input type) with the transformed sequence.
    """

    # 1. Handle input format and extract the 1D sequence
    is_numpy = isinstance(input_grid, np.ndarray)
    if is_numpy:
        # Assuming the relevant data is in the first row if it's 2D, 
        # or it's already 1D. Using .tolist() for easier processing.
        if input_grid.ndim > 1:
            input_sequence = input_grid[0].tolist()
        else:
             input_sequence = input_grid.tolist()
    elif isinstance(input_grid, list) and input_grid and isinstance(input_grid[0], list):
         # Assumes list-of-lists format, take the first list
         input_sequence = list(input_grid[0]) # Ensure it's a mutable list copy
    elif isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
         # Handle case where input might be a flat list directly
         input_sequence = list(input_grid)
         # We'll need to decide output format later, maybe default to list-of-list? 
         # For consistency with ARC, let's assume the test harness expects list-of-lists or numpy.
         # If input was flat list, maybe return flat list? Let's stick to list-of-lists for now
         # based on typical ARC outputs. We can adjust if tests fail.
         # Let's track if the input was *originally* flat
         was_flat_list = True 
    else:
        # Handle unexpected formats or empty input
        # Returning input as-is or raising error might be options.
        # For now, let's try returning input if format is unknown.
        return input_grid 

    n = len(input_sequence)
    # 2. Create a mutable copy for the output sequence
    output_sequence = list(input_sequence) 
    
    was_flat_list = not (is_numpy or (isinstance(input_grid, list) and input_grid and isinstance(input_grid[0], list)))


    # 3. Iterate through the sequence to identify islands and apply transformations
    i = 0
    while i < n:
        # 3a. Check if the current digit is non-zero (start of a potential island)
        if input_sequence[i] != 0:
            start_index = i
            current_island_digits = []
            
            # 3b. Find the extent of the current island (scan consecutive non-zeros)
            while i < n and input_sequence[i] != 0:
                current_island_digits.append(input_sequence[i])
                i += 1
            # Loop ends when a zero is hit or end of sequence. Last non-zero was at i-1.
            end_index = i - 1 # Inclusive index of the island's end

            # 3c. Determine the dominant digit for this island
            dominant_digit = _find_dominant_digit(current_island_digits)

            # 3d. Replace digits in the output sequence for this island's range
            if dominant_digit is not None: # Check if island was not empty
                for j in range(start_index, end_index + 1):
                    output_sequence[j] = dominant_digit
            # 'i' is already positioned at the element *after* the island, loop continues correctly.
        
        # 3e. If the current digit is zero, it's a separator. It's already correct in the output copy. Move on.
        else:
            i += 1

    # 4. Format the output sequence back into the original input structure
    if is_numpy:
        # Reshape based on original input dimensions if possible
        # Since examples are 1xN, reshape to (1, N) or return 1D if input was 1D
        if input_grid.ndim > 1:
             output_grid = np.array([output_sequence], dtype=input_grid.dtype)
        else: # Input was 1D numpy array
             output_grid = np.array(output_sequence, dtype=input_grid.dtype)
    elif was_flat_list:
         # If input was a flat list, return a flat list
         output_grid = output_sequence
    else: # Assumed list-of-lists input
        output_grid = [output_sequence]
        

    return output_grid