import copy
import numpy as np

"""
Transforms a single-row input grid by identifying two 'marker' pixels of the 
same non-white color. It then fills the segment of pixels strictly between 
these two markers with the marker color. All other pixels remain unchanged. 
The input is assumed to be a grid containing exactly one row, and this row 
contains exactly two pixels of the same non-white color, with all other pixels 
being white (0). The function handles both list-of-lists and NumPy array inputs.
"""

def find_non_white_markers(grid_row):
    """
    Finds the color and indices of the two non-white marker pixels in a 1D grid row.
    Validates that exactly two markers of the same non-white color exist, 
    and no other non-white colors are present.

    Args:
        grid_row: A list of integers representing a single row of the grid.

    Returns:
        A tuple (marker_color, indices) where marker_color is the integer
        color value and indices is a sorted list containing the two column
        indices of the markers. Returns (None, []) if the expected pattern 
        (exactly two markers of same non-white color, others white) is not met.
    """
    marker_color = None
    indices = []

    # Iterate through the row to find non-white pixels and their indices
    for idx, pixel_color in enumerate(grid_row):
        if pixel_color != 0: # Found a non-white pixel
            if marker_color is None:
                # This is the first non-white pixel found
                marker_color = pixel_color
                indices.append(idx)
            elif pixel_color == marker_color:
                # This is a subsequent pixel matching the first marker's color
                indices.append(idx)
            else:
                # Found a non-white pixel of a *different* color - violates assumption
                # print(f"Pattern Violation: Found different non-white color {pixel_color} at index {idx}. Expected {marker_color}.")
                return None, [] # Pattern violated: multiple non-white colors

    # After checking all pixels, validate that exactly two markers were found
    if len(indices) == 2:
        # Correct pattern found: return the color and the sorted indices
        # Sorting is good practice although iteration order likely ensures it here.
        return marker_color, sorted(indices) 
    else:
        # Did not find exactly two markers of the *same* non-white color
        # print(f"Pattern Violation: Found {len(indices)} markers of color {marker_color}. Expected 2.")
        return None, [] # Pattern violated: incorrect number of markers


def transform(input_grid):
    """
    Transforms the input grid by filling the segment between two identical 
    non-white markers in its single row with their color. Handles list or numpy array input.
    
    Args:
        input_grid: A list of lists or NumPy array representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid (1xN). Returns
        a copy of the input if the expected marker pattern isn't found or if input is invalid.
    """
    
    # --- Input Standardization and Validation ---
    try:
        # Convert potential NumPy array to list of lists for consistent processing
        grid_list = np.array(input_grid, dtype=int).tolist() 
        
        # Validate structure: must be list of lists, must have exactly one row
        if not isinstance(grid_list, list) or not grid_list or not isinstance(grid_list[0], list):
             # print("Warning: Input grid is not a valid list of lists.")
             # Attempt to return original structure if possible
             try:
                 return copy.deepcopy(input_grid)
             except: # Fallback if deepcopy fails
                 return [[0]] # Or some other error indicator
                 
        if len(grid_list) != 1:
            # print("Warning: Input grid does not have exactly one row.")
            # Attempt to return original structure
            try:
                 return copy.deepcopy(input_grid)
            except:
                 return [[0]] 

        input_row = grid_list[0]
        
    except Exception as e:
        # print(f"Error processing input grid: {e}")
        # Cannot proceed if input is fundamentally broken, return original if possible
        try:
            return copy.deepcopy(input_grid)
        except: # If even deepcopy fails on the input
             return [[0]] # Default error grid

    # --- Core Transformation Logic ---
    
    # Create a deep copy of the input row to modify for the output.
    # This ensures the original input is untouched and handles cases where no transformation occurs.
    output_row = copy.deepcopy(input_row)

    # Find the marker color and their indices using the helper function
    marker_color, marker_indices = find_non_white_markers(input_row)

    # Proceed only if valid markers were found (color is not None implies 2 indices found)
    if marker_color is not None:
        # Get the start (exclusive) and end (exclusive) column indices for the segment to fill
        # Indices: marker_indices[0] < i < marker_indices[1]
        start_fill_index = marker_indices[0] + 1
        end_fill_index = marker_indices[1] # range() is exclusive of the end value

        # Fill the segment between the markers in the output row copy
        # Basic bounds check for robustness, though marker finding logic should ensure validity
        if 0 <= start_fill_index < end_fill_index <= len(output_row):
            for i in range(start_fill_index, end_fill_index):
                 # Check if the pixel to be filled is currently white (as per observed pattern)
                 # This is an implicit assumption check based on examples, not strictly required by the core logic
                 # if output_row[i] == 0: 
                 output_row[i] = marker_color
                 # else:
                 #    print(f"Warning: Pixel at index {i} was not white before filling.")
        # else:
             # This case should ideally not happen if find_non_white_markers is correct
             # print("Warning: Invalid marker indices calculated for filling.")

    # --- Output Formatting ---
    
    # Reconstruct the output grid as a list containing the single modified row
    # to match the standard ARC grid format (list of lists)
    output_grid = [output_row]

    return output_grid