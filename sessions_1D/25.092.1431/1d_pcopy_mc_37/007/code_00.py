import copy

"""
Transforms a 1D input grid (single row) by identifying isolated single non-white 
pixels and expanding each into a horizontal block of three pixels of the same 
color in the output grid.

An isolated pixel is defined as a non-white pixel (color != 0) located at an 
index `i` (where `0 < i < length - 1`) whose immediate left neighbor 
(at `i-1`) and immediate right neighbor (at `i+1`) in the *original* input 
grid both have different colors than the pixel at `i`.

The identification of isolated pixels is based solely on the original input 
grid state. The expansion overwrites the pixels at indices `i-1`, `i`, and 
`i+1` in the output grid with the color of the isolated pixel. Pixels not 
identified as isolated and not overwritten by an expansion retain their 
original input color.
"""

def _find_isolated_pixels(input_row):
    """
    Identifies isolated pixels in a single row based on the definition.
    
    An isolated pixel is non-white, not at the edges, and has neighbors 
    of different colors than itself.

    Args:
        input_row (list[int]): The row to analyze.
        
    Returns:
        list[tuple[int, int]]: A list of tuples, where each tuple contains 
                                (index, color) of an identified isolated pixel.
    """
    isolated_pixels_info = []
    row_len = len(input_row)
    
    # Iterate through potential isolated pixel indices (1 to len-2).
    # Pixels at index 0 and row_len - 1 cannot be isolated by definition 
    # as they lack two neighbors for comparison.
    for i in range(1, row_len - 1):
        current_color = input_row[i]
        
        # Condition 1: Pixel must be non-white (not background color 0).
        if current_color == 0:
            continue
            
        # Get neighbor colors
        left_color = input_row[i - 1]
        right_color = input_row[i + 1]
        
        # Condition 2 & 3: Neighbors must have different colors than the current pixel.
        if left_color != current_color and right_color != current_color:
            # This pixel meets all criteria for being isolated.
            isolated_pixels_info.append((i, current_color))
            
    return isolated_pixels_info

def transform(input_grid):
    """
    Applies the isolated pixel expansion transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A grid representing the input state 
                                      (expected to be 1xN).

    Returns:
        list[list[int]]: The transformed grid (1xN).
    """
    # --- Input Validation and Setup ---
    # Expect a grid containing exactly one row.
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format if necessary, though ARC guarantees valid formats.
        # Returning an empty grid structure for robustness.
        return [[]] 
        
    input_row = input_grid[0]
    row_len = len(input_row)

    # Handle edge case of an empty row within the grid.
    if row_len == 0:
      return [[]]

    # --- Initialization ---
    # Create a deep copy of the input row. This copy will be modified to become the output row.
    # Using a copy ensures that identifications are based purely on the original input state.
    output_row = copy.deepcopy(input_row)

    # --- Identify Objects/Patterns ---
    # Find all pixels in the *original* input row that meet the "isolated" criteria.
    # The helper function returns a list of (index, color) for these pixels.
    isolated_pixels = _find_isolated_pixels(input_row)

    # --- Apply Transformation ---
    # Iterate through the list of identified isolated pixels.
    for index, color in isolated_pixels:
        # For each isolated pixel, expand it into a 3-pixel block in the output row.
        # The _find_isolated_pixels function ensures 'index' is always valid for accessing 
        # index-1 and index+1 because it only checks indices between 1 and row_len - 2.
        
        # Modify the pixel to the left.
        output_row[index - 1] = color
        # Modify the pixel at the original index.
        output_row[index] = color
        # Modify the pixel to the right.
        output_row[index + 1] = color

    # --- Return Result ---
    # Wrap the modified output row back into the standard grid format (a list containing one list).
    return [output_row]