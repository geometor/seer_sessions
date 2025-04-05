import copy
# numpy is implicitly available but not explicitly needed for this logic if input is list-like
# import numpy as np 

"""
Transforms a sequence of digits based on the following rules:
1. Locate the digit '2', which acts as a fixed marker.
2. Find the nearest non-zero digit to the left of the marker ('left_fill_value').
3. Replace all zeros strictly between the 'left_fill_value' and the marker with 'left_fill_value'.
4. Find the nearest non-zero digit to the right of the marker ('right_fill_value').
5. Replace all zeros strictly between the marker and the 'right_fill_value' with 'right_fill_value'.
6. If no non-zero digit exists on a side (left or right), no filling occurs on that side.
7. The marker '2' and existing non-zero digits in the input sequence remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list-like sequence (e.g., list, numpy array) of integers.

    Returns:
        A new list or array representing the transformed sequence. Returns a copy
        of the original if the marker '2' is not found.
    """
    
    # Initialize output_grid as a deep copy to avoid modifying the input object
    # This works for both lists and numpy arrays
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid) # Get the length of the sequence

    # Find the index of the marker '2'
    marker_index = -1
    try:
        # Convert to list temporarily to use the .index() method reliably
        # This handles cases where input_grid might be a numpy array
        input_list_for_index = list(input_grid) 
        marker_index = input_list_for_index.index(2)
    except ValueError:
        # Marker '2' not found, return the original grid copy unchanged
        return output_grid # No transformation needed if no marker

    # --- Left-side processing: Find nearest non-zero and fill ---
    left_fill_value = None
    left_fill_index = -1
    # Search backwards from the position immediately left of the marker
    for i in range(marker_index - 1, -1, -1):
        if input_grid[i] != 0:  # Found the nearest non-zero digit
            left_fill_value = input_grid[i]
            left_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the left, fill the zeros in between
    if left_fill_value is not None:
        # Iterate from the position right after the left fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            # Check if the position in the original grid was a zero before filling
            if input_grid[i] == 0: 
                 output_grid[i] = left_fill_value # Update the output grid

    # --- Right-side processing: Find nearest non-zero and fill ---
    right_fill_value = None
    right_fill_index = -1
    # Search forwards from the position immediately right of the marker
    for i in range(marker_index + 1, n):
        if input_grid[i] != 0: # Found the nearest non-zero digit
            right_fill_value = input_grid[i]
            right_fill_index = i
            break # Stop searching once the nearest is found

    # If a non-zero value was found to the right, fill the zeros in between
    if right_fill_value is not None:
        # Iterate from the position right after the marker up to (not including) the right fill value
        for i in range(marker_index + 1, right_fill_index):
            # Check if the position in the original grid was a zero before filling
             if input_grid[i] == 0: 
                 output_grid[i] = right_fill_value # Update the output grid

    # Return the modified grid
    return output_grid