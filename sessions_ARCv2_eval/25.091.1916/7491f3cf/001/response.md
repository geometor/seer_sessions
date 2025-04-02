```python
import numpy as np

"""
The transformation identifies four 5x5 pattern regions (P1, P2, P3, P4) within 
a bordered grid. These regions are separated by columns of the border color.
The first three regions (P1, P2, P3) each contain a 'background' color and 
a distinct 'foreground' object color. The fourth region (P4) initially 
contains only the background color.

The transformation rule is to replace the content of the P4 region with a 
copy of one of the first three patterns (P1, P2, or P3). The pattern to be 
copied is selected based on the foreground color present in P1, P2, or P3, 
following a priority rule:
1. If Red (color 2) is the foreground color in any of P1, P2, or P3, copy the 
   pattern containing Red.
2. Otherwise, if Blue (color 1) is the foreground color in any of P1, P2, or P3, 
   copy the pattern containing Blue.

The border, separators, and the contents of P1, P2, and P3 remain unchanged 
in the output grid.
"""

def find_foreground(pattern_array, background_color):
    """
    Finds the unique color in a pattern array that is not the background color.
    
    Args:
        pattern_array (np.array): A 2D numpy array representing the pattern region.
        background_color (int): The background color value.

    Returns:
        int or None: The foreground color value, or None if only the background 
                     color is found (or the pattern is empty/invalid).
    """
    unique_colors = np.unique(pattern_array)
    for color in unique_colors:
        if color != background_color:
            return int(color) # Ensure return type is standard int
    return None

def transform(input_grid):
    """
    Transforms the input grid by copying a prioritized pattern (P1, P2, or P3) 
    into the fourth pattern region (P4).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input
    output_np = input_np.copy()
    
    # Define the row and column slices for the pattern regions (P1, P2, P3, P4)
    # Assumes a 7x25 grid structure with 1-pixel border/separators
    # Inner content is rows 1-5 (inclusive)
    rows_slice = slice(1, 6) 
    # P1: cols 1-5
    p1_cols_slice = slice(1, 6)
    # P2: cols 7-11
    p2_cols_slice = slice(7, 12)
    # P3: cols 13-17
    p3_cols_slice = slice(13, 18)
    # P4: cols 19-23
    p4_cols_slice = slice(19, 24)

    # Identify the background color (from P4)
    # Taking the top-left corner of P4
    background_color = int(input_np[rows_slice.start, p4_cols_slice.start]) 

    # Identify foreground colors and their associated pattern regions
    foreground_colors = {} # Dictionary to map foreground_color -> source_region_slice
    
    # Analyze P1
    p1_region = input_np[rows_slice, p1_cols_slice]
    fg1_color = find_foreground(p1_region, background_color)
    if fg1_color is not None:
        foreground_colors[fg1_color] = (rows_slice, p1_cols_slice)
        
    # Analyze P2
    p2_region = input_np[rows_slice, p2_cols_slice]
    fg2_color = find_foreground(p2_region, background_color)
    if fg2_color is not None:
        foreground_colors[fg2_color] = (rows_slice, p2_cols_slice)

    # Analyze P3
    p3_region = input_np[rows_slice, p3_cols_slice]
    fg3_color = find_foreground(p3_region, background_color)
    if fg3_color is not None:
        foreground_colors[fg3_color] = (rows_slice, p3_cols_slice)

    # Select the source pattern based on color priority (Red=2 > Blue=1)
    source_region_slice = None
    if 2 in foreground_colors: # Check for Red first
        source_region_slice = foreground_colors[2]
    elif 1 in foreground_colors: # Then check for Blue
        source_region_slice = foreground_colors[1]
    # else: # If neither Red nor Blue is found (shouldn't happen based on examples)
        # Handle error or default case if necessary, but problem implies one exists.
        # For robustness, could raise an error or default to P1, etc.
        # print("Warning: Neither Red (2) nor Blue (1) foreground color found.")
        # If we assume the problem guarantees 1 or 2 is present, no else needed.

    # Copy the selected source pattern into the P4 region of the output grid
    if source_region_slice is not None:
        source_pattern = input_np[source_region_slice]
        output_np[rows_slice, p4_cols_slice] = source_pattern
    else:
        # This case implies neither color 1 nor 2 was found, which contradicts examples.
        # The output grid remains unchanged in P4 in this unexpected scenario.
        print("Error: Could not find a pattern with Red (2) or Blue (1) foreground color.")

    # Convert the output numpy array back to a list of lists
    return output_np.tolist()
```