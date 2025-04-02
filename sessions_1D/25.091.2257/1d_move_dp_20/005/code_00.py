import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a single-row input grid based on a specific pattern.
1. Identifies the sequence `[0, 0, 1, 0]` (two whites, one blue, one white) within the input grid row. Let the index of the blue pixel (`1`) be `M`.
2. Identifies the two white pixels (`[0, 0]`) immediately preceding the blue pixel. These are located at indices `M-2` and `M-1`. These are the `moved_whites`.
3. Constructs the output row by:
    a. Starting with the `moved_whites` (`[0, 0]`).
    b. Appending all pixels from the beginning of the input row up to (but not including) the `moved_whites` (i.e., indices `0` to `M-3`).
    c. Appending the final part of the marker pattern, which is the blue pixel and the last white pixel (`[1, 0]`), located at indices `M` and `M+1` in the input.
4. The resulting sequence forms the output grid row, which will have the same length as the input row.
"""

def find_pattern_1_index(row: List[int]) -> Optional[int]:
    """
    Finds the index of the '1' in the pattern [..., 0, 0, 1, 0].

    Args:
        row: The list of integers representing the grid row.

    Returns:
        The index of the '1' if the pattern is found, otherwise None.
    """
    # Iterate backwards from the second-to-last possible position of '1'
    # Need indices i-2, i-1, i, i+1, so i must be at least 2 and at most len(row) - 2
    if len(row) < 4:
        return None # Pattern cannot exist if row is too short

    for i in range(len(row) - 2, 1, -1): 
        # Check if the pattern [0, 0, 1, 0] exists ending at index i+1
        if (row[i] == 1 and
            row[i+1] == 0 and
            row[i-1] == 0 and
            row[i-2] == 0):
            return i  # Return the index of the '1'
    return None # Pattern not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list containing a single list (the row) of integers.
                    Can also handle a NumPy array input.

    Returns:
        A list containing the single transformed row as a list of integers.
        Returns the original grid if the pattern is not found or input is invalid.
    """
    # --- Input Validation and Preparation ---
    # Check if input is a list or numpy array
    if not isinstance(input_grid, (list, np.ndarray)):
        print("Warning: Invalid input_grid type. Expected list or numpy array.")
        return [] # Return empty list for fundamentally wrong input type

    # Check if it contains exactly one row
    if len(input_grid) != 1:
         print(f"Warning: Expected input grid with 1 row, got {len(input_grid)}. Returning original.")
         # Return the input in list format if possible, otherwise handle based on type
         if isinstance(input_grid, np.ndarray):
             try:
                 return input_grid.tolist()
             except Exception: # Catch potential errors during conversion
                  return [] # Return empty if conversion fails
         elif isinstance(input_grid, list):
              return input_grid # Return the multi-row list as is
         else:
              return [] # Fallback

    # Extract the row, handle numpy array case gracefully
    input_row = []
    try:
        if isinstance(input_grid, np.ndarray):
            # Ensure it's a 2D array before accessing [0]
            if input_grid.ndim == 2 and input_grid.shape[0] == 1:
                 input_row = input_grid[0].tolist()
            else:
                 # Handle cases like 1D array or incorrect shape
                 print(f"Warning: Unexpected NumPy array shape {input_grid.shape}. Trying to flatten.")
                 input_row = input_grid.flatten().tolist() # Attempt flatten
                 if len(input_grid) != 1: # Re-check after potential flatten
                      print("Warning: Still not a single row structure after flatten. Returning empty.")
                      return []
                 input_grid = [input_row] # Adjust input_grid to match expected structure
            
        elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
             input_row = input_grid[0]
        else:
             print("Warning: Input grid structure is not a list containing a single list.")
             # Attempt to recover if it's just a flat list provided directly
             if isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
                 print("Assuming input was a flat list representing the single row.")
                 input_row = input_grid
                 input_grid = [input_row] # Wrap it for consistency
             else:
                  return [[]] # Return list containing empty list for invalid structure
    except Exception as e:
        print(f"Error processing input grid: {e}. Returning empty list.")
        return [[]]


    # --- Core Logic ---
    # 1. Find the index 'M' of the '1' in the pattern [0, 0, 1, 0]
    marker_1_index = find_pattern_1_index(input_row)

    # Handle case where pattern is not found
    if marker_1_index is None:
        print("Warning: Pattern [0, 0, 1, 0] not found. Returning original grid.")
        # Return in standard list-of-lists format
        return input_grid # Return the original validated/adjusted input_grid

    # 2. Identify the 'moved_whites' ([0, 0] immediately before '1')
    # These are at indices M-2 and M-1
    moved_whites_start_index = marker_1_index - 2
    moved_whites = input_row[moved_whites_start_index : marker_1_index] 
    # Check assumption if needed: 
    # if moved_whites != [0, 0]: print("Warning: Pixels before '1' were not [0,0]")

    # 3. Identify the 'prefix' (elements before the moved_whites)
    # These are from index 0 up to (but not including) moved_whites_start_index
    prefix = input_row[0 : moved_whites_start_index]

    # 4. Identify the 'suffix' ([1, 0] starting at marker_1_index)
    # These are at indices M and M+1
    suffix = input_row[marker_1_index : marker_1_index + 2]
    # Check assumption if needed:
    # if suffix != [1, 0]: print("Warning: Pixels at/after '1' were not [1,0]")

    # 5. Construct the output row by concatenating: moved_whites + prefix + suffix
    output_row = moved_whites + prefix + suffix

    # 6. Return the output grid in the standard format (list of lists)
    return [output_row]