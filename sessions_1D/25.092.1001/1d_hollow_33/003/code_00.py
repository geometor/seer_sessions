import numpy as np # Import numpy as input might be numpy array
import copy # Potentially useful, though list slicing/copying is often sufficient

"""
Transformation Rule:
Identifies a single contiguous horizontal segment of non-white pixels (value > 0) in a 1xN input grid (row).
Modifies the segment by changing all interior pixels (pixels strictly between the first and last pixel of the segment) to white (value 0).
The first and last pixels of the segment, and all pixels outside the segment (background pixels), remain unchanged.
If no segment is found, or the segment has length 0 or 1 (no interior), the grid remains unchanged.
The output grid has the same dimensions as the input grid.
"""

def _find_segment_indices(row):
    """
    Finds the start and end indices of the first contiguous segment of non-zero values.

    Args:
        row (list or np.ndarray): A list or 1D numpy array representing a row of pixels.

    Returns:
        tuple: A tuple containing (start_index, end_index). Returns (None, None) 
               if no non-zero segment is found or the segment has length 0 or 1.
    """
    start_index = -1
    end_index = -1
    
    # Convert potential numpy array row to list for consistent iteration
    row_list = list(row)
    n = len(row_list)

    # Find the start index (first non-zero pixel)
    for i, pixel in enumerate(row_list):
        if pixel != 0:
            start_index = i
            break

    # If no non-zero pixel found, return None, None
    if start_index == -1:
        return None, None

    # Find the end index (last non-zero pixel)
    # Iterate backwards from the end of the list
    for i in range(n - 1, -1, -1):
        if row_list[i] != 0:
            end_index = i
            break
            
    # Check if the segment has interior pixels (length > 1 implies end > start)
    # If start_index == end_index, length is 1, no interior.
    # If end_index was never found (shouldn't happen if start_index was found), 
    # or if start_index > end_index (shouldn't happen with the search logic),
    # we don't have a valid segment with an interior.
    if start_index >= end_index: 
       return None, None # Segment length is 0 or 1, no interior

    # Ensure the found segment is contiguous (this specific task seems to guarantee it, but good practice)
    # Check if all pixels between start and end are non-zero *in the input*
    # This check might be redundant given the problem description but can prevent errors in similar tasks.
    # For this task, we assume the input guarantees one contiguous segment.
    # is_contiguous = all(row_list[i] != 0 for i in range(start_index, end_index + 1))
    # if not is_contiguous:
    #     # This condition might indicate multiple segments or an unexpected input format.
    #     # For this specific task, based on examples, we assume contiguity.
    #     # If it could fail, we might need to refine the segment finding logic.
    #     return None, None # Or handle error appropriately

    return start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]] or np.ndarray): A 2D list or numpy array 
                                      representing the input grid. Expected to be 1xN.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    
    # Handle potential numpy array input and ensure we work with lists
    if isinstance(input_grid, np.ndarray):
        # Convert numpy array to list of lists
        grid_list = input_grid.tolist()
    else:
        # Assume it's already list-like (e.g., list of lists)
        # Use deepcopy if modifying nested structures in place, but here we create a new list
        grid_list = [list(row) for row in input_grid] # Ensure inner lists are mutable copies

    # Basic validation for empty or incorrectly formatted input
    if not grid_list or not grid_list[0]:
        return [] # Return empty list for empty input

    # --- Core Logic ---
    # Assume grid is 1xN based on examples
    input_row = grid_list[0] 
    
    # Create a copy of the row to modify for the output
    output_row = list(input_row) # Ensure it's a mutable list copy

    # Find the start and end indices of the non-white segment in the original row
    start_index, end_index = _find_segment_indices(input_row)

    # Check if a valid segment with interior pixels was found
    # We need start_index < end_index - 1, which means end_index > start_index + 1
    if start_index is not None and end_index is not None and end_index > start_index + 1:
        
        # Iterate through the interior pixels of the segment
        # The range starts from the pixel *after* the start_index
        # and ends *before* the end_index.
        for i in range(start_index + 1, end_index):
            # Change the interior pixels to white (0) in the output row
            output_row[i] = 0

    # Return the modified row wrapped in a list to match the grid format
    output_grid = [output_row]
    
    return output_grid